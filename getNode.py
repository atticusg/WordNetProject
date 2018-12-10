import json
import networkx as nx
from nltk.corpus import wordnet as wn
import numpy as np
import random
import fastrand

import csv
def generate_word_graph(hyp, poly, holo):
    G1 = nx.Graph()
    hypedges = set()
    holoedges = set()
    polyedges = set()
    idToLemma = dict()
    lemmaToId = dict()
    count = 0
    for lemma_name in list(wn.lemmas('n')):
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
                        hypedges.add((lemma_name, lemma_name2))
        if poly:
            for synset in wn.synsets(lemma_name, "n"):
                for lemma_name2 in synset.lemmas():
                    #lemma_name2 = lemma_name2.lower()

                    #num = lemma_name2.rfind('.')
                    #lemma_name2 = lemma_name2[:num]
                    #num2 = lemma_name.rfind('.')
                    #lemma_name = lemma_name.synset()
                    lemma_name2 = synset
                    print(lemma_name2, lemma_name)
                    #G1.add_edge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                    polyedges.add((lemma_name, lemma_name2))
        if holo:
            for synset in wn.synsets(lemma_name, "n"):
                for synset2 in synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms():
                    for lemma_name2 in synset2.lemma_names():
                        lemma_name2 = lemma_name2.lower()
                        G1.add_edge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                        hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
    G1.remove_edges_from(G1.selfloop_edges())
    return G1, idToLemma, lemmaToId, hypedges, polyedges, holoedges


def getNode(G, listNode, id1, synset1):
    for node in listNode:
        getName = id1[node]
        print (getName, node)

G2, id2, synset2, hyp,poly, holo = generate_word_graph(False, True, True)
