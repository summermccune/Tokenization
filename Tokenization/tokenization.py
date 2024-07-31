import pandas as pd
from tokenize import Whitespace
import re
from nltk.util import bigrams
from tokenizers import Tokenizer, SentencePieceBPETokenizer
from tokenizers.models import BPE, WordPiece, Unigram
from tokenizers.trainers import BpeTrainer, WordPieceTrainer, UnigramTrainer
import pickle
from collections import Counter
from tokenizers.pre_tokenizers import Whitespace

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

def batch_iterator(data, batch_size):
  for i in range(0, len(data), batch_size):
      yield data['Opcodes'][i : i + batch_size]

def count_unigrams(df, c):
  """
  Updates the count of unigrams in order to get TOP31
  """
  for row in df['Opcodes']:
     data = row.split()
     c.update(data)

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

def prepare_tokenizer_trainer(alg, v_size, unk_token, spl_tokens):
    """
    Prepares the tokenizer and trainer with unknown & special tokens
    """
    if alg == 'BPE':
        tokenizer = Tokenizer(BPE(unk_token = unk_token))
        trainer = BpeTrainer(special_tokens = spl_tokens, vocab_size=v_size)
    elif alg == 'UNI':
        tokenizer = Tokenizer(Unigram())
        trainer = UnigramTrainer(unk_token= unk_token, special_tokens = spl_tokens, vocab_size=v_size)
    elif alg == 'WPC':
        tokenizer = Tokenizer(WordPiece(unk_token = unk_token))
        trainer = WordPieceTrainer(special_tokens = spl_tokens, vocab_size=v_size)

    tokenizer.pre_tokenizer = Whitespace()
    return tokenizer, trainer

def train_tokenizer(alg, train_data, v_size, unk_token, spl_tokens, batch_size):
    """
    Trains the tokenizer
    """
    if (alg == 'BPE' or alg == 'UNI' or alg == 'WPC'):
      tokenizer, trainer = prepare_tokenizer_trainer(alg, v_size, unk_token, spl_tokens)
      tokenizer.train_from_iterator(batch_iterator(train_data, batch_size), trainer=trainer)
      return tokenizer
    elif alg == 'SPC':
      tokenizer = SentencePieceBPETokenizer()
      tokenizer.train_from_iterator(batch_iterator(train_data, batch_size),vocab_size=v_size)
    return tokenizer

def encode(tokenizer, df):
  encode = tokenizer.encode_batch(df['Opcodes'])
  tokens = [encoding.tokens for encoding in encode]
  return tokens

def single_words(train, test):
    #set up values
    size = 31

    #make new df with opcode and malware as columns
    SW_train = train.copy()
    SW_test = test.copy()

    #counting opcodes for data cleaning
    countTotal = Counter()
    count_unigrams(SW_train, countTotal)

    #list for most common opcodes
    total_count = countTotal.most_common(size)
    countList = [x[0] for x in total_count]
    print(countList)
    del countTotal

    #store cleaned rows
    train_rows = removeNonVocab(countList, SW_train['Opcodes'])
    test_rows = removeNonVocab(countList, SW_test['Opcodes'])
    del countList
    SW_train['Opcodes'] = train_rows
    SW_test['Opcodes'] = test_rows
    del train_rows
    del test_rows

    #convert tokenized dataframe to pkl
    SW_train.to_pickle('TokenizedData/SW_train.pkl')
    SW_test.to_pickle('TokenizedData/SW_test.pkl')
    del SW_train, SW_test

def word_pairs(train, test):
    #set up values
    size = 30

    #make new df as copy to avoid overwriting original
    WP_train = train.copy()
    WP_test = test.copy()

    #counting bigrams for data cleaning
    countTotal = Counter()
    count_bigrams(WP_train, countTotal)

    #list for most common bigrams
    total_count = countTotal.most_common(size)
    countList = [x[0] for x in total_count]
    print(countList)
    del countTotal

    #store cleaned rows
    train_rows = removeNonVocab(countList, WP_train['Opcodes'])
    test_rows = removeNonVocab(countList, WP_test['Opcodes'])
    del countList

    #make new df for bigrams
    WP_train = pd.DataFrame(columns = ['Opcodes', 'Label'])
    WP_test = pd.DataFrame(columns = ['Opcodes', 'Label'])
    WP_train['Opcodes'] = train_rows
    del train_rows
    WP_train['Label'] = train['Label']
    WP_test['Opcodes'] = test_rows
    del test_rows
    WP_test['Label'] = test['Label']

    #save as pkl
    WP_train.to_pickle('TokenizedData/WP_train.pkl')
    WP_test.to_pickle('TokenizedData/WP_test.pkl')
    del WP_train,WP_test

def BPE(train, test):
    #set up values
    batch_size = 1000
    unk_token = "<UNK>"
    spl_tokens = ["<UNK>", "<SEP>", "<MASK>", "<CLS>"]
    v_size = 1000
    BPE_tokenizer = train_tokenizer('BPE', train, v_size, unk_token, spl_tokens, batch_size)
    BPE_tokenizer.save("Tokenizers/BPE-trained.json")

    BPE_train = train.copy()
    BPE_test = test.copy()
    BPE_train_tokens = encode(BPE_tokenizer, BPE_train[:2450]) + encode(BPE_tokenizer[2450:4900])
    BPE_test_tokens = encode(BPE_tokenizer, BPE_test)
    del BPE_tokenizer
    BPE_train = pd.DataFrame(columns = ['Opcodes', 'Label'])
    BPE_test = pd.DataFrame(columns = ['Opcodes', 'Label'])
    BPE_train['Opcodes'] = BPE_train_tokens
    del BPE_train_tokens
    BPE_train['Label'] = train['Label']
    BPE_test['Opcodes'] = BPE_test_tokens
    del BPE_test_tokens
    BPE_test['Label'] = test['Label']

    #save as pkl
    BPE_train.to_pickle('TokenizedData/BPE_train.pkl')
    BPE_test.to_pickle('TokenizedData/BPE_test.pkl')
    del BPE_train,BPE_test

def WPC(train, test):
    #set up values
    batch_size = 1000
    unk_token = "<UNK>"
    spl_tokens = ["<UNK>", "<SEP>", "<MASK>", "<CLS>"]
    v_size = 500
    
    WPC_tokenizer = train_tokenizer('WPC', train, v_size, unk_token, spl_tokens, batch_size)
    WPC_tokenizer.save("Tokenizers/WPC-trained.json")

    WPC_train = train.copy()
    WPC_test = test.copy()
    WPC_train_tokens = encode(WPC_tokenizer, WPC_train[:2450]) + encode(WPC_tokenizer[2450:4900])
    WPC_test_tokens = encode(WPC_tokenizer, WPC_test)
    del WPC_tokenizer
    WPC_train = pd.DataFrame(columns = ['Opcodes', 'Label'])
    WPC_test = pd.DataFrame(columns = ['Opcodes', 'Label'])
    WPC_train['Opcodes'] = WPC_train_tokens
    del WPC_train_tokens
    WPC_train['Label'] = train['Label']
    WPC_test['Opcodes'] = WPC_test_tokens
    del WPC_test_tokens
    WPC_test['Label'] = test['Label']

    #save as pkl
    WPC_train.to_pickle('TokenizedData/WPC_train.pkl')
    WPC_test.to_pickle('TokenizedData/WPC_test.pkl')
    del WPC_train
    del WPC_test

def SPC(train, test):
   #set up values
    batch_size = 1000
    unk_token = "<UNK>"
    spl_tokens = ["<UNK>", "<SEP>", "<MASK>", "<CLS>"]
    v_size = 500
    SPC_tokenizer = train_tokenizer('SPC', train, v_size, unk_token, spl_tokens, batch_size)
    SPC_tokenizer.save("Tokenizers/SPC-trained.json")

    SPC_train = train.copy()
    SPC_test = test.copy()
    SPC_train_tokens = encode(SPC_tokenizer, SPC_train[:2450]) + encode(SPC_tokenizer[2450:4900])
    SPC_test_tokens = encode(SPC_tokenizer, SPC_test)
    del SPC_tokenizer
    SPC_train = pd.DataFrame(columns = ['Opcodes', 'Label'])
    SPC_test = pd.DataFrame(columns = ['Opcodes', 'Label'])
    SPC_train['Opcodes'] = SPC_train_tokens
    del SPC_train_tokens
    SPC_train['Label'] = train['Label']
    SPC_test['Opcodes'] = SPC_test_tokens
    del SPC_test_tokens
    SPC_test['Label'] = test['Label']

    #save as pkl
    SPC_train.to_pickle('TokenizedData/SPC_train.pkl')
    SPC_test.to_pickle('TokenizedData/SPC_test.pkl')
    del SPC_train, SPC_test

def UNI(train, test):
   #set up values
    batch_size = 1000
    unk_token = "<UNK>"
    spl_tokens = ["<UNK>", "<SEP>", "<MASK>", "<CLS>"]
    v_size = 500
    UNI_tokenizer = train_tokenizer('UNI', train, v_size, unk_token, spl_tokens, batch_size)
    UNI_tokenizer.save("Tokenizers/UNI-trained.json")

    UNI_train = train.copy()
    UNI_test = test.copy()
    UNI_train_tokens = encode(UNI_tokenizer, UNI_train[:2450]) + encode(UNI_tokenizer[2450:4900])
    UNI_test_tokens = encode(UNI_tokenizer, UNI_test)
    del UNI_tokenizer
    UNI_train = pd.DataFrame(columns = ['Opcodes', 'Label'])
    UNI_test = pd.DataFrame(columns = ['Opcodes', 'Label'])
    UNI_train['Opcodes'] = UNI_train_tokens
    del UNI_train_tokens
    UNI_train['Label'] = train['Label']
    UNI_test['Opcodes'] = UNI_test_tokens
    del UNI_test_tokens
    UNI_test['Label'] = test['Label']

    #save as pkl
    UNI_train.to_pickle('TokenizedData/UNI_train.pkl')
    UNI_test.to_pickle('TokenizedData/UNI_test.pkl')
    del UNI_train, UNI_test

def main():
    #read in the data
    print("Reading in families")
    FakeRean = pd.read_csv('Families/FakeRean.csv')
    OnLineGames = pd.read_csv('Families/OnLineGames.csv')
    Vobfus = pd.read_csv('Families/Vobfus.csv')
    Winwebsec = pd.read_csv('Families/Winwebsec.csv')
    BHO = pd.read_csv('Families/BHO.csv')
    CeeInject = pd.read_csv('Families/CeeInject.csv')
    Renos = pd.read_csv('Families/Renos.csv')

    #make csvs to df with train and test columns
    dataset = pd.concat([FakeRean, OnLineGames, Vobfus, Winwebsec, BHO, CeeInject, Renos], ignore_index=True)

    del FakeRean, Winwebsec, OnLineGames, Vobfus, BHO, CeeInject, Renos

    # Split the original DataFrame into training (70%) and testing (30%) sets
    print("Splitting data into train and test")
    train = dataset.sample(frac=0.7, random_state=42)
    test = dataset.drop(train.index)

    del dataset

    #drop first column
    train = train.iloc[:, 1:]
    test = test.iloc[:, 1:]

    #SINGLE WORDS - SW
    print("Starting SW")
    single_words(train, test)
    print("Finished SW")

    #WORD PAIRS - WP
    print("Starting WP")
    word_pairs(train, test)
    print("Finished WP")

    #BYTE PAIR ENCODING - BPE
    print("Starting BPE")
    BPE(train,test)
    print("Finished BPE")

    #WORD PIECE - WPC
    print("Starting WPC")
    WPC(train,test)
    print("Finished WPC")

    #SENTENCE PIECE - SPC
    print("Starting SPC")
    SPC(train,test)
    print("Finished SPC")

    #UNIGRAM - UNI
    print("Starting UNI")
    UNI(train,test)
    print("Finished UNI")

if __name__ == "__main__":
    main()
