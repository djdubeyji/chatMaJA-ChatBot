import pandas as pd
import os

import lancedb
from langchain_community.vectorstores.lancedb import LanceDB
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from torch import cuda, bfloat16

import os
import urllib.request
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_core.runnables import RunnablePassthrough, RunnablePick



# 1. Settings

os.environ['HF_HOME'] = os.getenv('HF_HOME', 'models')

path_to_data_csv = 'master_with_embeddings_more_columns.csv'

path_to_database = 'db'
retrieve_top_k_docs_bm25 = 1
retrieve_top_k_docs_vector = 1

embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'

model_id='llama-2-7b-chat.Q2_K.gguf' # low quality, TheBloke/Llama-2-7B-GGUF 



# 2. Load the data

df = pd.read_csv(path_to_data_csv)

documents=[]
for index, row in df.iterrows():
    doc = Document(page_content = row['chunk'],
                   metadata={'id': row['id'], 'title': row['title'], 'authors': row['authors'], 'sources': row['sources']})
    documents.append(doc)

print(f'---\n--- Read {len(documents)} documents from {path_to_data_csv}')


# 3. Create retrievers

print(f'---\n--- Creating retrievers...')

bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k =  retrieve_top_k_docs_bm25

device = 'cuda' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embedding_model,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 32}
)

try:
    print("--- Trying to connect to LanceDB")
    db = lancedb.connect(path_to_database)
    table = db.open_table("chatmaja_test")
    docsearch = LanceDB(connection=table, embedding=embed_model)
    print("--- LanceDB found, connected successfully")
except:
    print("--- Error connecting to LanceDB, creating new one")
    db = lancedb.connect(path_to_database)
    table = db.create_table("chatmaja_test", data=[
            {"vector": embed_model.embed_query("Hello World"), "text": "Hello World", "id": "1", "authors": "authoors", "sources": "sourcees", "title": "tiitle"}
        ], mode="overwrite")
    print("--- LanceDB created and connected successfully")
    docsearch = LanceDB.from_documents(documents, embed_model, connection=table)
    print("--- Finished loading documents to LanceDB")

retriever_lancedb = docsearch.as_retriever(search_kwargs={"k": retrieve_top_k_docs_vector})

ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_lancedb],
                                       weights=[0.4, 0.6])

print("---\n--- Created BM25 and vector search retrievers")


# 4. Load LLM


# Download model if not exists

path_to_model = os.path.join(os.getenv('HF_HOME'), model_id)
link_to_model = f"https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/{model_id}"

if not os.path.isfile(path_to_model):
    print(f"--- Downloading {model_id}...")
    os.makedirs(os.getenv('HF_HOME'), exist_ok=True)
    urllib.request.urlretrieve(link_to_model, path_to_model)
    print(f"--- Downloaded {model_id} successfully.")
else:
    print(f"--- Model {model_id} already downloaded.")


# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Make sure the model path is correct for your system!
n_gpu_layers = -1 if device == 'cuda' else None
llm = LlamaCpp(
    model_path=path_to_model,
    temperature=0.75,
    max_tokens=100,
    n_gpu_layers=n_gpu_layers,
    n_ctx=512, # increasing context makes computations longer
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

# 5. Create the pipeline

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Prompt
rag_prompt_llama = hub.pull("rlm/rag-prompt-llama") # https://smith.langchain.com/hub/rlm/rag-prompt

# Chain
chain = (
    RunnablePassthrough.assign(context=RunnablePick("context") | format_docs)
    | rag_prompt_llama
    | llm
    | StrOutputParser()
)

def answer_query(question: str) -> str:
    print(f'- - - Question: {question}')
    docs = ensemble_retriever.get_relevant_documents(question)
    print(f'- - - Relevant documents: {[d.page_content for d in docs]}')
    answer = chain.invoke({"context": docs, "question": question})
    print(f'- - - Results: {answer}')
    sources = "Sources:\n - " + "\n - ".join([
        d.metadata['title'] + ", " + d.metadata['authors'] + ", " + d.metadata['sources'] 
        for d in docs])
    answer_with_sources = answer + '\n\n' + sources
    return answer_with_sources

def answer_query_streaming(message: str, history: list):    
    print(f'- - - Question: {message}')
    
    docs = ensemble_retriever.get_relevant_documents(message)
    print(f'- - - Relevant documents: {[d.page_content for d in docs]}')
    sources = "Sources:\n - " + "\n - ".join([
        d.metadata['title'] + ", " + d.metadata['authors'] + ", " + d.metadata['sources'] 
        for d in docs])
    
    printed_so_far = ''
    for chunk in chain.stream({"context": docs, "question": message}):
        printed_so_far += chunk
        yield printed_so_far

    answer_with_sources = printed_so_far + '\n\n' + sources
    yield answer_with_sources