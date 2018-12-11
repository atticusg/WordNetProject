from nltk.corpus import wordnet as wn
import json
import numpy as np
import community
import snap
import random
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

def generate_meaning_graph(hyp, poly, holo):
    G1 = snap.TUNGraph.New()
    hypedges = set()
    holoedges = set()
    polyedges = set()
    idToSynset = dict()
    synsetToId = dict()
    count = 0
    for synset in list(wn.all_synsets('n')):
        G1.AddNode(count)
        idToSynset[count] = synset
        synsetToId[synset] = count
        count +=1
    for synset in list(wn.all_synsets('n')):
        if hyp:
            for synset2 in synset.hyponyms() + synset.instance_hyponyms():
                G1.AddEdge(synsetToId[synset], synsetToId[synset2])
                hypedges.add((synsetToId[synset], synsetToId[synset2]))
        if poly:
            for lemma_name in synset.lemma_names():
                for synset2 in wn.synsets(lemma_name, "n"):
                    G1.AddEdge(synsetToId[synset], synsetToId[synset2])
                    polyedges.add((synsetToId[synset], synsetToId[synset2]))
        if holo:
            for synset2 in synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms():
                G1.AddEdge(synsetToId[synset], synsetToId[synset2])
                holoedges.add((synsetToId[synset], synsetToId[synset2]))
    snap.DelSelfEdges(G1)
    return G1,idToSynset, synsetToId, hypedges, polyedges, holoedges

def com_rating(com, id):
    lch = id[com[0]]
    for thing in com[1:]:
        syn = id[thing]
        lch = lch.lowest_common_hypernyms(syn)[0]
    min_depth = lch.min_depth()
    q = [lch]
    subtree = set()
    subtree.add(lch)
    count = 0
    while len(q) != 0:
        count += 1
        cur = q[0]
        q = q[1:]
        for syn in cur.hyponyms() + cur.instance_hyponyms():
            subtree.add(syn)
            q.append(syn)
        break
    ratio = float(len(com))/float(len(subtree))
    return min_depth, ratio


print("hi")
G0, Polyid, Polysynset, _,_,_ = generate_meaning_graph(False, True, False)
print("hi")
G0 = snap.GenConfModel(G0)
snap.SaveEdgeList(G0, "G0.txt", "")
G0 = nx.read_edgelist("G0.txt", nodetype=int)
dendo = community.generate_dendrogram(G0)
print("hi")
prev_part= None
results = dict()
count = 0
for part in dendo:
    count +=1
    results[count] = [0.0,0.0,0.0]
    if prev_part is None:
        prev_part = dict()
        for com in part.values():
            prev_part[com] = [nodes for nodes in part.keys() if part[nodes] == com]
            md, rat = com_rating(prev_part[com], Polyid)
            results[count][0] += md
            results[count][1] += rat
            results[count][2] += 1
    else:
        new_part = dict()
        for com in part.values():
            temps = [nodes for nodes in part.keys() if part[nodes] == com]
            new_part[com] = []
            for key in temps:
                new_part[com] += prev_part[key]
            md, rat = com_rating(new_part[com], Polyid)
            results[count][0] += md
            results[count][1] += rat
            results[count][2] += 1
        prev_part= new_part
for k in results:
    print(k, results[k][0]/results[k][2],results[k][1]/results[k][2])
