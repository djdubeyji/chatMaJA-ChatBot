# Data acquisition

Here we describe the process of acquiring the data (abstracts) from PubMed:

1. Download IDs of articles from PubMed
2. Download data for each article from PubMed
3. Create a CSV with necessary data

To update the data to include also the more recent articles, one would have to repeat the process described below, but with different time periods.

## 1 - `PM-IDs` folder

This folder contains Excel lists of PubMed IDs of articles found in PubMed with query "intelligence[Title/Abstract]" that were published between 2013 and November 26th 2023 ([see commit](https://github.com/mstaczek/QAsystem-INLPT-WS2023/commit/d2ebd9596c520deba1ef9cdd234e5189d77db84d)). 

> PubMed allows to download up to 10000 IDs at once. This is why we downloaded data in `batches` of up to 10000.

For years such as 2022 where there were over 10000 articles matching our filters, IDs were downloaded twice - once from the beginning of the year going forward, and once from the end going backwards, which created overlap and duplicated IDs. This way, we downloaded all possible IDs for each year. Should there be more than 20000 articles in a year, we would have to acquire IDs in a different manner. As a last step, all IDs were added to the first file (`pmid-intelligen-set-2013-2017.xlsx` has now 5 columns) and duplicated IDs were removed. 


| Period          | Number of IDs | File Name                               |
|-----------------|---------------|-----------------------------------------|
| 2013-2017       | 56933*        | pmid-intelligen-set-2013-2017.xlsx      |
| 2018-2019       | 7141          | pmid-intelligen-set2018-2019.xlsx       |
| 2020            | 7316          | pmid-intelligen-set2020.xlsx            |
| 2021 part 1     | 10000         | pmid-intelligen-set2021.xlsx            |
| 2021 part 2     | 10000         | pmid-intelligen-set-2021-2.xlsx         |
| 2022 part 1     | 10000         | pmid-intelligen-set-2022.xlsx           |
| 2022 part 2     | 10000         | pmid-intelligen-set-2022-2.xlsx         |
| 2023 part 1     | 10000         | pmid-intelligen-set2023.xlsx            |
| 2023 part 2     | 10000         | pmid-intelligen-set-2023-2.xlsx         |

\* - IDs from all files were added to the first file: `pmid-intelligen-set-2013-2017.xlsx`

## 2 - `Raw data` folder

This folder contains all possible data for each of the articles, also as Excel spreadsheets. Number of files (5 files) and their lengths correspond to number of columns and rows in each column in a file with PM-IDs called `pmid-intelligen-set-2013-2017.xlsx` where all IDs were added.

To download data, an online tool available at [pubmed2xl.com/xlsx](https://pubmed2xl.com/xlsx/) has been used to download data for each of the IDs. 

| File         | Number of Articles | File Name                                      |
|--------------|--------------------|------------------------------------------------|
| Excel file 1 | 9999               | 2d94316c-88aa-11ee-a672-d21848e7cc81.xlsx     |
| Excel file 2 | 10000              | 9c9d478e-88a9-11ee-8cf3-d21848e7cc81.xlsx     |
| Excel file 3 | 10000              | 49622e90-88a9-11ee-b077-d21848e7cc81.xlsx     |
| Excel file 4 | 16935              | d76c73c4-88a6-11ee-9309-d21848e7cc81.xlsx     |
| Excel file 5 | 9999               | 2d94316c-88aa-11ee-a672-d21848e7cc81.xlsx     |


## 3 - `Data extracted` folder

This folder contains a single, big (~93 MB) CSV file with 2 columns: Title and Abstract. This is the entrypoint for later stages of the project.

| File            | Number of Articles | File Name        |
|-----------------|--------------------|------------------|
| CSV file        | 56933              | MasterSheet.txt  |