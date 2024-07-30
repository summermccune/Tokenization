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
def split_dataframe(df, chunk_size=1000):
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def main():
    print("Starting BERT embedding process")
    
    #SINGLE WORDS SECTION - SW:
    
    #initialize bert
    bert = DistilBERT()
    
    #read in the single words data
    TOP31_df = pd.read_pickle('TokenizedData/TOP31.pkl')
    print("finished reading in SW")
    
    #turn data into sentences instead of lists
    TOP31_df['Opcodes'] = to_sentence(TOP31_df)
    print("finished turning SW to sentence")
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(TOP31_df)
    del TOP31_df
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    print("finished getting embeddings for SW")
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/TOP31_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("done with SW")

    #WORD PAIRS SECTION - WP:
    
    #read in the word pairs data
    WP_df = pd.read_pickle('TokenizedData/WP_df.pkl')
    print("finished reading in WP")
    
    #turn data into sentences instead of lists
    WP_df['Opcodes'] = to_sentence(WP_df)
    print("finished turning WP into sentences")
    
    # Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(WP_df)
    del WP_df
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    print("finished getting embeddings for WP")
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WP_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("done with WP")

    #BYTE PAIR ENCODING SECTION - BPE:

    #read in BPE data
    BPE_df = pd.read_pickle('TokenizedData/BPE_df.pkl')
    print("finished reading in BPE data")
    
    #turn data into sentences instead of a lists
    BPE_df['Opcodes'] = to_sentence(BPE_df)
    print("finished turning BPE to sentences")
    
    #Split dataframe into chunks in order to conserve memory
    chunks = split_dataframe(BPE_df)
    del BPE_df
    
    #Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks
    print("finished embeddings for BPE")
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/BPE_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("done with BPE")

    #WORD PIECE SECTION - WPC:

    #read in WPC data
    WPC_df = pd.read_pickle('TokenizedData/WPC_df.pkl')
    print("finished reading in WPC data")
    
    #turn data into sentences instead of lists
    WPC_df['Opcodes'] = to_sentence(WPC_df)
    print("finished turning WPC to sentences")
    
    #Split dataframe into chunks
    chunks = split_dataframe(WPC_df)
    del WPC_df
    
    #Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del chunk
        del embeddings
    del chunks
    print("finished getting embeddings for WPC")

    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/WPC_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("finished with WPC")

    #SENTENCE PIECE SECTION - SPC:
    
    #load SPC data
    SPC_df = pd.read_pickle('TokenizedData/SPC_df.pkl')
    print("finished reading in SPC data")
    
    #turn data into sentences instead of lists
    SPC_df['Opcodes'] = to_sentence(SPC_df)
    print("finished turning SPC to sentences")
    
    # Split dataframe into chunks
    chunks = split_dataframe(SPC_df)
    del SPC_df
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del chunk
        del embeddings
    del chunks
    print("finished getting embeddings for SPC")
    
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/SPC_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("finished with SPC")

    #UNIGRAM SECTION - UNI:
    
    #load UNI data
    UNI_df = pd.read_pickle('TokenizedData/WPC_df.pkl')
    print("finished reading in UNI data")
    
    #turn data into sentences instead of lists
    UNI_df['Opcodes'] = to_sentence(UNI_df)
    print("finished turning UNI to sentences")
    
    # Split dataframe into chunks
    chunks = split_dataframe(UNI_df)
    del UNI_df
    
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del chunk
        del embeddings
    del chunks
    print("finished getting embeddings for UNI")

    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    
    # Save the embeddings to a file
    np.save('Embeddings/UNI_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("finished with UNI")
    
if __name__ == "__main__":
    main()

