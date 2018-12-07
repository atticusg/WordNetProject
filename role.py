from nltk.corpus import wordnet as wn
import numpy as np
import snap
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
numImp = 9

def generate_meaning_graph(hyp, poly, holo):
    global numImp
    G1 = snap.TUNGraph.New()
    print wn.synsets('festoon')
    hypedges = set()
    holoedges = set()
    polyedges = set()
    idToSynset = dict()
    synsetToId = dict()
    count = 0
    numEl = 0
    for synset in list(wn.all_synsets('n')):
        if synset == wn.synset('benthos.n.01'):
            print synset
            numImp = count
            print count
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


def makeHist(d):
    n  = plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], d)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    name = "_word_holo_benthos"
    plt.title('Histogram'+ name)
    plt.show()

def getFeat():
    #G1, id2, synset2, _,_,_ = generate_word_graph(True, False, False)

    #G2, id2, synset2, _,_,_ = generate_word_graph(False, True, False)
    #G3, id2, synset2, _,_,_ = generate_word_graph(False, False, True)
    G4, id2, synset2, _,_,_ = generate_meaning_graph(True, False, False)
    #G5, id2, synset2, _,_,_ = generate_meaning_graph(False, True, False)
    #G6, id2, synset2, _,_,_ = generate_meaning_graph(False, False, True)
    #G7, id2, synset2, _,_,_ = generate_meaning_graph(True, False, True)

    degVec = {}
    egoNet = {}
    egoNetDeg = {}
    G = G4
    it = 0
    for node in G.Nodes():
        it += 1
        deg = node.GetDeg()
        nodeName = node.GetId()
        degVec[nodeName] = deg
        egoNet[nodeName] = 0
        egoNetDeg[nodeName] = 0
        commNeib = 0
        NodeVec = snap.TIntV()
        nodeList = snap.GetNodesAtHop(G,nodeName , 1, NodeVec, False)
        for node2 in NodeVec:
            nodeIt = G.GetNI(node2)
            dest = nodeIt.GetDeg()
            egoNetDeg[nodeName] += dest
            NodeVec2 = snap.TIntV()
            nodeList = snap.GetNodesAtHop(G,node2 , 1, NodeVec2, False)
            for el in NodeVec2:
                if el in NodeVec:
                    commNeib += 1
        egoNet[nodeName]  = deg + commNeib/2
        egoNetDeg[nodeName] = egoNetDeg[nodeName] - commNeib - deg
    print egoNet[numImp], egoNetDeg[numImp], degVec[numImp]

    featDictOne = {}
    for el in G.Nodes():
        numId = el.GetId()
        featVec = [degVec[numId], egoNet[numId], egoNetDeg[numId]]
        featDictOne[numId] = featVec
    for i in range(0,2):
        featDict = {}
        for el in G.Nodes():
            numId = el.GetId()
            featVec = recFeat(featDictOne, G, numId)
            featDict[numId] = featVec
        featDictOne = featDict
    getSim(featDictOne)

def getSim(featDict):
    print numImp
    feat9 = featDict[numImp]
    featVec9 = np.asarray(feat9)
    squareY = np.power(featVec9,2)
    sumY = np.sum(squareY)
    listSim = []
    for el in featDict:
        featVec = featDict[el]
        featVec = np.asarray(featVec)
        dotPro = np.dot(featVec, feat9)
        normx = np.linalg.norm(featVec)
        normy = np.linalg.norm(feat9)
        den = normx*normy
        if den == 0:
            sim = 0
        else:
            sim = dotPro/den
        listSim.append((sim, el))
    listSim = sorted(listSim, reverse=True)
    getHist(listSim)
    print listSim[:20]

def recFeat(featDictOne, G, node):
    featVec = featDictOne[node]
    featVec = np.asarray(featVec)
    sumVec = np.zeros(featVec.shape[0])
    meanVec = np.zeros(featVec.shape[0])
    num = 0
    NodeVec = snap.TIntV()
    nodeList = snap.GetNodesAtHop(G, node, 1, NodeVec, False)
    for el2 in NodeVec:
        num += 1
        featVec2 = featDictOne[el2]
        featVec2 = np.asarray(featVec2)
        sumVec = sumVec + featVec2
    if num > 0:
        meanVec = np.divide(sumVec,num)
    featVec = np.concatenate((featVec, sumVec))
    featVec = np.concatenate((featVec, meanVec))
    return featVec

def getHist(listSim):
    simMost = listSim[0][0]
    simLeast = 0
    simMost = simMost/20
    mapBuck = {}
    mapList = []
    mapList2 = []
    for el in listSim:
        sim = el[0]
        mapList.append(sim)
        for i in range (0, 20):
            if (i+1) not in mapBuck:
                mapBuck[i+1] = 0
            if sim <= simMost*(i+1):
                if (i+1) not in mapBuck:
                    mapBuck[i+1] = 0
                mapBuck[i+1] += 1
                break
    for el in mapBuck:
        mapList2.append(mapBuck[el])
    makeHist(mapList2)

getFeat()
