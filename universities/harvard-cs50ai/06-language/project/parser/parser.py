import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det NP | NP NP | Adj NP | P NP | NP Adj | Adv NP | Conj NP | Adv
VP -> V | V NP | Adv VP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokens from sentance
    tokens = nltk.word_tokenize(sentence)
    # list of words that will be returned
    words = []

    # check every token
    for token in tokens:
        # if at least one character is an aplhabetic, add token to words
        for character in token:
            if character.isalpha():
                words.append(token.lower())
                break

    return words

# code from
# https://github.com/Rajil1213/cs50AI/blob/master/Week6/parser/parser.py


def check(subtree):
    """
    Return True if any child of 'subtree' has the label "NP"
    """

    # if the subtree itself is an NP, then return True
    if subtree.label() == "NP":
        return True

    # if the subtree has only one child, then its probably a terminal node
    # in which case return False
    # but the label must not be 'S' since
    # S can contain only one child when S -> VP is followed by the parse tree
    if len(subtree) == 1 and subtree.label() != 'S':
        return False

    # otherwise go further into the subtree
    # and evaluate each subsubtree there
    for subsubtree in subtree:

        if check(subsubtree):
            return True

    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    chunks = []

    for subtree in tree:

        # get the label of the subtree defined by the grammar
        node = subtree.label()

        # check if this tree contains a subtree with 'NP'
        # if not check another subtree
        contains = check(subtree)
        if not contains:
            continue

        # if the node is a NP or VP or S, then
        # go further into the tree to check for noun phrase chunks
        # at each point take the list of trees returned and
        # append each to the actual chunks' list in the parent
        if node == "NP" or node == "VP" or node == "S":
            subsubtree = np_chunk(subtree)
            for np in subsubtree:
                chunks.append(np)

    # if the current tree has no subtree with a 'NP' label
    # and is itself an 'NP' labeled node then, append the tree to chunks
    if tree.label() == "NP" and not contains:
        chunks.append(tree)

    return chunks


if __name__ == "__main__":
    main()
