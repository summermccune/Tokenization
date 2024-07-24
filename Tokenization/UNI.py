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

    UNI_tokenizer = train_tokenizer('UNI')

    #divide dataset into halves
    half_index = len(dataset)//2
    first_half = dataset.iloc[:half_index].copy()
    second_half = dataset.iloc[half_index:].copy()

    #encode
    UNI_tokens_first = encode(UNI_tokenizer, first_half)
    UNI_tokens_second = encode(UNI_tokenizer, second_half)

    #combine the halves
    joined_list = UNI_tokens_first + UNI_tokens_second

    #put into df
    UNI_df = pd.DataFrame(columns = ['Opcodes', 'Label'])
    UNI_df['Opcodes'] = joined_list
    UNI_df['Label'] = dataset['Label']

    #save as pkl
    UNI_df.to_pickle('TokenizedData/UNI_df.pkl')

if __name__ == "__main__":
    main()


