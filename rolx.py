import snap
import os
import random
from nltk.corpus import wordnet as wn
import math
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
import networkx as nx

def generate_word_graph(hyp, poly, holo, type):
	if type == 0:
	    G1 = snap.TUNGraph.New()
	else:
		G1 = snap.TNGraph.New()
	hypedges = set()
	holoedges = set()
	polyedges = set()
	idToLemma = dict()
	lemmaToId = dict()
	count = 0
	for lemma_name in list(wn.all_lemma_names('n')):
		G1.AddNode(count)
		idToLemma[count] = lemma_name
		lemmaToId[lemma_name] = count
		count +=1
	for lemma_name in list(wn.all_lemma_names('n')):
		if hyp:
			for synset in wn.synsets(lemma_name, "n"):
				for synset2 in synset.hyponyms() + synset.instance_hyponyms():
					for lemma_name2 in synset2.lemma_names():
						lemma_name2 = lemma_name2.lower()
						if type in [0,1]:
							G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
							hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
						else:
							G1.AddEdge(lemmaToId[lemma_name2],lemmaToId[lemma_name])
							hypedges.add((lemmaToId[lemma_name2],lemmaToId[lemma_name]))
		if poly:
			for synset in wn.synsets(lemma_name, "n"):
				for lemma_name2 in synset.lemma_names():
					lemma_name2 = lemma_name2.lower()
					G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
					polyedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
		if holo:
			for synset in wn.synsets(lemma_name, "n"):
				for synset2 in synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms():
					for lemma_name2 in synset2.lemma_names():
						lemma_name2 = lemma_name2.lower()
						G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
						hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
	snap.DelSelfEdges(G1)
	return G1, idToLemma, lemmaToId, hypedges, polyedges, holoedges

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

def create_node_vectors(Graphs, iterations):
    features = np.zeros((Graphs[0].GetNodes(), 3 * len(Graphs)))
    for i,G in enumerate(Graphs):
        for node in G.Nodes():
            ego = {node.GetId()}
            for nbr in node.GetOutEdges():
                ego.add(nbr)
            egoedge = 0
            nonegoedge = 0
            for id in ego:
                for id2 in G.GetNI(id).GetOutEdges():
                    if id2 in ego:
                        egoedge += 1
                    else:
                        nonegoedge += 1
            features[node.GetId(), i*3:(i+1)*3] = [float(node.GetDeg()),float(egoedge/2),float(nonegoedge)]
    for _ in range(iterations):
        print("hi")
        original_length = features.shape[1]
        features = np.concatenate((features,np.zeros((Graphs[0].GetNodes(), original_length*(len(Graphs)*3 - 1)))), axis=1)
        for i,G in enumerate(Graphs):
            for node in G.Nodes():
                sumy = np.zeros((1,original_length))
                count = 0
                for id in node.GetOutEdges():
                    sumy += features[id, :original_length]
                    count +=1
                if count != 0:
                    meany = sumy/count
                else:
                    meany = sumy
                features[node.GetId(), original_length*(i*2+1):original_length*(i*2+2)] = sumy
                features[node.GetId(), original_length*(i*2+2):original_length*(i*2+3)] = meany
        features = trim(features)
    return features

def trim(features):
    return features

def extract_roles(features, r):
    print(features.shape)
    model = NMF(n_components=r, init='random', solver="mu", random_state=0)
    #W represents each nodes role membership
    W = model.fit_transform(features)
    return W

def create_superego(G, id,role, id_to_word, name, dir):
        G2 = snap.TUNGraph.New()
        G2.AddNode(id)
        for id2 in G.GetNI(id).GetOutEdges():
            if not G2.IsNode(id2):
                G2.AddNode(id2)
            for id3 in G.GetNI(id2).GetOutEdges():
                if not G2.IsNode(id3):
                    G2.AddNode(id3)
        for id2 in G2.Nodes():
            for id3 in G.GetNI(id2.GetId()).GetOutEdges():
                if G2.IsNode(id3):
                    G2.AddEdge(id2.GetId(),id3)
        snap.SaveEdgeList(G2, "test.txt", "")
        fig = plt.figure()
        nxG = nx.read_edgelist("test.txt", nodetype=int)
        nx.draw(nxG, with_labels=True)
        fig.savefig(str(dir) + "\\role" + str(role) + "node" + str(id) + id_to_word[id].name() + name + ".png")
        plt.close(fig)



G0 = generate_word_graph(True, False, False, 0)
snap.SaveEdgeList(G0, "G0.txt", "")
G1 = generate_word_graph(True, False, False, 1)
snap.SaveEdgeList(G1, "G1.txt", "")
G2 = generate_word_graph(True, False, False, 2)
snap.SaveEdgeList(G2, "G2.txt", "")

print(meme)
PolyG, Polyid, Polysynset, _,_,_ = generate_meaning_graph(False, True, False)
print(snap.GetMxScc(PolyG).GetNodes())
HypG, Hypid, Hypsynset, _,_,_ = generate_meaning_graph(True, False, False)
HoloG, Holoid, Holosynset, _,_,_ = generate_meaning_graph(False, False, True)
for k in Polyid:
    if Polyid[k] != Hypid[k]:
        print("oh no")


W = extract_roles(create_node_vectors([HypG, PolyG, HoloG], 3), 12)
print(W.shape)
roles = []
counts = dict()
nodes = dict()
for i in range(W.shape[0]):
    role = np.argmax(W[i])
    roles.append(role)
    if role not in nodes:
        nodes[role] = [i]
    else:
        nodes[role].append(i)
    if role not in counts:
        counts[role] = 1
    else:
        counts[role] += 1
for role in counts:
    os.mkdir(str(role))
    print(role,counts[role])
    sample = random.sample(nodes[role], min(20, counts[role]))
    for id in sample:
        os.mkdir(str(role)+ "\\" + str(Hypid[id].name()))
        create_superego(HypG, id, role, Hypid, "HYP",str(role)+ "\\" + str(Hypid[id].name()))
        create_superego(PolyG, id, role, Hypid, "POLY",str(role)+ "\\" + str(Hypid[id].name()))
        create_superego(HoloG, id, role, Hypid, "HOLO",str(role)+ "\\" + str(Hypid[id].name()))
