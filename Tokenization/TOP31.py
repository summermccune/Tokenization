#make new df with opcode and malware as columns
TOP31_df = dataset.copy()
TOP31_df.head()

#counting opcodes for data cleaning
countTotal = Counter()
count_unigrams(TOP31_df, countTotal)
TOP31_df.head()

#list for most common opcodes
total_count = countTotal.most_common(31)
countList = [x[0] for x in total_count]
print(countList)

#store cleaned rows
rows = removeNonVocab(countList, TOP31_df['Opcodes'])
TOP31_df['Opcodes'] = rows

print(TOP31_df.head())
print(TOP31_df.tail())

#convert tokenized dataframe to pkl
TOP31_df.to_pickle('TokenizedData/TOP31.pkl')
