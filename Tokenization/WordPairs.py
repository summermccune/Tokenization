import pandas as pd
from collections import Counter

def count_bigrams(df, c):
  """
  Updates the count of bigrams for word pair tokenization. 
  Returns a list of bigrams in order to create a new dataframe with bigrams
  """
  bigrams_list = []
  for row in df['Opcodes']:
     data = row.split()
     bigrms = list(bigrams(data))
     #make bigrams each their own string
     bigrms = [f"{first}_{second}" for first, second in bigrms]
     bigrams_list.append(' '.join(bigrms))
     c.update(bigrms)
  return bigrams_list

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
    # Load your dataset
    dataset = pd.read_pickle('path_to_your_dataset.pkl')

    # Make new df as copy
    word_pairs_df = dataset.copy()

    # Counting bigrams for data cleaning
    countTotal = Counter()
    bigram_list = count_bigrams(word_pairs_df, countTotal)

    # List for most common bigrams
    total_count = countTotal.most_common(31)
    countList = [x[0] for x in total_count]
    print(countList)

    # Make new df for bigrams
    wp_df = pd.DataFrame(columns=['Opcodes', 'Label'])
    wp_df['Opcodes'] = bigram_list
    wp_df['Label'] = word_pairs_df['Label']

    # Remove non-vocab bigrams
    rows = removeNonVocab(countList, wp_df['Opcodes'])
    wp_df['Opcodes'] = rows
    wp_df.head()

    # Save the dataframe to a pickle file
    wp_df.to_pickle('TokenizedData/WP_df.pkl')

if __name__ == "__main__":
    main()

