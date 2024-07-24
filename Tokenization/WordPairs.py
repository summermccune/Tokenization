def main():
    # Load your dataset
    dataset = pd.read_pickle('path_to_your_dataset.pkl')

    # Make new df as copy
    word_pairs_df = dataset.copy()

    # Counting bigrams for data cleaning
    countTotal = Counter()
    bigram_list = count_bigrams(word_pairs_df, countTotal)

    # List for most common bigrams
    total_count = countTotal.most_common(31)
    countList = [x[0] for x in total_count]
    print(countList)

    # Make new df for bigrams
    wp_df = pd.DataFrame(columns=['Opcodes', 'Label'])
    wp_df['Opcodes'] = bigram_list
    wp_df['Label'] = word_pairs_df['Label']

    # Remove non-vocab bigrams
    rows = removeNonVocab(countList, wp_df['Opcodes'])
    wp_df['Opcodes'] = rows
    wp_df.head()

    # Save the dataframe to a pickle file
    wp_df.to_pickle('TokenizedData/WP_df.pkl')

if __name__ == "__main__":
    main()

