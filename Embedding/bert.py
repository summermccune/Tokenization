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
    print("STARTING")
    #TOP31
    #LOAD TOKENIZED DATA FROM EARLIER
    bert = DistilBERT()
    TOP31_df = pd.read_pickle('TokenizedData/TOP31.pkl')
    print("finished reading in TOP31")
    #turn into a sentence
    TOP31_df['Opcodes'] = to_sentence(TOP31_df)
    print("finished turning TOP31 to sentence")
    # Split dataframe into chunks
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
    print("finished getting embeddings for TOP31")
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    # Save the embeddings to a file
    np.save('Embeddings/TOP31_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    print("done with TOP31")

    #WP
    #LOAD TOKENIZED DATA FROM EARLIER
    WP_df = pd.read_pickle('TokenizedData/WP_df.pkl')
    #turn into a sentence
    WP_df['Opcodes'] = to_sentence(WP_df)
    # Split dataframe into chunks
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
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    # Save the embeddings to a file
    np.save('Embeddings/WP_bert_embeddings.npy', all_embeddings)
    del all_embeddings

    #BPE
    #LOAD TOKENIZED DATA FROM EARLIER
    BPE_df = pd.read_pickle('TokenizedData/BPE_df.pkl')
    #turn into a sentence
    BPE_df['Opcodes'] = to_sentence(BPE_df)
    # Split dataframe into chunks
    chunks = split_dataframe(BPE_df)
    del BPE_df
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
    np.save('Embeddings/BPE_bert_embeddings.npy', all_embeddings)
    del all_embeddings

    #WPC
    #LOAD TOKENIZED DATA FROM EARLIER
    WPC_df = pd.read_pickle('TokenizedData/WPC_df.pkl')
    #turn into a sentence
    WPC_df['Opcodes'] = to_sentence(WPC_df)
    # Split dataframe into chunks
    chunks = split_dataframe(WPC_df)
    del WPC_df
    # Process each chunk
    embeddings_list = []
    for chunk in chunks:
        embeddings, _ = bert.embed(chunk['Opcodes'].tolist())
        embeddings_list.append(embeddings)
        del chunk
        del embeddings
    del chunks
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    # Save the embeddings to a file
    np.save('Embeddings/WPC_bert_embeddings.npy', all_embeddings)
    del all_embeddings

    #SPC
    #LOAD TOKENIZED DATA FROM EARLIER
    SPC_df = pd.read_pickle('TokenizedData/SPC_df.pkl')
    #turn into a sentence
    SPC_df['Opcodes'] = to_sentence(SPC_df)
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
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    # Save the embeddings to a file
    np.save('Embeddings/SPC_bert_embeddings.npy', all_embeddings)
    del all_embeddings

    #UNI
    #LOAD TOKENIZED DATA FROM EARLIER
    UNI_df = pd.read_pickle('TokenizedData/WPC_df.pkl')
    #turn into a sentence
    UNI_df['Opcodes'] = to_sentence(UNI_df)
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
    # Concatenate all embeddings into a single numpy array
    all_embeddings = np.vstack(embeddings_list)
    # Save the embeddings to a file
    np.save('Embeddings/UNI_bert_embeddings.npy', all_embeddings)
    del all_embeddings
    
if __name__ == "__main__":
    main()
