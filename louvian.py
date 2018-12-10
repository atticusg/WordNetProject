from nltk.corpus import wordnet as wn
import numpy as np
import snap
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#import louvain
import json

import networkx as nx
from community import community_louvain



def generate_meaning_graph(hyp, poly, holo):
    G1 = nx.Graph()
    hypedges = set()
    holoedges = set()
    polyedges = set()
    idToSynset = dict()
    synsetToId = dict()
    count = 0
    numSame = 0
    for synset in list(wn.all_synsets('n')):
        G1.add_node(count)
        idToSynset[count] = synset
        synsetToId[synset] = count
        count +=1
    for synset in list(wn.all_synsets('n')):
        if hyp:
            for synset2 in synset.hyponyms() + synset.instance_hyponyms():
                G1.add_edge(synsetToId[synset], synsetToId[synset2])
                hypedges.add((synsetToId[synset], synsetToId[synset2]))
        if poly:
            for lemma_name in synset.lemma_names():
                for synset2 in wn.synsets(lemma_name, "n"):
                    if synset == synset2:
                        numSame += 1
                    G1.add_edge(synsetToId[synset], synsetToId[synset2])
                    polyedges.add((synsetToId[synset], synsetToId[synset2]))
        if holo:
            for synset2 in synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms():
                G1.add_edge(synsetToId[synset], synsetToId[synset2])
                holoedges.add((synsetToId[synset], synsetToId[synset2]))
    print (numSame, "num")
    G1.remove_edges_from(G1.selfloop_edges())
    return G1,idToSynset, synsetToId, hypedges, polyedges, holoedges


def generate_word_graph(hyp, poly, holo):
    G1 = nx.Graph()
    hypedges = set()
    holoedges = set()
    polyedges = set()
    idToLemma = dict()
    lemmaToId = dict()
    count = 0
    for lemma_name in list(wn.all_lemma_names('n')):
        G1.add_node(count)
        idToLemma[count] = lemma_name
        lemmaToId[lemma_name] = count
        count +=1
    for lemma_name in list(wn.all_lemma_names('n')):
        if hyp:
            for synset in wn.synsets(lemma_name, "n"):
                for synset2 in synset.hyponyms() + synset.instance_hyponyms():
                    for lemma_name2 in synset2.lemma_names():
                        lemma_name2 = lemma_name2.lower()
                        G1.add_edge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                        hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
        if poly:
            for synset in wn.synsets(lemma_name, "n"):
                for lemma_name2 in synset.lemma_names():
                    lemma_name2 = lemma_name2.lower()
                    G1.add_edge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                    polyedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
        if holo:
            for synset in wn.synsets(lemma_name, "n"):
                for synset2 in synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms():
                    for lemma_name2 in synset2.lemma_names():
                        lemma_name2 = lemma_name2.lower()
                        G1.add_edge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                        hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
    G1.remove_edges_from(G1.selfloop_edges())
    return G1, idToLemma, lemmaToId, hypedges, polyedges, holoedges

G1, id1, synset1, _,_,_ = generate_word_graph(True, False, False)
G2, id2, synset2, _,_,_ = generate_meaning_graph(True, False, False)
print (G1.size(), len(G1))
print (G2.size(), len(G2))
print ("yes")
#partition = community_louvain.best_partition(G1)
#partition2 = community_louvain.best_partition(G2)
dendo = community_louvain.generate_dendrogram(G1)
for level in range(len(dendo)) :
    newPart = community_louvain.partition_at_level(dendo, level)
    #print("partition at level", level, "is", newPart)
    size = float(len(set(newPart.values())))
    print (size, level, "size")
#size1 = float(len(set(partition.values())))
#size2 = float(len(set(partition2.values())))
dendo2 = community_louvain.generate_dendrogram(G2)
for level in range(len(dendo2)) :
    newPart = community_louvain.partition_at_level(dendo2, level)
    #print("partition at level", level, "is", newPart)
    size = float(len(set(newPart.values())))
    print (size, level, "size2")
#size1 = float(len(set(partition.values())))
#size2 = float(len(set(partition2.values())))
#print (size1, size2)
# print ("here")
# nx.write_graphml(G1, "testG1.graphml")
# print ("here")
# count = 0
# listPar1 = {}
# listPar2 = {}
# for com in set(partition.keys()) :
#     bucket = partition[com]
#     if bucket in listPar1:
#         listVal = listPar1[bucket]
#         listVal.append(com)
#         listPar1[bucket] = listVal
#     else:
#         listPar1[bucket] = [com]
#     count += 1
#     print (count, "1")
# count = 0
# with open('fileDictWord.json', 'w') as outfile:
#     json.dump(listPar1, outfile)
# for com in set(partition2.values()) :
#     print (count, "2")
#     list_nodes = [nodes for nodes in partition2.keys()
#     if partition2[nodes] == com]
#     listPar2[count] = list_nodes
#     count += 1
#
# with open('fileDictMeaning.json', 'w') as outfile:
#     json.dump(listPar2, outfile)
