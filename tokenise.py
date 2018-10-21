import MeCab
from search_algorithm2 import *
from natto import MeCab

# Tokenise the sentense into morphemes using MeCabs parse feature, and adds the result to a tokenised
def getToken(sentence):
    tokenised = []
    with MeCab(r'-F%m\n') as nm:
        for n in nm.parse(sentence, as_nodes=True):
            tokenised.append(n.feature)
    return tokenised

# This function assumes that the longest match in a string is the correct word.
def parseSentence(sentence):
    partsOfSent = []
    print(getToken(sentence)[:-1])
    tokenised = getToken(sentence)
    # 捕鯨が好きです
    for token in tokenised:
        tokenIter = tokenised
        # Combines all the morphemes and searches JMdict for the combination
        for tokenIndex in range(len(tokenised), 0, -1):
            searchToken = ""
            for item in tokenIter[0:tokenIndex]:
                searchToken += item
            wordDef = wordResults(searchToken)
            # If a match is found, the morphemes used in the combination are removed from tokenised.
            # This continues untill there are no morphemes left in tokenised.
            if wordDef != []:
                partsOfSent.append(wordDef)
                for i in tokenIter[0:tokenIndex]:
                    tokenised.pop(0)
    return partsOfSent
