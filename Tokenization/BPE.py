import pandas as pd
from tokenizers import ByteLevelBPETokenizer, SentencePieceBPETokenizer
from collections import Counter

def train_tokenizer(alg):
    """
    Trains the tokenizer
    """
    if (alg == 'BPE' or alg == 'UNI' or alg == 'WPC'):
      tokenizer, trainer = prepare_tokenizer_trainer(alg)
      tokenizer.train_from_iterator(batch_iterator('train'), trainer=trainer)
      return tokenizer
    elif alg == 'BBPE':
      tokenizer = ByteLevelBPETokenizer()
      tokenizer.train_from_iterator(batch_iterator('train'),vocab_size=v_size)
    elif alg == 'SPC':
      tokenizer = SentencePieceBPETokenizer()
      tokenizer.train_from_iterator(batch_iterator('train'),vocab_size=v_size)
    return tokenizer

def encode(tokenizer, df):
  encode = tokenizer.encode_batch(df['Opcodes'])
  tokens = [encoding.tokens for encoding in encode]
  return tokens

def main():
  #set up values
  batch_size = 1000
  unk_token = "<UNK>"
  spl_tokens = ["<UNK>", "<SEP>", "<MASK>", "<CLS>"]
  v_size = 100

  BPE_tokenizer = train_tokenizer('BPE')

  #divide dataset into halves - helps to avoid consuming too much memory
  half_index = len(dataset)//2
  first_half = dataset.iloc[:half_index].copy()
  second_half = dataset.iloc[half_index:].copy()

  BPE_tokens_first = encode(BPE_tokenizer, first_half)

  BPE_tokens_second = encode(BPE_tokenizer, second_half)

  #combine the two lists
  joined_list = BPE_tokens_first + BPE_tokens_second

  #put into a dataframe
  BPE_df = pd.DataFrame(columns = ['Opcodes', 'Label'])
  BPE_df['Opcodes'] = joined_list
  BPE_df['Label'] = dataset['Label']

  #save as pkl
  BPE_df.to_pickle('TokenizedData/BPE_df.pkl')

if __name__ == "__main__":
    main()


