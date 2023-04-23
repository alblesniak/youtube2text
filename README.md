The script `calc_loglikelihood.py` performs a comparative analysis of keywords and n-grams (bigrams and trigrams) from two different corpora of text files. The main steps are:

- Combine multiple directories containing text files for each corpus.
- Process and tokenize the text files using the spacy library and extract metadata (file name, number of tokens, and number of lemmas).
- Extract bigrams and trigrams from the processed texts using the gensim library.
- Calculate the log-likelihood values for all n-grams in both corpora, which is a measure of how much more likely an n-gram is to appear in one corpus compared to the other.
- Separate the n-grams based on their occurrences per 1,000 words in each corpus.
- Save the results and metadata to Excel files.