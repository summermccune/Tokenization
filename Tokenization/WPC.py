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
