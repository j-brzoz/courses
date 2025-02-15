import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = {}

    # Read all files
    for filename in os.listdir(directory):

        # only if .txt files
        if filename[-4:] == ".txt":
            with open(os.path.join(directory, filename), "r",
                      encoding="utf8") as f:
                contents[filename] = f.read()

    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    for word in nltk.word_tokenize(document):
        if (word not in string.punctuation and
                word not in nltk.corpus.stopwords.words("english")):
            words.append(word.lower())

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    counter = dict()
    # check all documents
    for document in documents:
        words = set(documents[document])
        # check all words in a document
        for word in words:
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1

    for word in counter:
        idfs[word] = math.log(len(documents) / counter[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = dict()

    # for every file
    for filename in files:

        # sum of tf-idf values
        sum = 0
        # words in a file
        words = files[filename]

        for word in query:
            # count how many times the word appears in the document
            counter = words.count(word)

            # calculate the sum of tf-idf values
            if counter > 0:
                sum += counter * idfs[word]

        # add the score to dictionary
        ranking[filename] = sum

    # sort
    output = sorted([filename for filename in files],
                    key=lambda x: ranking[x],
                    reverse=True)

    return output[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # ranking dictionary
    ranking = {sentence: {"idf": 0, "qtd": 0, "length": 0, "fromQuery": 0}
               for sentence in sentences}

    # for every sentence update values
    for sentence in sentences:
        s = sentence
        ranking[s]["length"] = len(nltk.word_tokenize(s))
        for word in query:
            if word in sentences[s]:
                ranking[s]["idf"] += idfs[word]
                ranking[s]["fromQuery"] += sentences[s].count(word)

        ranking[s]["qtd"] = ranking[s]["fromQuery"] / ranking[s]["length"]

    # sort
    output = sorted([sentence for sentence in sentences],
                    key=lambda x: (ranking[x]["idf"], ranking[x]["qtd"]),
                    reverse=True)

    return output[:n]


if __name__ == "__main__":
    main()
