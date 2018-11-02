from nltk.corpus import wordnet as wn
import snap
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
            for lemma in wn.lemmas(lemma_name, "n"):
                for lemma2 in lemma.hyponyms() + lemma.instance_hyponyms():
                    G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma2.name()])
                    hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma2.name()]))
        if poly:
            for synset in wn.synsets(lemma_name, "n"):
                for lemma_name2 in synset.lemma_names():
                    lemma_name2 = lemma_name2.lower()
                    G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma_name2])
                    polyedges.add((lemmaToId[lemma_name], lemmaToId[lemma_name2]))
        if holo:
            for lemma in wn.lemmas(lemma_name, "n"):
                for lemma2 in lemma.member_holonyms() + lemma.part_holonyms() + lemma.substance_holonyms():
                    G1.AddEdge(lemmaToId[lemma_name], lemmaToId[lemma2.name()])
                    hypedges.add((lemmaToId[lemma_name], lemmaToId[lemma2.name()]))
    snap.DelSelfEdges(G1)
    return G1, idToLemma, lemmaToId, hypedges, polyedges, holoedges
