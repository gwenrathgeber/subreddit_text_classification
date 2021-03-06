# Script to run our text preprocessing on .csv of cleaned data and return final modeling dataframe

# Imports
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import time 

# Data
df = pd.read_csv('../data/cleaned_subreddit_data.csv')

# Target Columns
columns = ['title','selftext']

# Verify no NAs in data
df = df.dropna()

def tokenize(column):
    df[column] = [word_tokenize(str(text)) for text in df[column]]
    return df[column]

def lemmatize(tokenized_column):
    lemmatizer = WordNetLemmatizer()
    df[tokenized_column] = [' '.join([lemmatizer.lemmatize(word) for word in text]) for text in df[tokenized_column]]
    return df[tokenized_column]

# def stem(lemmatized_column):
#     stemmer = PorterStemmer()
#     df[lemmatized_column] = [' '.join([stemmer.stem(word) for word in text]) for text in df[lemmatized_column]]
#     return df[lemmatized_column]

def main():
    for column in columns:
        print(f'Tokenizing {column}')
        start_time = time.perf_counter()
        df[column] = tokenize(column)
        print(f'{time.perf_counter() - start_time} elapsed')
        print(f'Lemmatizing {column}')
        df[column] = lemmatize(column)
        print(f'{time.perf_counter() - start_time} elapsed')
        # print(f'Stemming {column} and rejoining.')
        # df[column] = stem(column)
        print(f'Total time elapsed on column {column}: {time.perf_counter() - start_time}')
    
    print(f'Total preprocessing time: {time.perf_counter() - start_time}')
    df.to_csv('../data/preprocessed_subreddit_data.csv', index=False)

if __name__ == "__main__":
    main()