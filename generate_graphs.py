from nltk.corpus import wordnet as wn
import numpy as np
import snap
import random
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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


def generate_word_graph(hyp, poly, holo):
    G1 = snap.TUNGraph.New()
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
                        G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                        hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
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

def make_log_degree_graph(Graphs):
    for tup in Graphs:
        G,label,color = tup
        results = dict()
        for node in G.Nodes():
            if node.GetDeg() in results:
                results[node.GetDeg()] +=1
            else:
                results[node.GetDeg()] =1
        x = []
        y = []
        for key in results:
            x.append(key)
            y.append(results[key])
        inds = np.argsort(x)
        x2 = []
        y2 = []
        for ind in inds:
            x2.append(x[ind])
            y2.append(y[ind])
        plt.loglog(x2, y2, color = color, label = label)
    plt.show()

def make_path_graph(Graphs):
    for tup in Graphs:
        G,label,color = tup
        results = dict()
        bigtotal = 0.
        bigcount = 0.
        for node in G.Nodes():
            pathtotal = 0.
            count = 0.
            for node2 in G.Nodes():
                pathtotal += snap.GetShortPath(G,node,node2)
                count +=1
            if pathtotal/count in results:
                results[pathtotal/count] +=1
            else:
                results[pathtotal/count] =1
            bigtotal += pathtotal
            bigcount += pathcount
        print(label, bigtotal/bigcount)
        x = []
        y = []
        for key in results:
            x.append(key)
            y.append(results[key])
        inds = np.argsort(x)
        x2 = []
        y2 = []
        for ind in inds:
            x2.append(x[ind])
            y2.append(y[ind])
        plt.loglog(x2, y2, color = color, label = label)
    plt.show()


G1, id2, synset2, _,_,_ = generate_word_graph(True, False, False)
print(G1.GetNodes())
G2, id2, synset2, _,_,_ = generate_word_graph(False, True, False)
G3, id2, synset2, _,_,_ = generate_word_graph(False, False, True)
snap.PlotShortPathDistr(G1, "hyp", "graph - shortest path", 1000)
snap.PlotShortPathDistr(G2, "poly", "graph - shortest path",1000)
snap.PlotShortPathDistr(G3, "mero", "graph - shortest path",1000)
make_log_degree_graph([(G1,"hypernym","b"),(G2,"polysemy", "y"),(G3,"meronymy","r")])










print(meme)

G2, id2, synset2, _,_,_ = generate_meaning_graph(True, False, False)
print(G2.GetNodes())
print(G2.GetEdges())
GW = snap.GetMxScc(G2)
print(GW.GetNodes())
print(GW.GetNodes(),"lolhyp")

G3, id2, synset2, _,_,_ = generate_meaning_graph(False, False, True)
print(G3.GetNodes())
print(G3.GetEdges())
GW = snap.GetMxScc(G2)
print(GW.GetNodes())
print(GW.GetNodes(),"lolmero")

G4, id2, synset2, _,_,_ = generate_meaning_graph(True, False, True)
print(G4.GetNodes())
print(G4.GetEdges())
GW = snap.GetMxScc(G4)
print(GW.GetNodes())
print(GW.GetNodes(),"lolmerohyp")

G, id, synset, _,_,_ = generate_meaning_graph(False, True, False)
print(G.GetNodes())
print(G.GetEdges())
Gs = snap.TCnComV()
snap.GetSccs(G,Gs )
count = 0
for G3 in Gs:
    print(G3.Len())
    count +=1
    if count >10:
        break
print("lolpoly")

paths = [0] * 50
count = 0
for edge in G.Edges():
    path = snap.GetShortPath(G2, synset2[id[edge.GetSrcNId()]],synset2[id[edge.GetDstNId()]])
    paths[path] += 1
    if path == 2:
        print(id[edge.GetSrcNId()],id[edge.GetDstNId()])
    count +=1
    if count % 10000 == 0:
        print(count)
        print(paths)

paths2 = [0] * 50
count = 0
for edge in G.Edges():
    path = snap.GetShortPath(G4, synset2[id[edge.GetSrcNId()]],synset2[id[edge.GetDstNId()]])
    paths2[path] += 1
    count +=1
    if count % 10000 == 0:
        print(count)
        print(paths2)
paths3 = [0] * 50
count = 0
ids = [i for i in range(G.GetNodes())]
for _ in G.Edges():
    path = snap.GetShortPath(G4, synset2[id[random.choice(ids)]],synset2[id[random.choice(ids)]])
    paths3[path] += 1
    count +=1
    if count % 10000 == 0:
        print(count)
        print(paths3)
plt.plot(paths, color = "r")
plt.plot(paths2, color = "y")
plt.plot(paths3, color = "b")
plt.show()
