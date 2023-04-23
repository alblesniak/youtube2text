import os
import math
import spacy
import pandas as pd
from collections import Counter
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from tqdm import tqdm
import shutil
import tempfile
import argparse

# Combine multiple directories into a temporary directory
def combine_directories(directories):
    combined_dir = tempfile.mkdtemp()
    for directory in directories:
        for file in os.listdir(directory):
            shutil.copy(os.path.join(directory, file), combined_dir)
    return combined_dir

# Compute the log-likelihood value for a given n-gram
def compute_log_likelihood(o_11, o_21, corpus_c, corpus_r):
    e_11 = (corpus_c * (o_11 + o_21)) / (corpus_c + corpus_r)
    e_21 = (corpus_r * (o_11 + o_21)) / (corpus_c + corpus_r)
    try:
        log_likelihood = 2 * ((o_11 * math.log(o_11 / e_11)) + (o_21 * math.log(o_21 / e_21)))
    except:
        log_likelihood = 0
    return log_likelihood

# Process and tokenize text files in a given directory and extract metadata
def process_files_and_extract_metadata(directory):
    nlp = spacy.load("pl_core_news_lg")
    texts = []
    metadata = []

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            text = f.read()
            doc = nlp(text)

            lemmatized = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
            texts.append(lemmatized)

            tokens = [token for token in doc if not token.is_punct and not token.is_stop]
            metadata.append((file, len(tokens), len(lemmatized)))

    return texts, metadata

# Extract bigrams and trigrams from the processed texts
def extract_ngrams(texts, min_count=5, threshold=10):
    bigram_model = Phrases(texts, min_count=min_count, threshold=threshold)
    trigram_model = Phrases(bigram_model[texts], threshold=threshold)

    bigram_phraser = Phraser(bigram_model)
    trigram_phraser = Phraser(trigram_model)

    ngram_texts = [trigram_phraser[bigram_phraser[text]] for text in texts]
    return ngram_texts

# Calculate the log-likelihood values for all n-grams in two corpora
def analyze_log_likelihood(corpus_c, corpus_r):
    corpus_c_ngrams = [ngram for text in corpus_c for ngram in text]
    corpus_r_ngrams = [ngram for text in corpus_r for ngram in text]

    corpus_c_counts = Counter(corpus_c_ngrams)
    corpus_r_counts = Counter(corpus_r_ngrams)

    all_ngrams = set(corpus_c_counts.keys()) | set(corpus_r_counts.keys())
    results = []

    for ngram in tqdm(all_ngrams, desc="Analyzing n-grams"):
        o_11 = corpus_c_counts[ngram]
        o_21 = corpus_r_counts[ngram]

        log_likelihood = compute_log_likelihood(o_11, o_21, len(corpus_c_ngrams), len(corpus_r_ngrams))
        
        occurrences_A = o_11
        occurrences_per_1000_A = (o_11 / len(corpus_c_ngrams)) * 1000
        occurrences_B = o_21
        occurrences_per_1000_B = (o_21 / len(corpus_r_ngrams)) * 1000
        
        results.append((ngram, log_likelihood, occurrences_A, occurrences_per_1000_A, occurrences_B, occurrences_per_1000_B))
    return results

def separate_ngrams_by_corpus(results_df):
    corpus_A_ngrams = results_df[results_df['occurrences_per_1000_A'] > results_df['occurrences_per_1000_B']]
    corpus_B_ngrams = results_df[results_df['occurrences_per_1000_A'] < results_df['occurrences_per_1000_B']]
    
    return corpus_A_ngrams, corpus_B_ngrams

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze n-grams in two corpora.')
    parser.add_argument('corpus_a_name', type=str, help='The name of the first corpus')
    parser.add_argument('corpus_b_name', type=str, help='The name of the second corpus')
    args = parser.parse_args()

    corpus_a_name = args.corpus_a_name
    corpus_b_name = args.corpus_b_name
    
    playlist_names = {
        'szustak': ['CNN', 'Wstawaki'],
        'zieliński': ['Kwadransik ze Słowem'],
        'kamiński': ['Gdy zstępuje Duch Święty - seria 1', 'Gdy zstępuje Duch Święty - seria 2', 'Kazania Biskupa 2020']
    }

    # Check if the provided parameters exist as keys in the dictionary
    if corpus_a_name not in playlist_names:
        raise ValueError(f"Invalid value for 'corpus_a_name': {corpus_a_name}. Must be one of {list(playlist_names.keys())}.")

    if corpus_b_name not in playlist_names:
        raise ValueError(f"Invalid value for 'corpus_b_name': {corpus_b_name}. Must be one of {list(playlist_names.keys())}.")


    dir_transcripts = os.path.join(os.getcwd(), 'transcripts')

    # Get the folder names for each corpus
    corpus_a_dirs = [os.path.join(dir_transcripts, folder) for folder in playlist_names[corpus_a_name]]
    corpus_b_dirs = [os.path.join(dir_transcripts, folder) for folder in playlist_names[corpus_b_name]]

    # Combine directories for corpus A
    print(f"Combining directories for corpus {corpus_a_name}...")
    combined_directory = combine_directories(corpus_a_dirs)

    # Process text files and extract metadata for corpus A
    print(f"Processing text files and extracting metadata for corpus {corpus_a_name}...")
    corpus_c_texts, corpus_A_metadata = process_files_and_extract_metadata(combined_directory)

    # Combine directories for corpus B
    print(f"Combining directories for corpus {corpus_b_name}...")
    combined_directory = combine_directories(corpus_b_dirs)

    # Process text files and extract metadata for corpus B
    print(f"Processing text files and extracting metadata for corpus {corpus_b_name}...")
    corpus_r_texts, corpus_B_metadata = process_files_and_extract_metadata(combined_directory)

    print(f"Extracting n-grams for corpus {corpus_a_name}...")
    corpus_c_ngrams = extract_ngrams(corpus_c_texts)

    print(f"Extracting n-grams for corpus {corpus_b_name}...")
    corpus_r_ngrams = extract_ngrams(corpus_r_texts)

    print("Analyzing log-likelihood for n-grams in both corpora...")
    log_likelihood_results = analyze_log_likelihood(corpus_c_ngrams, corpus_r_ngrams)

    df = pd.DataFrame(log_likelihood_results, columns=['keyword', 'log_likelihood', f'occurrences_{corpus_a_name}', f'occurrences_per_1000_{corpus_a_name}', f'occurrences_{corpus_b_name}', f'occurrences_per_1000_{corpus_b_name}'])
    df = df.sort_values(by='log_likelihood', ascending=False)

    # Separate n-grams based on occurrences per 1,000 words
    corpus_A_ngrams, corpus_B_ngrams = separate_ngrams_by_corpus(df)

    # Create the results directory if it doesn't exist
    results_dir = os.path.join(os.getcwd(), 'results', f'{corpus_a_name}_{corpus_b_name}')
    os.makedirs(results_dir, exist_ok=True)

    # Save the results to separate sheets in an Excel file
    excel_path = os.path.join(results_dir, "log_likelihood_results.xlsx")
    with pd.ExcelWriter(excel_path) as writer:
        df.to_excel(writer, sheet_name='All_keywords', index=False)
        corpus_A_ngrams.to_excel(writer, sheet_name=f'corpus_{corpus_a_name}', index=False)
        corpus_B_ngrams.to_excel(writer, sheet_name=f'corpus_{corpus_b_name}', index=False)

    # Save metadata to a new Excel file
    print("Saving metadata to a separate Excel file...")
    metadata_df_A = pd.DataFrame(corpus_A_metadata, columns=['title', 'tokens', 'lemmas'])
    metadata_df_B = pd.DataFrame(corpus_B_metadata, columns=['title', 'tokens', 'lemmas'])

    metadata_excel_path = os.path.join(results_dir, "corpora_metadata.xlsx")
    with pd.ExcelWriter(metadata_excel_path) as writer:
        metadata_df_A.to_excel(writer, sheet_name=f'corpus_{corpus_a_name}', index=False)
        metadata_df_B.to_excel(writer, sheet_name=f'corpus_{corpus_b_name}', index=False)

    print("Analysis complete.")



