import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

def create_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
     yield data[i:i + batch_size]

def to_sentence(df):
    processed_dataset = []

    for sample in df['Opcodes']:
     # Split the string by commas and join with space
     processed_sample = ' '.join(sample)
     # Append the processed sample to the new dataset
     processed_dataset.append(processed_sample)

    return processed_dataset


def elmo_model(data, batch_size=32):
    elmo = hub.KerasLayer("https://tfhub.dev/google/elmo/3")

    emb = elmo(tf.constant(data['Opcodes']))
    embeddings = emb.numpy()

    return embeddings

def split_dataframe(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def main():
    #SW
    print("Starting SW")
    SW_train = pd.read_pickle('TokenizedData/SW_train.pkl')
    SW_train['Opcodes'] = SW_train['Opcodes'].apply(lambda x: x[:64])
    SW_train['Opcodes'] = to_sentence(SW_train)
    chunks = split_dataframe(SW_train, 1225)
    del SW_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/SW_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    SW_test = pd.read_pickle('TokenizedData/SW_test.pkl')
    SW_test['Opcodes'] = SW_test['Opcodes'].apply(lambda x: x[:64])
    SW_test['Opcodes'] = to_sentence(SW_test)
    chunks = split_dataframe(SW_test, 1050)
    del SW_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/SW_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished SW")
    

    #WP
    print("Starting WP")
    WP_train = pd.read_pickle('TokenizedData/WP_train.pkl')
    WP_train['Opcodes'] = WP_train['Opcodes'].apply(lambda x: x[:64])
    WP_train['Opcodes'] = to_sentence(WP_train)
    chunks = split_dataframe(WP_train, 1225)
    del WP_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/WP_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    WP_test = pd.read_pickle('TokenizedData/WP_test.pkl')
    WP_test['Opcodes'] = WP_test['Opcodes'].apply(lambda x: x[:64])
    WP_test['Opcodes'] = to_sentence(WP_test)
    chunks = split_dataframe(WP_test, 1050)
    del WP_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/WP_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished WP")
    
    #Load tokenized data
    print("Starting BPE")
    BPE_train = pd.read_pickle('TokenizedData/BPE_train.pkl')
    BPE_train['Opcodes'] = BPE_train['Opcodes'].apply(lambda x: x[:64])
    BPE_train['Opcodes'] = to_sentence(BPE_train)
    chunks = split_dataframe(BPE_train, 1225)
    del BPE_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/BPE_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    BPE_test = pd.read_pickle('TokenizedData/BPE_test.pkl')
    BPE_test['Opcodes'] = BPE_test['Opcodes'].apply(lambda x: x[:64])
    BPE_test['Opcodes'] = to_sentence(BPE_test)
    chunks = split_dataframe(BPE_test, 1050)
    del BPE_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/BPE_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished BPE")
    
    #WPC
    print("Starting WPC")
    WPC_train = pd.read_pickle('TokenizedData/WPC_train.pkl')
    WPC_train['Opcodes'] = WPC_train['Opcodes'].apply(lambda x: x[:64])
    WPC_train['Opcodes'] = to_sentence(WPC_train)
    chunks = split_dataframe(WPC_train, 1225)
    del WPC_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/WPC_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    WPC_test = pd.read_pickle('TokenizedData/WPC_test.pkl')
    WPC_test['Opcodes'] = WPC_test['Opcodes'].apply(lambda x: x[:64])
    WPC_test['Opcodes'] = to_sentence(WPC_test)
    chunks = split_dataframe(WPC_test, 1050)
    del WPC_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/WPC_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished WPC")
    
    #SPC
    print("Starting SPC")
    SPC_train = pd.read_pickle('TokenizedData/SPC_train.pkl')
    SPC_train['Opcodes'] = SPC_train['Opcodes'].apply(lambda x: x[:64])
    SPC_train['Opcodes'] = to_sentence(SPC_train)
    chunks = split_dataframe(SPC_train, 1225)
    del SPC_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/SPC_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    SPC_test = pd.read_pickle('TokenizedData/SPC_test.pkl')
    SPC_test['Opcodes'] = SPC_test['Opcodes'].apply(lambda x: x[:64])
    SPC_test['Opcodes'] = to_sentence(SPC_test)
    chunks = split_dataframe(SPC_test, 1050)
    del SPC_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/SPC_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished SPC")
    
    #UNI
    print("Starting UNI")
    UNI_train = pd.read_pickle('TokenizedData/UNI_train.pkl')
    UNI_train['Opcodes'] = UNI_train['Opcodes'].apply(lambda x: x[:64])
    UNI_train['Opcodes'] = to_sentence(UNI_train)
    chunks = split_dataframe(UNI_train, 1225)
    del UNI_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/UNI_elmo_train.npy', all_embeddings)
    del all_embeddings

    #Load tokenized data
    UNI_test = pd.read_pickle('TokenizedData/UNI_test.pkl')
    UNI_test['Opcodes'] = UNI_test['Opcodes'].apply(lambda x: x[:64])
    UNI_test['Opcodes'] = to_sentence(UNI_test)
    chunks = split_dataframe(UNI_test, 1050)
    del UNI_train

    embeddings_list = []
    for chunk in chunks:
        embeddings = elmo_model(chunk)
        embeddings_list.append(embeddings)
        del embeddings
        del chunk
    del chunks

    all_embeddings = np.vstack(embeddings_list)
    np.save('Embeddings/UNI_elmo_test.npy', all_embeddings)
    del all_embeddings

    print("Finished UNI")
    

if __name__ == "__main__":
    main()
