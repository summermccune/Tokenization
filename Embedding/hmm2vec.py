import pandas as pd
import numpy as np
from hmmlearn import hmm

def train_hmm_models(opcodes,n_states):
    hmm_models = []
    for opcode_seq in opcodes:
        opcode_seq = np.array(opcode_seq)

        model = hmm.CategoricalHMM(n_components=n_states, n_iter=100)
        model.fit(opcode_seq.reshape(-1, 1))

        hmm_models.append(model)
        
    return hmm_models

def opcodes_to_numbers(dataset):
    opcode_to_number = opcodes_to_numbers_dict(dataset)
    columns = dataset['Opcodes']
    opcode_sequences = []
    for sample in columns:
        temp = []
        for opcode in sample:
            temp.append(opcode_to_number[opcode])
            opcode_sequences.append(temp)
    return opcode_sequences

def opcodes_to_numbers_dict(df):
    opcode_to_number = {}
    count = 0
    for opcode_list in df['Opcodes']:
        for opcode in opcode_list:
            if opcode not in opcode_to_number:
                opcode_to_number[opcode] = count
                count += 1
    print(opcode_to_number)
    return opcode_to_number

def b_matrix_to_features(hmm_models, max_feature_length):
    hmm2vec_features = []
    for model in hmm_models:
        mov_index = np.argmax(model.emissionprob_[:, opcode_to_number['mov']])
        sorted_indices = [mov_index, 1 - mov_index]
        sorted_bmatrices = model.emissionprob_[sorted_indices]
        feature_vector = sorted_bmatrices.flatten()

        if len(feature_vector) < max_feature_length:
            feature_vector = np.pad(feature_vector, (0, max_feature_length - len(feature_vector)), mode='constant')
        elif len(feature_vector) > max_feature_length:
            feature_vector = feature_vector[:max_feature_length]
            hmm2vec_features.append(feature_vector)
    return hmm2vec_features

#Function to generate HMM2Vec embeddings
def hmm2vec_embeddings(df,n_states):
    #convert opcodes to numbers
    opcode_sequences = opcodes_to_numbers(df)
    hmm_models = train_hmm_models(opcode_sequences, n_states)
    hmm2vec_features = b_matrix_to_features(hmm_models, 100)
    return hmm2vec_features

def main():
    #Load tokenized data
    TOP31_df = pd.read_pickle('TokenizedData/TOP31.pkl')
    SPC_df = pd.read_pickle('TokenizedData/SPC_df.pkl')
    BPE_df = pd.read_pickle('TokenizedData/BPE_df.pkl')
    UNI_df = pd.read_pickle('TokenizedData/UNI_df.pkl')
    WPC_df = pd.read_pickle('TokenizedData/WPC_df.pkl')

    #Generate embeddings
    TOP31_hmm2vec_embeddings = hmm2vec_embeddings(TOP31_df,2)
    SPC_hmm2vec_embeddings = hmm2vec_embeddings(SPC_df,2)
    BPE_hmm2vec_embeddings = hmm2vec_embeddings(BPE_df,2)
    UNI_hmm2vec_embeddings = hmm2vec_embeddings(UNI_df,2)                                                             $
    WPC_hmm2vec_embeddings = hmm2vec_embeddings(WPC_df,2)

    #save embeddings as npy
    np.save('Embeddings/TOP31_hmm2vec_embeddings.npy', TOP31_hmm2vec_embeddings)
    np.save('Embeddings/SPC_hmm2vec_embeddings.npy', SPC_hmm2vec_embeddings)
    np.save('Embeddings/BPE_hmm2vec_embeddings.npy', BPE_hmm2vec_embeddings)
    np.save('Embeddings/UNI_hmm2vec_embeddings.npy', UNI_hmm2vec_embeddings)
    np.save('Embeddings/WPC_hmm2vec_embeddings.npy', WPC_hmm2vec_embeddings)

    print("finished")

if __name__ == "__main__":
    main()
