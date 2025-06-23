# Group 11 - QAsystem-INLPT-WS2023

Repository with our project for NLP with Transformers course. 

### Mentor: Robin Khanna 

| Name | Matriculation Number | GitHub Username | Email Address |
| --- | --- | --- | --- |
| Agata Kaczmarek | 4734079 | [kaczmareka](https://github.com/kaczmareka) | ak.agata.kaczmarek@gmail.com |
| Pranjal Sharma | 4732227 | [djdubeyji](https://github.com/djdubeyji) | pranjal.sharma@stud.uni-heidelberg.de |
| Jan Smoleń |4734263 | [smolenj](https://github.com/smolenj) | jan.smolen@stud.uni-heidelberg.de |
| Mateusz Stączek | 4734410 | [mstaczek](https://github.com/mstaczek/) | mateusz.staczek@stud.uni-heidelberg.de |


### Final project report: [documentation.md](https://github.com/mstaczek/QAsystem-INLPT-WS2023/blob/main/documentation.md)

## Note - This repo uses Git LFS for CSV files

1. Install: https://git-lfs.com/
2. Run `git lfs install`
3. Afterwards, git will automatically download large CSV files from LFS and when adding them to the repository, they will be stored somewhat separately from regular files.

---

# Introduction - chatMaJA
The project focuses on developing a question-answering machine using Large Language Models (LLM) wherein data from PubMed is used containing the keyword "Intelligence" ranging from the year 2013-2023. 

Example of our Gradio UI, streaming model output to the user:

![GIF of Gradio](/img/Gradio.gif)

# Goal
The objective of developing this project is to understand how these LLMs can nowadays be used, to help solve problems of question-answering domain-specific systems.

# [Meeting Notes](/Meetings)
The creators of this project gather and contribute their regular research and learnings to further understand the process and discuss the current and next phases of this project.

# Directory structure:
- `Evaluation` - all files needed to perform an evaluation of the solution and the results of it,
- `Final_solution` - all files needed to run the final version of our solution,
- `Meetings` - meeting notes,
- `Previous_Work` - all files created during previous phases of the project,
- `img` - all images used in the documentation file,
- `presentation_milestone_1.pdf` - file with the presentation we created for milestone 1,
- `documentation.md` - report.

# How to run the project?

All files needed to run our solution can be found in the directory `Final_Solution`. The requirements regarding packages are in the `Final_Solution\requirements.txt` file. In the folder `Final_Solution` there is also a detailed description, of how to run each part of the solution and why.

In general, the final version of our solution includes two UIs, which can be used following the steps from the description below.

## Local Docker + simple Flask (CPU)

This version of UI works on CPU only and is easily available by building and running a standalone Docker container. Below there is a screenshot of working UI. The detailed description about the Docker container can be found in README.md in directory `Docker_Flask_App`.

![Screenshot of UI with sources](/img/Flask_UI.png)

### How to run - with Docker Compose

> **Note:** commands below assume you're in the directory `QAsystem-INLPT-WS2023/Final_Solution/Docker_Flask_App` with the `Dockerfile.base`, `Dockerfile` and `docker-compose.yaml` files.

Build an image with the environment and run docker compose up (which automatically will build an image with the app):

```bash
docker build -t chatmaja_base:v1 -f Dockerfile.base .
docker compose up
```

Then, open http://localhost:5000/. 

#### Two version of CSV files

We prepared 2 datasets - one with chunks from 100 abstracts, and the other with chunks from all abstracts. Loading all chunks to LanceDB requires computing embeddings and takes a very long time on CPU (but works). Either run on a tiny subset of data or download a ready database.

> Options:
> > Update `docker-compose.yml` to use a smaller dataset.
> 
> OR
> 
> > Download and extract a ready LanceDB database `db` folder and place it in the same directory as `docker-compose.yml` - [download link](https://wutwaw-my.sharepoint.com/:f:/g/personal/01151437_pw_edu_pl/EnwtlXrMPApNlDmptSaLnQEBYF_-Bxe7xUs47pqBqQhBYg?e=DCKSDy).

> **For best answers, use all abstracts and download the precomputed LanceDB database.**

>Note: read the readme in `QAsystem-INLPT-WS2023/Final_Solution/Docker_Flask_App` to learn, how to download and add precomputed LanceDB embeddings.

## Gradio notebook (with GPU, on Colab too) - recommended

For better performance and user experience, use UI variant with Gradio in Jupyter Notebook (can be run on Collab with GPU):

Below there is a screenshot of working UI, opened in a separate browser card:

![Screenshot of Gradio](/img/Gradio.png)

and a screenshot of Gradio directly in Colab, with T4 GPU:

![Screenshot of Gradio in Colab](/img/Gradio_Colab.png)


### How to run - Gradio notebook

Simply open the Jupyter notebook `notebook_with_gradio.ipynb` in the `Final_Solution` folder and run all cells. The Gradio UI will be available both in Jupyter Notebook and at http://localhost:7860/.

To run on Colab, you need to upload requirements:
- `QAsystem-INLPT-WS2023\Final_Solution\requirements.txt`

and data, either the whole dataset or a sample:

- sample:  `QAsystem-INLPT-WS2023\Final_Solution\data\preprocessed_data\master_without_embeddings_first_100.csv`,
- whole: `QAsystem-INLPT-WS2023\Final_Solution\data\preprocessed_data\master_without_embeddings_all.csv`.

Remember to set the correct paths to those files (in first cell to install all requirements and later, set `path_to_data_csv` to point to the CSV file).

The Gradio UI will be available both in Colab, and at a printed URL.

#### Gradio - download precomputed LanceDB embeddings

Loading whole dataset to LanceDB takes more than 5 minutes on T4 Colab GPU. We provide a ready LanceDB database `db` folder to download. Extract it to create a folder `db` in the same directory as `notebook_with_gradio.ipynb` - [download link](https://wutwaw-my.sharepoint.com/:f:/g/personal/01151437_pw_edu_pl/EnwtlXrMPApNlDmptSaLnQEBYF_-Bxe7xUs47pqBqQhBYg?e=DCKSDy).

> **For best answers, use all abstracts and download the precomputed LanceDB database.**

--------------------------------
# How the project was created - phases

## [Phase 1](/Previous_Work/Phase1-Planning&DataGathering)
This includes planning work on the project and gathering the raw data that forms the baseline of the project. 

### Data extraction scheme

The process of downloading and preparing data before it is ready to be loaded by our pipeline includes the following steps:

1. Manually download IDs of articles from PubMed (PMIDs) for selected queries and time range:

    Open PubMed -> search for keyword "Intelligence" -> select year range 2013-2023 -> download list of PMIDS. [4]

    Due to PubMed's limitation of the maximum number of IDs downloaded at once, the downloading of all IDs has to be done in parts, for different time ranges. Should there be an overlap in time ranges, deduplication of IDs is also done at this step.

2. Use a website to download `.xlsx` with abstracts and other metadata of articles based on their PubMed ID:

    Go to pubmed2xl.com -> input PMIDs -> download the abstract, title, and all other information for papers with these IDs.

#### Directory structure
Phase1 - Planning&DataGathering 
- DataExtracted - MasterSheet.txt file containing relevant titles abstracts,
- PM-IDs - .xslx files with PubMed articles IDs,
- Raw Data - .xslx files with full information on papers,
- Documentation - project requirements and notes.

## [Phase 2](/Previous_Work)

We have created various versions of WebApp, including Flask and Gradio. The ones chosen for the final solution can be found in the `Final_Solution` directory. In this directory, there is a separate `README.md` file with all the details about our decision.

## [Phase 3](/Previous_Work/Phase3-Embed&Retrieve)

This phase consists of our first approach to constructing a vector database including embedded chunks of the vectors and then retrieving relevant chunks of abstracts based on the query. We decided to try out a Milvus database run locally in a docker container paired with BERT embeddings. For the search, we used cosine similarity.

- `create_new_master_sheet.ipynb` - Create a new master sheet based on the raw data. This time it includes PMID, Title, and Abstract,
- `docker-compose` - docker compose for running Milvus db,
- `embed.ipynb` - Split abstracts into 3-sentence-long chunks, embed them, and store in `/data`. Only the first 100 records were processed for demo purposes,
- `populate_db.ipynb` - Create a collection in Milvus and populate it with vectors read from .csv file with embeddings,
- `retrieve_demo.ipynb` - demonstration of relevant chunk retrieval from vector Milvus database based on string query. 

## [Phase 4](/Previous_Work/Phase4-TBD)

This phase consists of implementing the final solution. During working on it, we understood, that the Milvus database was not a good option for us - due to the lack of possibilities to use hybrid search in our setup. Therefore we decided to use BM25 and LanceDB and combine their results using EnsembleRetriever. During this phase, we also experimented with various data preprocessing settings. We also started working on combining the pipeline with UI and created a CSV file with all our preprocessed data.

## [Phase 5](/Previous_Work/Phase5-evaluation)

During this phase, we worked on experiments and evaluation of the final solution. We also created the plots, which were later used in the documentation of the project.

## Phase 6 

Finally, we worked on the final version of the solution, GitHub appearance, and documentation.
