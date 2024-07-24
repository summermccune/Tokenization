import pandas as pd
from collections import Counter

def count_unigrams(df, c):
  """
  Updates the count of unigrams in order to get TOP31
  """
  for row in df['Opcodes']:
     data = row.split()
     c.update(data)

def removeNonVocab(vocab, series):
  """
  Removes strings not in the top vocab. Returns cleaned rows
  """
  rows = []
  vocab_str = '|'.join(vocab)
  pattern = '\\b((?!\\b( |' + vocab_str + ')\\b).)*\\b'
  for row in series:
    row = re.sub(pattern, '', row)
    row = re.sub(' +', ' ', row)
    rows.append(row.split())
  return rows

def main():
  #make new df with opcode and malware as columns
  TOP31_df = dataset.copy()
  TOP31_df.head()

  #counting opcodes for data cleaning
  countTotal = Counter()
  count_unigrams(TOP31_df, countTotal)
  TOP31_df.head()

  #list for most common opcodes
  total_count = countTotal.most_common(31)
  countList = [x[0] for x in total_count]
  print(countList)

  #store cleaned rows
  rows = removeNonVocab(countList, TOP31_df['Opcodes'])
  TOP31_df['Opcodes'] = rows

  print(TOP31_df.head())
  print(TOP31_df.tail())

  #convert tokenized dataframe to pkl
  TOP31_df.to_pickle('TokenizedData/TOP31.pkl')

if __name__ == "__main__":
    main()
