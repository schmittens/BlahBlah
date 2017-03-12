import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag, map_tag
from nltk.corpus import stopwords
from nltk.chunk import *
from itertools import product


# make a list of words to deduct from stopwords

# create command line input

# build vocabulary?

# chunking?
# concordance

class DomainParser():
    def __init__(self, query):
        self.query = query
        self.parse_query = query
        self.stopped = []

        self.language = "english"
        self.nounGrammar = r"""
                        NP: {<DT|PP\$>?<JJ>?<[N].*>+}   # chunk determiner/possessive, adjectives and noun
                            {<[\.N].*>}       # chunk sequences of all noun forms
                            {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
                            {<NNP>+}                # chunk sequences of proper nouns
                            {<NNS>+}                # chunk sequences of possessive form nouns
                        """
        self.nounCP = nltk.RegexpParser(self.nounGrammar)
        self.nounChunked = ""
        self.nounChunkScore = ChunkScore()

        self.verbGrammar = r"""
                        VP: {<VB|VBP>}
                        """
        self.verbCP = nltk.RegexpParser(self.verbGrammar)

        self.stopwords = stopwords.words("english")
        self.stoptypes = None

        self.stemmer = SnowballStemmer(self.language)
        self.stemmed = []

        self.lemmatizer = WordNetLemmatizer()

        self.tokenizer = word_tokenize
        self.tagger = pos_tag

        self.synonymList = {}


    def getKey(self, item):
        return item[0]

    def setLanguage(self, language):
        self.language = language

    def setNounGrammar(self, grammar):
        self.nounGrammar = grammar
        self.nounCP = nltk.RegexpParser(self.nounGrammar)

    def setVerbGrammar(self, grammar):
        self.verbGrammar = grammar
        self.verbCP = nltk.RegexpParser(self.verbGrammar)

    def tokenize(self, query):
        self.tokenized = self.tokenizer(query)
        print(self.tokenized)

    def stop(self, query):
        for word in query:
            if word not in self.stopwords:
                self.stopped.append(word)
        print(self.stopped)

    def stem(self, query, lemmatize=True):
        if lemmatize == True:
            self.stemmed = [self.lemmatizer.lemmatize(word) for word in query]
            print("Lemmatized:", self.stemmed)
        else:
            self.stemmed = [self.stemmer.stem(word) for word in query]
            print("Stemmed:", self.stemmed)

    def tag(self, query):
        self.tagged = self.tagger(query)
        print(self.tagged)

    def nounChunk(self, query):
        self.nounChunked = self.nounCP.parse(query)
        print(self.nounChunked)
        for w, t, c in tree2conlltags(self.nounChunked):
            print("Word:",w, "Tag:", t, "Chunk:", c)

        # import settings (Stemmer to use, ...)

    def verbChunk(self, query):
        print(self.verbCP.parse(query))
        # import settings (Stemmer to use, ...)

    def synonimizer(self, word):
        synlist = wordnet.synsets(word)
        returnlist = []
        for item in synlist:
            lemmalist = item.lemmas()
            for lemma in lemmalist:
                returnlist.append(lemma.name())
        return returnlist

    def synonymLister(self, tokenized):
        for word in tokenized:
            sublist = self.synonimizer(word)
            self.synonymList[word] = sublist
        print(self.synonymList)

    def synonymFinder(self):
        pass

    def maxSimilarityFinder(self, queryword, domainword):
        syns1 = wordnet.synsets(queryword)
        syns2 = wordnet.synsets(domainword)
        sims = []

        for sense1, sense2 in product(syns1, syns2):
            d = wordnet.wup_similarity(sense1, sense2)
            sims.append((d, (queryword, sense1.definition()), (domainword, sense2.definition())))

        print(sims)

        p = 0
        returnItem = []

        for item in sims:
            if item[0]:
                #print(item[0])
                if item[0] > p:
                    p = item[0]
                    returnItem.append(item)

        return returnItem

    def averageSimilarity(self, similarityList):
        total = 0
        for item in similarityList:
            total += item

        return total/len(similarityList)


class IntentParser():
    def __init__(self, query, domain):
        self.query = query
        self.domain = domain

        # import domain specific settings

