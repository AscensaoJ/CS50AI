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
S -> NP VP | S Conj S | S Conj DC
DC -> VP NP
AdjP -> Adj | Adj AdjP
ConjP -> Conj NP | Conj VP | ConjP NP VP
NP -> N | Det NP | AdjP NP | N PP | N VP
PP -> P NP
VP -> V | V NP | V NP PP | V PP | Adv VP | VP Adv
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
    # Get tokens from sentence
    words = nltk.word_tokenize(sentence)

    # Ensure only tokens with at least one alphabetic character
    for word in words:
        has_alpha = False
        for char in word:
            if char.isalpha():
                has_alpha = True
                break
        if not has_alpha:
            words = [x for x in words if x != word]

    # Make all words lowercase
    words = [x.lower() for x in words]

    # Return list of preprocessed words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Initailize holder for found valid chunks
    chunks = []

    # Check each subtree of tree
    for subtree in tree.subtrees():

        # Only do something if subtree is noun phrase
        if subtree.label() == "NP":
            chunk = True

            #Check each subtree t of our current subtree
            for t in subtree.subtrees():

                # Skip current subtree, as tree is subtree of itself
                if t == subtree:
                    continue

                # Flag if current subtree has noun phrase subtrees
                if t.label() == "NP":
                    chunk = False
                    break
            
            # Add new valid chunck to list of found valid chunks
            if chunk:
                chunks.append(subtree)
    
    # Return list of found valid chunks
    return chunks


if __name__ == "__main__":
    main()
