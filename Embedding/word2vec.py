import numpy as np
import pandas as pd
from gensim.models import Word2Vec

def word2vec_embeddings(train_dataframe, test_dataframe):
  #word2vec N = 100, W = 30 FOR EVERYTHING BUT SVM
  model = Word2Vec(train_dataframe['Opcodes'], min_count=1, vector_size=100, window=30)
  train_embeddingsALL = np.array([np.mean([model.wv[word] for word in text if word in model.wv], axis=0) for text in train_dataframe['Opcodes']])
  test_embeddingsALL = np.array([np.mean([model.wv[word] for word in text if word in model.wv], axis=0) for text in test_dataframe['Opcodes']])


  #word2vec N = 31, W = 10 FOR SVM
  model = Word2Vec(train_dataframe['Opcodes'], min_count=1, vector_size=31, window=10)
  train_embeddingsSVM = np.array([np.mean([model.wv[word] for word in text if word in model.wv], axis=0) for text in train_dataframe['Opcodes']])
  test_embeddingsSVM = np.array([np.mean([model.wv[word] for word in text if word in model.wv], axis=0) for text in test_dataframe['Opcodes']])

  return train_embeddingsALL, train_embeddingsSVM, test_embeddingsALL, test_embeddingsSVM


def main():
  #SW
  print("Starting SW")
  SW_train = pd.read_pickle('TokenizedData/SW_train.pkl')
  SW_test = pd.read_pickle('TokenizedData/SW_test.pkl')
  SW_train_w2v, SW_train_w2v_SVM, SW_test_w2v, SW_test_w2v_SVM = word2vec_embeddings(SW_train, SW_test)

  #save as npy
  np.save('Embeddings/SW_train_w2v.npy', SW_train_w2v)
  np.save('Embeddings/SW_train_w2v_SVM.npy', SW_train_w2v_SVM)
  np.save('Embeddings/SW_test_w2v.npy', SW_test_w2v)
  np.save('Embeddings/SW_test_w2v_SVM.npy', SW_test_w2v_SVM)
  del SW_train, SW_test, SW_train_w2v, SW_train_w2v_SVM, SW_test_w2v, SW_test_w2v_SVM
  print("Finished SW")

  #WP
  print("Starting WP")
  WP_train = pd.read_pickle('TokenizedData/WP_train.pkl')
  WP_test = pd.read_pickle('TokenizedData/WP_test.pkl')
  WP_train_w2v, WP_train_w2v_SVM, WP_test_w2v, WP_test_w2v_SVM = word2vec_embeddings(WP_train, WP_test)

  #save as npy
  np.save('Embeddings/WP_train_w2v.npy', WP_train_w2v)
  np.save('Embeddings/WP_train_w2v_SVM.npy', WP_train_w2v_SVM)
  np.save('Embeddings/WP_test_w2v.npy', WP_test_w2v)
  np.save('Embeddings/WP_test_w2v_SVM.npy', WP_test_w2v_SVM)
  del WP_train, WP_test, WP_train_w2v, WP_train_w2v_SVM, WP_test_w2v, WP_test_w2v_SVM
  print("Finished WP")

  #BPE
  print("Starting BPE")
  BPE_train = pd.read_pickle('TokenizedData/BPE_train.pkl')
  BPE_test = pd.read_pickle('TokenizedData/BPE_test.pkl')
  BPE_train_w2v, BPE_train_w2v_SVM, BPE_test_w2v, BPE_test_w2v_SVM = word2vec_embeddings(BPE_train, BPE_test)

  #save as npy
  np.save('Embeddings/BPE_train_w2v.npy', BPE_train_w2v)
  np.save('Embeddings/BPE_train_w2v_SVM.npy', BPE_train_w2v_SVM)
  np.save('Embeddings/BPE_test_w2v.npy', BPE_test_w2v)
  np.save('Embeddings/BPE_test_w2v_SVM.npy', BPE_test_w2v_SVM)
  del BPE_train, BPE_test, BPE_train_w2v, BPE_train_w2v_SVM, BPE_test_w2v, BPE_test_w2v_SVM
  print("Finished BPE")

  #WPC
  print("Starting WPC")
  WPC_train = pd.read_pickle('TokenizedData/WPC_train.pkl')
  WPC_test = pd.read_pickle('TokenizedData/WPC_test.pkl')
  WPC_train_w2v, WPC_train_w2v_SVM, WPC_test_w2v, WPC_test_w2v_SVM = word2vec_embeddings(WPC_train, WPC_test)

  #save as npy
  np.save('Embeddings/WPC_train_w2v.npy', WPC_train_w2v)
  np.save('Embeddings/WPC_train_w2v_SVM.npy', WPC_train_w2v_SVM)
  np.save('Embeddings/WPC_test_w2v.npy', WPC_test_w2v)
  np.save('Embeddings/WPC_test_w2v_SVM.npy', WPC_test_w2v_SVM)
  del WPC_train, WPC_test, WPC_train_w2v, WPC_train_w2v_SVM, WPC_test_w2v, WPC_test_w2v_SVM
  print("Finished WPC")

  #SPC
  print("Starting SPC")
  SPC_train = pd.read_pickle('TokenizedData/SPC_train.pkl')
  SPC_test = pd.read_pickle('TokenizedData/SPC_test.pkl')
  SPC_train_w2v, SPC_train_w2v_SVM, SPC_test_w2v, SPC_test_w2v_SVM = word2vec_embeddings(SPC_train, SPC_test)

  #save as npy
  np.save('Embeddings/SPC_train_w2v.npy', SPC_train_w2v)
  np.save('Embeddings/SPC_train_w2v_SVM.npy', SPC_train_w2v_SVM)
  np.save('Embeddings/SPC_test_w2v.npy', SPC_test_w2v)
  np.save('Embeddings/SPC_test_w2v_SVM.npy', SPC_test_w2v_SVM)
  del SPC_train, SPC_test, SPC_train_w2v, SPC_train_w2v_SVM, SPC_test_w2v, SPC_test_w2v_SVM
  print("Finished SPC")

  #UNI
  print("Starting UNI")
  UNI_train = pd.read_pickle('TokenizedData/UNI_train.pkl')
  UNI_test = pd.read_pickle('TokenizedData/UNI_test.pkl')
  UNI_train_w2v, UNI_train_w2v_SVM, UNI_test_w2v, UNI_test_w2v_SVM = word2vec_embeddings(UNI_train, UNI_test)

  #save as npy
  np.save('Embeddings/UNI_train_w2v.npy', UNI_train_w2v)
  np.save('Embeddings/UNI_train_w2v_SVM.npy', UNI_train_w2v_SVM)
  np.save('Embeddings/UNI_test_w2v.npy', UNI_test_w2v)
  np.save('Embeddings/UNI_test_w2v_SVM.npy', UNI_test_w2v_SVM)
  del UNI_train, UNI_test, UNI_train_w2v, UNI_train_w2v_SVM, UNI_test_w2v, UNI_test_w2v_SVM
  print("Finished UNI")

if __name__ == "__main__":
    main()
