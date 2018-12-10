from gensim.models.poincare import PoincareModel, PoincareRelations, LinkPredictionEvaluation, ReconstructionEvaluation
from gensim.test.utils import datapath
import json
import networkx as nx
from nltk.corpus import wordnet as wn
import numpy as np
import random
import csv

def generate_meaning(hyp, poly, randomV):
    random.seed(42)
    hypedges = set()
    polyedges = set()
    idToSynset = dict()
    synsetToId = dict()
    count = 0
    setSyn = []
    setSyn2 = []
    randomE = set()
    for synset in list(wn.all_synsets('n')):
        idToSynset[count] = synset
        synsetToId[synset] = count
        setSyn.append(str(synset.name()))
        if count == 15000:
            break
        count +=1
    if randomV:
        print ("here11")
        for i in range (0, 5000):
            rangeV = len(list(wn.all_synsets('n')))
            num1 = random.randint(0,15000)
            num2 = random.randint(0,15000)
            if num1 == num2:
                continue
            print(i, num1, num2)
            synset = setSyn[num1]
            synset2 = setSyn[num2]
            randomE.add((synset, synset2))
            setSyn2.append(synset)
            setSyn2.append(synset2)

    print ("done")
    if hyp:
        for synset in list(wn.all_synsets('n')):
            for synset2 in synset.hyponyms() + synset.instance_hyponyms():
                if str(synset.name()) in setSyn and str(synset2.name()) in setSyn:
                    hypedges.add((str(synset.name()), str(synset2.name())))
                    setSyn2.append(str(synset.name()))
                    setSyn2.append(str(synset2.name()))
    if poly:
        print ("here")
        for synset in list(wn.all_synsets('n')):
                for lemma_name in synset.lemma_names():
                    for synset2 in wn.synsets(lemma_name, "n"):
                        if str(synset.name()) in setSyn and str(synset2.name()) in setSyn:
                            if str(synset.name()) in setSyn2 and str(synset2.name()) in setSyn2:
                                polyedges.add((str(synset.name()), str(synset2.name())))
    return hypedges, polyedges, randomE

hyp,poly, randomFile = generate_meaning(False, True, True)
poly = list(poly)
# hyp = list(hyp)
randF = list(randomFile)
num = len(poly)
# numHyp = len(hyp)
print num
numTest = num/80
# numTestHyp = numHyp/80
polyTest = poly[:numTest]
polyTrain = poly[numTest:]
# hypTest = hyp[:numTestHyp]
# hypTrain = hyp[numTestHyp:]

with open('randFileEdges.tsv', 'w+') as outfile:
     writer = csv.writer(outfile, delimiter='\t')
     writer.writerows(randF)
# with open('hypFileEdges.tsv', 'w+') as outfile:
#      writer = csv.writer(outfile, delimiter='\t')
#      writer.writerows(hyp)
with open('polyFileEdgesRand.tsv', 'w+') as outfile:
     writer = csv.writer(outfile, delimiter='\t')
     writer.writerows(poly)
with open('polyTrainFileRand.tsv', 'w+') as outfile:
     writer = csv.writer(outfile, delimiter='\t')
     writer.writerows(polyTrain)
with open('polyTestFileRand.tsv', 'w+') as outfile:
     writer = csv.writer(outfile, delimiter='\t')
     writer.writerows(polyTest)

# with open('hypTestFile.tsv', 'w+') as outfile:
#      writer = csv.writer(outfile, delimiter='\t')
#      writer.writerows(hypTest)
#
# with open('hypTrainFile.tsv', 'w+') as outfile:
#      writer = csv.writer(outfile, delimiter='\t')
#      writer.writerows(hypTrain)

#file_path = datapath('randFileEdges.tsv')
print("POLY TO HYP")
model = PoincareModel(PoincareRelations("randFileEdges.tsv"), negative=2)
model.train(epochs=100)
#print(model.kv.most_similar('pitch.n.02', topn=10))
test = LinkPredictionEvaluation("polyTrainFileRand.tsv", "polyTestFileRand.tsv", model.kv)
print(test.evaluate())

recon = ReconstructionEvaluation("polyFileEdgesRand.tsv", model.kv)
print(recon.evaluate())
