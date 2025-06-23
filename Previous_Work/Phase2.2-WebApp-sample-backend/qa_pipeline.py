import pandas as pd
import os

import lancedb
from langchain_community.vectorstores.lancedb import LanceDB
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

import transformers
from transformers import AutoTokenizer
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from torch import cuda, bfloat16
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import RetrievalQA


# 1. Settings

embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'

HF_AUTH = os.getenv('HF_AUTH', None)
# model_id='meta-llama/Llama-2-7b-chat-hf'

model_id='Maykeye/TinyLLama-v0' # FOR UI INTEGRATION TESTING PURPOSES ONLY


# 2. Load the data

df = pd.read_csv('master_with_embeddings.csv')

documents=[]
for index, row in df.iterrows():
    doc = Document(page_content = row['chunk'],
                   metadata={'id': row['id'], 'title': row['title']})
    documents.append(doc)

print(f'---\n--- Loaded {len(documents)} embedded documents ---\n---')


# 3. Create retrievers 

bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k =  5

device = 'cuda' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embedding_model,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)

try:
    print("---\n--- Trying to connect to LanceDB ---\n---")
    db = lancedb.connect('/app/db')
    table = db.open_table("chatmaja_test")
    docsearch = LanceDB(connection=table, embedding=embed_model)
    print("---\n--- LanceDB found, connected successfully ---\n---")
except:
    print("---\n--- Error connecting to LanceDB, creating new one ---\n---")
    db = lancedb.connect('/app/db')
    table = db.create_table("chatmaja_test", data=[ # sample data to create the table
            {"vector": embed_model.embed_query("Hello World"), "text": "Hello World", "id": "1"}
        ], mode="overwrite")
    print("---\n--- LanceDB created and connected successfully ---\n---")
    docsearch = LanceDB.from_documents(documents, embed_model, connection=table)
    print("---\n--- Finished loading documents to LanceDB ---\n---")

retriever_lancedb = docsearch.as_retriever(search_kwargs={"k": 5})


ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_lancedb],
                                       weights=[0.4, 0.6])


# 4. Load LLM

model_config=transformers.AutoConfig.from_pretrained(
    model_id, token=HF_AUTH
)

# FOR CUDA ONLY
# bitsAndBites_config = transformers.BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type='nf4',
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=bfloat16
# )

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config = model_config,
    # quantization_config=bitsAndBites_config,
    device_map='auto',
    token = HF_AUTH
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(model_id,token = HF_AUTH)


# 5. Create the pipeline

#from assignment 4, we can change sth here, e.g. use other model, in general do some experiments
some_pipeline = transformers.pipeline(
    model= model, tokenizer=tokenizer,
    return_full_text = True,
    task='text-generation',
    # temperature=0.01, #parameter of the model
    max_new_tokens=512,
    repetition_penalty = 1.1
)

llm = HuggingFacePipeline(pipeline = some_pipeline)
rag_pipeline = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    verbose=True,
    retriever=ensemble_retriever,
    chain_type_kwargs={"verbose": True },
)

def answer_query(query: str) -> str:
    result = rag_pipeline(query)['result']
    answer = f"Query: {query}\n\nAnswer: {result}"
    return answer

