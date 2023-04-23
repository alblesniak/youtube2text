# N-gram Analysis for Two Corpora

This Python script analyzes n-grams in two corpora to find distinctive keywords in each corpus based on the log-likelihood ratio. It processes text files, extracts metadata, identifies bigrams and trigrams, calculates log-likelihood values for all n-grams, and saves the results to an Excel spreadsheet.

## Requirements

- Python 3.x
- spacy
- pandas
- gensim
- tqdm

You can install these packages using pip:

```sh
pip install spacy pandas gensim tqdm
```

Additionally, you need to download the pl_core_news_lg model for spacy:

```sh
python -m spacy download pl_core_news_lg
```

## Usage
Place the text files you want to analyze in folders within the transcripts directory. Modify the `playlist_names` dictionary in the script to include the desired corpora names and associated folder names.
Run the script with the following command:

```sh
python calc_loglikelihood.py corpus_a_name corpus_b_name
```

Replace `corpus_a_name` and `corpus_b_name` with the desired names for the corpora (keys in the playlist_names dictionary).

## Output
The script will save the following results in the results directory:

- An Excel file with n-gram analysis results, including log-likelihood values and occurrences per 1,000 words in each corpus.
- A separate Excel file with metadata (file name, number of tokens, and number of lemmas) for each text file in the corpora.