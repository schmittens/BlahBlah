from SR.Listener import Listener
from Logging.Logging import SRLogger
from NL.NLProcessor import DomainParser

testqueries = [
    "Turn on the light",
    "Turn off the light",
    "Diagnostics mode",
    "System status",
    "Cats are great",
    "Great cats are big"
]

log = SRLogger()

#l = Listener(['google', 'ibm'])
#l.__getattribute__(l.mode)()

#print(l.json)

testlist = ['test1', 'test2']



for utterance in testqueries:
    print(utterance)
    nlp = DomainParser(utterance)
    #nlp.tokenize(nlp.query)
    #nlp.tag(nlp.tokenized)
    #nlp.nounChunk(nlp.tagged)
    #nlp.synonymLister(nlp.tokenized)

    print(nlp.maxSimilarityFinder('light', 'light'))
    print(nlp.averageSimilarity([0.5, 1]))


