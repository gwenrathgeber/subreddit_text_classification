# This script accepts the raw API response .csv and outputs one with NAs and deleted posts removed,
# plus any HTML fragments removed 

# Imports
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import re
import string


# Ignore warnings
warnings.filterwarnings("ignore")

# Import Data
df = pd.read_csv('../data/subreddit_data.csv')

print('Number of Entries per subreddit pre-cleaning:')
print(df['subreddit'].value_counts())

# Select the columns we're interested in modeling
columns = ['id','selftext','author','title','subreddit']

df = df[columns]

# # Just in case there are any HTML impurities in the raw data, we will use BeautifulSoup 
# # to clean the text columns
# print('Removing html...')

# for col in df:
#     if df[col].dtypes == 'O':
#         print(f'Removing html from {col}')
#         for item in df.index:
#             df.loc[item,col] = BeautifulSoup(df.loc[item,col]).get_text()

# Drop posts without selftext
df = (df[~df['selftext'].isna()])

# Drop posts without titles
df = (df[~df['title'].isna()])

# Drop posts where text has been removed or deleted by users/moderators
df = df[df['selftext']!='[removed]']
df = df[df['selftext']!='[deleted]']
df = df[~df['selftext'].str.startswith('[removed]')]
df = df[~df['selftext'].str.startswith('[deleted]')]


df = df.drop(df[df['author'] == 'AutoModerator'].index)
df = df[~df['selftext'].isna()]
df.reset_index(inplace=True)

# Reset index of results because it is annoying 
df.reset_index(drop=True, inplace=True)

# Remove URLS from selftext and title columns
print('Removing URLs from posts...')
df['selftext'] = [re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) for text in df['selftext']]

print('Removing URLs from titles...')
df['title'] = [re.sub(r'http\S+', '', text) for text in df['selftext']]

# Remove certain reddit markdown issues from title and selftext column
print('Removing markdown issues...')
df['selftext'] = df['selftext'].str.replace('x200B','')
df.loc[:,'selftext'] = df['selftext'].str.replace('\n',' ')

# Remove punctuation manually:
print('Removing punctuation...')
string.punctuation += '’'
df['selftext'] = ["".join(l for l in s if l not in string.punctuation) for s in df['selftext']]
df['title'] = ["".join(l for l in s if l not in string.punctuation) for s in df['title']]

# Drop posts without selftext
df = (df[~df['selftext'].isna()])

# Drop posts without titles
df = (df[~df['title'].isna()])

# Drop posts where text has been removed or deleted by users/moderators
df = df[df['selftext']!='[removed]']
df = df[df['selftext']!='[deleted]']
df = df[~df['selftext'].str.startswith('[removed]')]
df = df[~df['selftext'].str.startswith('[deleted]')]


df = df.drop(df[df['author'] == 'AutoModerator'].index)
df = df[~df['selftext'].isna()]
df.reset_index(inplace=True)

# Reset index of results because it is annoying 
df.reset_index(drop=True, inplace=True)

print('\nNumber of Entries per subreddit post-cleaning:')
print(df['subreddit'].value_counts())

print('Writing results to file...')
df.to_csv('../data/cleaned_subreddit_data.csv', index=False)
print('Cleaning completed.')