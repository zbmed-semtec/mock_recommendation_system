# Input Data

The scripts in this folder are used to create the input files for the Mock Recommendation System. The [`get_text.py`](./code/get_text.py) script is used for creating the 'relish_text.jsonl' file which consists of the PMIDs, Titles and Abstracts of the all the documents within the RELISH Corpus. Whereas, the [`get_recoms.py`](./code/get_recoms.py) script is used for creating the 'relish_recoms.jsonl' file which consists of pairwise document relevance assessments along with a recommendation number alloted based on as they appear within the RELISH Corpus.  

**NOTE:** Before executing the scripts, make sure to download both these files and place them within the `/code` folder.
+ [RELISH Text TSV](https://drive.google.com/file/d/1L-4spewLWN7jMzA5uTiBNTHhPl926j64/view)
+ [RELISH Relevance Assessment TSV](https://github.com/zbmed-semtec/relish-preprocessing/blob/main/data/output/relish-ground-truth/RELISH.tsv)


## Generating the 'relish_text.jsonl' file

If you are within the code folder, please execute the following script.

```
python3 get_text.py --input RELISH_documents_2022628.tsv --output relish_text.jsonl
```

## Generating the 'relish_recoms.jsonl' file

If you are within the code folder, please execute the following script.

```
python3 get_recoms.py --input RELISH.tsv --output relish_recoms.jsonl
```