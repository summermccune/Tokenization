import pandas as pd
import numpy as np
import torch
import transformers as ppb

class DistilBERT:
    def __init__(self, batch_size: int = 16):
      """ Initialize Distil-BERT model

      Args:
          param: distil-bert parameters from hydra config
      """
      self.batch_size = batch_size
      self.model_class = ppb.DistilBertModel
      self.tokenizer_class = ppb.DistilBertTokenizer

      self.tokenizer = self.tokenizer_class.from_pretrained(
          'distilbert-base-uncased'
      )
      self.model = self.model_class.from_pretrained(
          'distilbert-base-uncased'
      )

    def embed(self, sample):
      """ Embed the data in small batches

      Args:
          sample (list): list of sentences

      Returns:
          features (list): the CLS tokens of size len(sample) x 768
      """
      n = len(sample)
      features = []

      # Loop through list of sentences batch by batch
      for i in range(0, n, self.batch_size):
        batch = sample[i:i+self.batch_size]

        tokens = self.tokenizer(
            batch, add_special_tokens=True, padding=True, truncation=True,
            max_length=512, return_tensors='pt')

        with torch.no_grad():
            last_hidden_states = self.model(
                tokens['input_ids'], attention_mask=tokens['attention_mask']
            )

        # Return only the CLS tokens
        batch_features = last_hidden_states[0][:, 0, :].numpy()
        features.extend(batch_features)

      return features, tokens
    
def to_sentence(df):
    processed_dataset = []

    for sample in df['Opcodes']:
        # Split the string by commas and join with space
        processed_sample = ' '.join(sample)
        # Append the processed sample to the new dataset
        processed_dataset.append(processed_sample)
    return processed_dataset

# Function to split dataframe into chunks
def split_dataframe(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def main():
    print("Starting BERT embedding process")
    
    #initialize bert
    bert = DistilBERT()
    
    #SINGLE WORDS SECTION - SW:
    
    print("Starting SW")
    
    #read in the single words train data
    SW_train = pd.read_pickle('TokenizedData/SW_train.pkl')
    
    #turn data into sentences instead of lists
    SW_train['Opcodes'] = to_sentence(SW_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(SW_train, 1225)
    del SW_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/SW_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the single words test data
    SW_test = pd.read_pickle('TokenizedData/SW_test.pkl')
    
    #turn data into sentences instead of lists
    SW_test['Opcodes'] = to_sentence(SW_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(SW_test, 1050)
    del SW_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/SW_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with SW")

    #WORD PAIRS SECTION - WP:
    
    print("Starting WP")
    
    #read in the WP train data
    WP_train = pd.read_pickle('TokenizedData/WP_train.pkl')
    
    #turn data into sentences instead of lists
    WP_train['Opcodes'] = to_sentence(WP_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(WP_train, 1225)
    del WP_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WP_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the WP test data
    WP_test = pd.read_pickle('TokenizedData/WP_test.pkl')
    
    #turn data into sentences instead of lists
    WP_test['Opcodes'] = to_sentence(WP_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(WP_test, 1050)
    del WP_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WP_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with WP")

    #BYTE PAIR ENCODING SECTION - BPE:

    print("Starting BPE")
    
    #read in the BPE train data
    BPE_train = pd.read_pickle('TokenizedData/BPE_train.pkl')
    
    #turn data into sentences instead of lists
    BPE_train['Opcodes'] = to_sentence(BPE_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(BPE_train, 1225)
    del BPE_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/BPE_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the BPE test data
    BPE_test = pd.read_pickle('TokenizedData/BPE_test.pkl')
    
    #turn data into sentences instead of lists
    BPE_test['Opcodes'] = to_sentence(BPE_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(BPE_test, 1050)
    del BPE_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/BPE_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with BPE")

    #WORD PIECE SECTION - WPC:

    print("Starting WPC")
    
    #read in the WPC train data
    WPC_train = pd.read_pickle('TokenizedData/WPC_train.pkl')
    
    #turn data into sentences instead of lists
    WPC_train['Opcodes'] = to_sentence(WPC_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(WPC_train, 1225)
    del WPC_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WPC_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the WPC test data
    WPC_test = pd.read_pickle('TokenizedData/WPC_test.pkl')
    
    #turn data into sentences instead of lists
    WPC_test['Opcodes'] = to_sentence(WPC_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(WPC_test, 1050)
    del WPC_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WPC_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with WPC")

    #SENTENCE PIECE SECTION - SPC:
    
    print("Starting SPC")
    
    #read in the SPC train data
    SPC_train = pd.read_pickle('TokenizedData/SPC_train.pkl')
    
    #turn data into sentences instead of lists
    SPC_train['Opcodes'] = to_sentence(SPC_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(SPC_train, 1225)
    del SPC_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/SPC_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the SPC test data
    SPC_test = pd.read_pickle('TokenizedData/SPC_test.pkl')
    
    #turn data into sentences instead of lists
    SPC_test['Opcodes'] = to_sentence(SPC_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(SPC_test, 1050)
    del SPC_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/SPC_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with SPC")

    #UNIGRAM SECTION - UNI:

    print("Starting UNI")
    
    #read in the UNI train data
    UNI_train = pd.read_pickle('TokenizedData/UNI_train.pkl')
    
    #turn data into sentences instead of lists
    UNI_train['Opcodes'] = to_sentence(UNI_train)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(UNI_train, 1225)
    del UNI_train
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/UNI_bert_train.npy', all_embeddings)
    del all_embeddings
    
    #read in the UNI test data
    UNI_test = pd.read_pickle('TokenizedData/UNI_test.pkl')
    
    #turn data into sentences instead of lists
    UNI_test['Opcodes'] = to_sentence(UNI_test)
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(UNI_test, 1050)
    del UNI_test
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/UNI_bert_test.npy', all_embeddings)
    del all_embeddings

    print("Finished with UNI")

if __name__ == "__main__":
    main()
