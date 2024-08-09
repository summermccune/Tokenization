import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from hmmlearn import hmm
from tokenizers import Tokenizer

def opcodes_to_numbers(df, vocab, type):
  #convert opcodes to numbers
  # use LabelEncoder to encode classes (opcode tokens) to numerical values
  le = LabelEncoder().fit(vocab)
  opcodes = [le.transform(tokens) for tokens in df['Opcodes']]
  # find numerical encoding for 'mov', used for B matrix
  if type == 'WP':
    mov = le.transform(['mov_mov'])
  else:
    mov = le.transform(['mov'])
  
  return opcodes, mov

# Function to split dataframe into chunks
def split_dataframe(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def train_hmm_models(opcodes,n_states):
  """
  Trains hmm models for each sample.
  Returns the list of best models.
  """
  hmm_models = []
  for opcode_seq in opcodes:
    opcode_seq = np.array(opcode_seq)
    model = hmm.CategoricalHMM(n_components=n_states, n_iter=100)
    model.fit(opcode_seq.reshape(-1, 1))

    hmm_models.append(model)

  return hmm_models

def b_matrix_to_features(hmm_models, max_feature_length, mov):
  """
  Converts the B matrix from the hmm models into a feature vector for classification.
  """
  hmm2vec_features = []
  for model in hmm_models:
    #determine the hidden state that has the highest probability with respect to the mov opcode
    mov_index = np.argmax(model.emissionprob_[:, mov])

    #deem this to be the first half of the HMM2Vec feature vector, with the other row of the B matrix being the second half of the vector
    sorted_indices = [mov_index, 1 - mov_index]
    sorted_bmatrices = model.emissionprob_[sorted_indices]

    # Flatten the rearranged B matrix to create HMM2Vec feature vector
    feature_vector = sorted_bmatrices.flatten()

    # pad or truncate feature_vector to ensure consistent length
    if len(feature_vector) < max_feature_length:
      feature_vector = np.pad(feature_vector, (0, max_feature_length - len(feature_vector)), mode='constant')
    elif len(feature_vector) > max_feature_length:
      feature_vector = feature_vector[:max_feature_length]

    hmm2vec_features.append(feature_vector)

  return hmm2vec_features

def hmm2vec_embeddings(df, n_states, vocab, type):
  opcodes, mov = opcodes_to_numbers(df, vocab, type)
  hmm_models = train_hmm_models(opcodes, n_states)

  if type == 'SW':
    max_feature_length = 62
  elif type == 'WP':
    max_feature_length = 60
  elif type == 'BPE':
    max_feature_length = 2000
  else:
    max_feature_length = 1000

  hmm2vec_features = b_matrix_to_features(hmm_models, max_feature_length, mov)
  return hmm2vec_features

def main():
  print("STARTING")

  #SINGLE WORDS
  SW_train = pd.read_pickle('TokenizedData/SW_train.pkl')
  
  TOP31_vocab = ['mov', 'push', 'add', 'pop', 'call', 'inc', 'xor', 'lea', 'dec', 'xchg', 'cmp', 'sub', 'or', 'and', 'jmp', 'test', 'adc', 'sbb', 'ret', 'je', 'out', 'in', 'jne', 'movl', 'imul', 'int3', 'lods', 'pushl', 'stos', 'scas', 'lret']
  
  chunks = split_dataframe(SW_train, 1225)
  del SW_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, TOP31_vocab, 'SW')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/SW_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  SW_test = pd.read_pickle('TokenizedData/SW_test.pkl')
  chunks = split_dataframe(SW_test, 1050)
  del SW_test
  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, TOP31_vocab, 'SW')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/SW_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with SW")

  #WP
  WP_train = pd.read_pickle('TokenizedData/WP_train.pkl')
  WP_vocab = ['mov_mov', 'add_add', 'mov_call', 'push_push', 'push_mov', 'call_mov', 'mov_push', 'pop_pop', 'push_call', 'lea_push', 'inc_add', 'mov_add', 'push_lea', 'lea_call', 'add_mov', 'mov_pop', 'pop_mov', 'pop_ret', 'lea_mov', 'call_lea', 'add_inc', 'mov_xor', 'mov_lea', 'add_push', 'jmp_mov', 'xor_mov', 'je_mov', 'test_je', 'call_push', 'mov_jmp']

  chunks = split_dataframe(WP_train, 1225)
  del WP_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, WP_vocab, 'WP')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/WP_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  WP_test = pd.read_pickle('TokenizedData/WP_test.pkl')
  chunks = split_dataframe(WP_test, 1050)
  del WP_test
  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, WP_vocab, 'WP')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/WP_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with WP")

  #BPE
  BPE_train = pd.read_pickle('TokenizedData/BPE_train.pkl')
  BPE_tokenizer = Tokenizer.from_file("Tokenizers/BPE-trained.json")
  BPE_vocab = list(BPE_tokenizer.get_vocab().keys())
  del BPE_tokenizer
  
  chunks = split_dataframe(BPE_train, 1225)
  del BPE_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, BPE_vocab, 'BPE')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/BPE_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  BPE_test = pd.read_pickle('TokenizedData/BPE_test.pkl')
  chunks = split_dataframe(BPE_test, 1050)
  del BPE_test

  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, BPE_vocab, 'BPE')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/BPE_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with BPE")

  #WPC
  WPC_train = pd.read_pickle('TokenizedData/WPC_df.pkl')
  WPC_tokenizer = Tokenizer.from_file("Tokenizers/WPC-trained.json")
  WPC_vocab = list(WPC_tokenizer.get_vocab().keys())
  del WPC_tokenizer

  chunks = split_dataframe(WPC_train, 1225)
  del WPC_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, WPC_vocab, 'WPC')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/WPC_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  WPC_test = pd.read_pickle('TokenizedData/WPC_test.pkl')
  chunks = split_dataframe(WPC_test, 1050)
  del WPC_test
  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, WPC_vocab, 'WPC')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/WPC_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with WPC")

  #SPC
  SPC_train = pd.read_pickle('TokenizedData/SPC_train.pkl')
  SPC_tokenizer = Tokenizer.from_file("Tokenizers/SPC-trained.json")
  SPC_vocab = list(SPC_tokenizer.get_vocab().keys())
  del SPC_tokenizer
  
  chunks = split_dataframe(SPC_train, 1225)
  del SPC_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, SPC_vocab, 'SPC')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/SPC_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  SPC_test = pd.read_pickle('TokenizedData/SPC_test.pkl')
  chunks = split_dataframe(SPC_test, 1050)
  del SPC_test
  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, SPC_vocab, 'SPC')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/SPC_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with SPC")

  #UNI
  UNI_train = pd.read_pickle('TokenizedData/UNI_train.pkl')
  UNI_tokenizer = Tokenizer.from_file("Tokenizers/UNI-trained.json")
  UNI_vocab = list(UNI_tokenizer.get_vocab().keys())
  del UNI_tokenizer

  chunks = split_dataframe(UNI_train, 1225)
  del UNI_train
  train_embeddings_list = []
  for chunk in chunks:
    train_embeddings = hmm2vec_embeddings(chunk, 2, UNI_vocab, 'UNI')
    train_embeddings_list.append(train_embeddings)
    del train_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_train_embeddings = np.vstack(train_embeddings_list)
  del train_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/UNI_train_hmm2vec.npy', all_train_embeddings)
  del all_train_embeddings

  UNI_test = pd.read_pickle('TokenizedData/UNI_test.pkl')
  chunks = split_dataframe(UNI_test, 1050)
  del UNI_test
  test_embeddings_list = []
  for chunk in chunks:
    test_embeddings = hmm2vec_embeddings(chunk, 2, UNI_vocab, 'UNI')
    test_embeddings_list.append(test_embeddings)
    del test_embeddings
    del chunk
  del chunks

  # Concatenate all embeddings into a single numpy array
  all_test_embeddings = np.vstack(test_embeddings_list)
  del test_embeddings_list

  # Save the embeddings to a file
  np.save('Embeddings/UNI_test_hmm2vec.npy', all_test_embeddings)
  del all_test_embeddings
  
  print("done with UNI")

if __name__ == "__main__":
    main()
