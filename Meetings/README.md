# Meetings

Mentor:
- Robin Khanna (conference link: [heiconf](https://heiconf.uni-heidelberg.de/gxrh-waya-dwae-px3j), email:  R.Khanna@stud.uni-heidelberg.de)

Team members: 
- Agata Kaczmarek (email: agata.kaczmarek@stud.uni-heidelberg.de)
- Pranjal Sharma (email: pranjal.sharma@stud.uni-heidelberg.de)
- Jan Smoleń (email: jan.smolen@stud.uni-heidelberg.de)
- Mateusz Stączek (email: mateusz.staczek@stud.uni-heidelberg.de)

### 2023-10-30: First time meeting each other

Members present: All team members

### 2023-11-13: First meeting with the mentor

Members present: Mentor, all team members except Jan

Important points of discussion:
- we are very free in choosing the ways of solving the problem,
- for the first milestone, deliver at least what is specified in the document with project description. Doing more than necessary is fine,
- to speed up development, use a subset of data,
- do not train the LLM from scratch. We may try finetuning but good luck with that,
- take a pretrained model from [HuggingFace llm leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard), recommended are LLAMA2 or other models with 7B or 13B parameters. Quantization might help to fit the model on a GPU,
- for delivering the final milestone, no presentation is needed, not even being in Heidelberg in person. What only matters is the respository.

### 2023-11-14: Meeting about assignment and project

Members present: all team members

Important deadlines for now:
- assignment task 1-3 Agata, Mateusz, Jan
- as for "task 4" Pranjal: document what we are going to do, project planning, work flow, gather the research papers - the data (research on that), if you find any papers about the project tools, you document it also
- Next meeting: next monday 8pm, to speak about our parts, what we did, what problems we have
- peer review for our parts until Saturday
- 
### 2023-11-20: Meeting about assignment 2 and project

Members present: all team members

Points of discussion:
- review of the progress of doing assignment 2,
- review of work done by Pranjal about gathering data from PubMed. Troubles and solution - manually downloading abstracts works in batches of 10000 and by choosing different time spans. Needs further processing to merge, remove duplicates from overlapping time spans etc.
- next meeting about the project and assignment 2 is scheduled on 2023.11.26.

### 2023-11-26: Meeting about assignment 2 and project

Members present: all team members

Points of discussion:
- review of the finished assignment 2,
- review of work done by Pranjal about project planning and the gathered data (abstracts and titles). Mentor has approved manual process of acquiring data if well documented and updates are possible.
- discussion about further plan for doing the project - tokenization of abstracts. Further plans later,
- next meeting about the project is scheduled on 2023.12.13.

### 2023-12-13: Meeting about assignment 3 and project

Members present: all team members

Points of discussion:
- division of work for assignment 3 and project: 
  - Pranjal, Agata, Mateusz - tasks 1-3 of assignment 3,
  - Jan - work on the project, including choosing vector database,
- a meeting with the mentor is scheduled on 2023.12.18 at 3 p.m., for 20 minutes - we need to make repo look better by then,
- to make repo more accessible, Pranjal will add readme.md files,
- a document with a simple plan of the project as presented on the tutorials would help, Agata will make it.

### 2023-12-18: Short meeting with the mentor

Members present: Mentor and all team members

Points of discussion:
- review of the progress of doing assignment 3 - approved,
- in the near future come up with the test data, 50-100 instances,
- database working and be able to answer queries also for first milestone,
- proper maintaining of GitHub also counts for milestone,
- team members did not raise any questions or issues regarding the project.


### 2024-01-09: Short meeting before first milestone

Members present: All team members

Points of discussion:
- Jan set db and inputed the data into it, the embeddings were done using BERT
- for now everything is locally
- similarity - inner product
- for now also it's about articles, not sentences or any other chunks, so we should change it in the future

- we will meet with mentor on 11th at 11.35
- Pranjal is not available until 18th Jan
- for 11th Jan we prepare the presentation:
	- Pranjal - data downloading and preprocessing (he will also start preparing the presentation slides)
	- Jan - what works for now with db
	- Pranjal - about UI, what we have for now
	- Agata + Mateusz - what we plan to change in parts that are ready now + what to add (e.g. use of LangChain)
	
- test data - Agata will think about some
- Jan will send the presentation before tommorows night

- Questions:
	- keywords - is lexicographic search and a separate database needed?
	- test data - how to create: use ChatGPT or create manually? how many questions are sufficient?

   ![image](https://github.com/mstaczek/QAsystem-INLPT-WS2023/assets/56119853/f4cb0a60-916e-4203-8871-ba9459888915)

### 2024-01-11: First milestone meeting with mentor

Members present: Mentor and all team members

- we are on the good way for the project
- LLM could improve the performacje of IR, as we can e.g. choose best k with IR and ask LLM to choose best from this best k
- we should experiment with  chunks, this is key to the success
- Test Data should have 20-100 examples, can be generated with ChatGPT
- for our problems with keywords and semantic search, there is an idea we might try: two databases is overhead, but hybrid search is what we are looking for (OpenSearch has it)
- we should upload slides to GitHub

### 2024-01-31: Planning of our solution

Members present: Agata Kaczmarek, Mateusz Stączek

- analysis of the solution from assignment 4,
- planning our pipeline - steps, components.

### 2024-02-09: Research on Milvus with hybrid search

Members present: Agata Kaczmarek, Mateusz Stączek

- research on Milvus with hybrid search - unsuccessful tries of following the tutorial with our data,
- looking for databases that support hybrid search,
- decision to change the database.

### 2024-02-10: Research about hybrid search and pipeline improvements

Members present: Agata Kaczmarek, Mateusz Stączek

- research on hybrid search - found `EnsembleRetriever`, seems the way to of a single database with hybrid search,
- comparing alternatives supported by Langchain: Elasticsearch BM25 vs BM25, and vector databases,
- thinking about improvements - compressing documents, automated creation of metadata filters, improving prompt.

### 2024-02-16: Meeting to solve problems with implementation

Members present: Agata Kaczmarek, Mateusz Stączek

- fixed setting up local environment - langchain had some problems with specific versions,
- pair programming.

### 2024-02-19: Preparatory meeting before update on the project

Members present: Agata Kaczmarek, Mateusz Stączek

- critical review of the current solution - noticed that we should include more data from the xlsx than only PMID, title and abstract,
- summarized what is working - baseline pipeline with LanceDB and BM25 with Llama2 7B on Colab with GPU,
- summarized what is not working - running it locally in Docker without GPU,
- listed problems, questions and ideas for improvements.
 

### 2024-02-20: Meeting about update on the project

Members present: All team members

- update about critical review of the current solution,
- discussion about listed problems, questions and ideas for improvements,
- division of further work: solve problems with implementation - Agata and Mateusz; evaluation - Jan; template of the documentation.md - Pranjal; writing documentation.md - all team members (division by who did what in the project),
- next team meeting: 26th February

### 2024-02-25: Meeting to solve problems with implementation

Members present: Agata Kaczmarek, Mateusz Stączek

- pair programming.

### 2024-02-26: Implementation and discussions about evaluation

Members present: Agata Kaczmarek, Mateusz Stączek, Jan Smoleń

- pair programming,
- discussions about evaluation process.

  
### 2024-03-01: Discussions about documentation

Members present: Agata Kaczmarek, Mateusz Stączek

- planning of the documentation,
- planning the final structure of the GitHub,
- checking if the current soultion meets all the criterias from the task description.

### 2024-03-02: Documentation and work on final solution

Members present: Agata Kaczmarek, Mateusz Stączek

- pair programming and writing the documentation.
