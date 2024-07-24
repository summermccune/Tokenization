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
    
    SPC_tokenizer = train_tokenizer('SPC')

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

    #divide dataset into halves
    half_index = len(dataset)//2
    first_half = dataset.iloc[:half_index].copy()
    second_half = dataset.iloc[half_index:].copy()

    #encoding first half and saving
    SPC_tokens_first = encode(SPC_tokenizer, first_half)
    #save first half
    with open('TokenizedData/SPC_tokens_first.pkl', 'wb') as f:
        pickle.dump(SPC_tokens_first, f)

    #encoding second half and saving
    SPC_tokens_second = encode(SPC_tokenizer, second_half)
    #second half
    with open('TokenizedData/SPC_tokens_second.pkl', 'wb') as f:
        pickle.dump(SPC_tokens_second, f)

    #separate code for reading after saving each half
    SPC_tokens_first = pd.read_pickle('TokenizedData/SPC_tokens_first.pkl')
    SPC_tokens_second = pd.read_pickle('TokenizedData/SPC_tokens_second.pkl')

    #combine the halves
    joined_list = SPC_tokens_first + SPC_tokens_second

    #put into df
    SPC_df = pd.DataFrame(columns = ['Opcodes', 'Label'])
    SPC_df['Opcodes'] = joined_list
    SPC_df['Label'] = dataset['Label']

    #save as pkl
    SPC_df.to_pickle('TokenizedData/SPC_df.pkl')
