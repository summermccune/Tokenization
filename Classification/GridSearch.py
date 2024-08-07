from matplotlib import pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from scikeras.wrappers import KerasClassifier
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def create_CNN_model(X_train):
    v_size = len(X_train[0])
    model = models.Sequential([
        layers.Input(shape=(v_size, 1)),
        layers.Conv1D(500, 1, activation='relu'),
        layers.Dropout(0.5),
        layers.Flatten(),
        layers.Dense(7, activation='softmax')
    ])
    optimizer = optimizers.Adam()
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
    return model

#GRID SEARCH
def SVM_linear(SVM_linear_grid, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    print(f'Starting SVM-linear for {tokenization_method} - {embedding_method}')
    svm = SVC(kernel = 'linear')
    grid_search = GridSearchCV(estimator=svm, param_grid=SVM_linear_grid, cv=2, verbose = 1)
    # Running the GridSearchCV
    grid_search.fit(X_train, y_train)
    print(f"Best parameters for {tokenization_method} - {embedding_method} - {model_name}: {grid_search.best_params_}")
    evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name)
    print(f'Finished SVM-linear for {tokenization_method} - {embedding_method}')

def SVM_rbf(SVM_grid, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    print(f'Starting SVM-rbf for {tokenization_method} - {embedding_method}')
    svm = SVC(kernel = 'rbf')
    grid_search = GridSearchCV(estimator=svm, param_grid=SVM_grid, cv=2, verbose = 1)
    # Running the GridSearchCV
    grid_search = grid_search.fit(X_train, y_train)
    print(f"Best parameters for {tokenization_method} - {embedding_method} - {model_name}: {grid_search.best_params_}")
    evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name)
    print(f'Finished SVM-rbf for {tokenization_method} - {embedding_method}')

def RF(RF_grid, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    print(f'Starting RF for {tokenization_method} - {embedding_method}')
    rf = RandomForestClassifier()
    grid_search = GridSearchCV(estimator=rf, param_grid=RF_grid, cv=2, verbose = 1)
    # Running the GridSearchCV
    grid_search = grid_search.fit(X_train, y_train)
    print(f"Best parameters for {tokenization_method} - {embedding_method} - {model_name}: {grid_search.best_params_}")
    evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name)
    print(f'Finished RF for {tokenization_method} - {embedding_method}')
    
def MLP(MLP_grid, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    print(f'Starting MLP for {tokenization_method} - {embedding_method}')
    mlp = MLPClassifier()
    grid_search = GridSearchCV(estimator=mlp, param_grid=MLP_grid, cv=2, verbose = 1)
    # Running the GridSearchCV
    grid_search = grid_search.fit(X_train, y_train)
    print(f"Best parameters for {tokenization_method} - {embedding_method} - {model_name}: {grid_search.best_params_}")
    evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name)
    print(f'Finished MLP for {tokenization_method} - {embedding_method}')

def CNN(CNN_grid, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    print(f'Starting CNN for {tokenization_method} - {embedding_method}')
    model = KerasClassifier(model=create_CNN_model(X_train))
    grid_search = GridSearchCV(estimator=model, param_grid=CNN_grid, cv=2, verbose = 1)
    # Running the GridSearchCV
    ohe = OneHotEncoder(sparse_output=False).fit(y_train.to_numpy().reshape(-1,1))
    y_train = ohe.transform(y_train.to_numpy().reshape(-1,1))
    y_test = ohe.transform(y_test.to_numpy().reshape(-1,1))
    grid_search = grid_search.fit(X_train, y_train)
    print(f"Best parameters for {tokenization_method} - {embedding_method} - {model_name}: {grid_search.best_params_}")
    evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name)
    print(f'Finished CNN for {tokenization_method} - {embedding_method}')

def evaluate_model(grid_search, X_train, X_test, y_train, y_test, tokenization_method, embedding_method, model_name):
    
    y_pred = grid_search.predict(X_test)
    train_pred = grid_search.predict(X_train)
    
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Train accuracy:", accuracy_score(y_train, train_pred))
    print("F1 Score:", f1_score(y_test, y_pred, average='weighted'))
    print("Precision:", precision_score(y_test, y_pred, average='weighted'))
    print("Recall:", recall_score(y_test, y_pred, average='weighted'))

    
    if model_name == 'CNN':
        # Convert one-hot encoded labels back to single-label format
        y_test_single = y_test.argmax(axis=1)
        y_pred_single = y_pred.argmax(axis=1)
        
    cm = confusion_matrix(y_test, y_pred)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    names = ['BHO', 'CeeInject', 'FakeRean', 'OnLineGames', 'Vobfus', 'Winwebsec', 'Renos']
    disp = ConfusionMatrixDisplay(confusion_matrix=cm_normalized, display_labels=names)
    disp.plot(cmap=plt.cm.Blues, xticks_rotation = 0.45)
    plt.title(f"{tokenization_method} + {embedding_method} + {model_name}")
    plt.show()

    plt.savefig(f"CMS2/{tokenization_method}_{embedding_method}_{model_name}.png")

def grid_results(tokenization_method):

    SVM_linear_grid = {'C':[0.1,1,10,100]}

    SVM_grid = {'C': [0.1,1,10,100,1000],
                'gamma': [1,0.1,0.01,0.001,0.0001]}

    RF_grid = {'bootstrap': [True, False],
               'n_estimators': [10,50,100,200,400,600,800],
               'max_depth': [None,10,20,30,40]}

    CNN_grid = {'epochs': [10,20,30,40,50],
                'optimizer__learning_rate': [0.00001,0.0001,0.001,0.01,0.1]}
    
    MLP_grid = {'learning_rate_init': [0.00001,0.0001,0.001,0.01,0.1],
                'early_stopping': [True],
                'hidden_layer_sizes': [(100,), (500,),(1000,)]}
    
    #Set up values
    print('Reading in data')
    train_df = pd.read_pickle(f'TokenizedData/{tokenization_method}_train.pkl')
    test_df = pd.read_pickle(f'TokenizedData/{tokenization_method}_test.pkl')

    X_train_w2v_SVM = np.load(f'Embeddings/{tokenization_method}_train_w2v_SVM.npy')
    X_test_w2v_SVM = np.load(f'Embeddings/{tokenization_method}_test_w2v_SVM.npy')

    X_train_w2v = np.load(f'Embeddings/{tokenization_method}_train_w2v.npy')
    X_test_w2v = np.load(f'Embeddings/{tokenization_method}_test_w2v.npy')


    X_train_hmm2vec = np.load(f'Embeddings/{tokenization_method}_train_hmm2vec.npy')
    X_test_hmm2vec = np.load(f'Embeddings/{tokenization_method}_test_hmm2vec.npy')

    X_train_bert = np.load(f'Embeddings/{tokenization_method}_bert_train.npy')
    X_test_bert = np.load(f'Embeddings/{tokenization_method}_bert_test.npy')

    X_train_elmo = np.load(f'Embeddings/{tokenization_method}_elmo_train.npy')
    X_test_elmo = np.load(f'Embeddings/{tokenization_method}_elmo_test.npy')

    y_train = train_df['Label']
    y_test = test_df['Label']
    print('Finished reading in data')

    # #SVM NEED TO DO SVM LINEAR AND RBF
    SVM_linear(SVM_linear_grid, X_train_w2v_SVM, X_test_w2v_SVM, y_train, y_test, tokenization_method, 'w2v', 'SVM-linear')
    SVM_rbf(SVM_grid, X_train_w2v_SVM, X_test_w2v_SVM, y_train, y_test, tokenization_method, 'w2v', 'SVM-rbf')
    SVM_linear(SVM_linear_grid, X_train_hmm2vec, X_test_hmm2vec, y_train, y_test, tokenization_method, 'hmm2vec', 'SVM-linear')
    SVM_rbf(SVM_grid, X_train_hmm2vec, X_test_hmm2vec, y_train, y_test, tokenization_method, 'hmm2vec', 'SVM-rbf')
    SVM_linear(SVM_linear_grid, X_train_bert, X_test_bert, y_train, y_test, tokenization_method, 'bert', 'SVM-linear')
    SVM_rbf(SVM_grid, X_train_bert, X_test_bert, y_train, y_test, tokenization_method, 'bert', 'SVM-rbf')
    SVM_linear(SVM_linear_grid, X_train_elmo, X_test_elmo, y_train, y_test, tokenization_method, 'elmo', 'SVM-linear')
    SVM_rbf(SVM_grid, X_train_elmo, X_test_elmo, y_train, y_test, tokenization_method, 'elmo', 'SVM-rbf')

    # #RF
    RF(RF_grid, X_train_w2v, X_test_w2v, y_train, y_test, tokenization_method, 'w2v', 'RF')
    RF(RF_grid, X_train_hmm2vec, X_test_hmm2vec, y_train, y_test, tokenization_method, 'hmm2vec', 'RF')
    RF(RF_grid, X_train_bert, X_test_bert, y_train, y_test, tokenization_method, 'bert', 'RF')
    RF(RF_grid, X_train_elmo, X_test_elmo, y_train, y_test, tokenization_method, 'elmo', 'RF')

    #CNN
    CNN(CNN_grid, X_train_w2v, X_test_w2v, y_train, y_test, tokenization_method, 'w2v', 'CNN')
    CNN(CNN_grid, X_train_hmm2vec, X_test_hmm2vec, y_train, y_test, tokenization_method, 'hmm2vec', 'CNN')
    CNN(CNN_grid, X_train_bert, X_test_bert, y_train, y_test, tokenization_method, 'bert', 'CNN')
    CNN(CNN_grid, X_train_elmo, X_test_elmo, y_train, y_test, tokenization_method, 'elmo', 'CNN')

    #MLP
    MLP(MLP_grid, X_train_w2v, X_test_w2v, y_train, y_test, tokenization_method, 'w2v', 'MLP')
    MLP(MLP_grid, X_train_hmm2vec, X_test_hmm2vec, y_train, y_test, tokenization_method, 'hmm2vec', 'MLP')
    MLP(MLP_grid, X_train_bert, X_test_bert, y_train, y_test, tokenization_method, 'bert', 'MLP')
    MLP(MLP_grid, X_train_elmo, X_test_elmo, y_train, y_test, tokenization_method, 'elmo', 'MLP')



def main():
    
    #SINGLE WORDS
    grid_results('SW')

    #WORD PAIRS
    grid_results('WP')

    #BYTE PAIR ENCODING
    grid_results('BPE')

    #WORD PIECE
    grid_results('WPC')

    #SENTENCE PIECE
    grid_results('SPC')

    #UNIGRAM
    grid_results('UNI')

if __name__ == "__main__":
    main()
