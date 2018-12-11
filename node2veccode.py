import argparse
import numpy as np
import matplotlib.pyplot as plt
from networkx import nx
import node2vec
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec
import snap
'''
Reference implementation of node2vec.

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec
Knowledge Discovery and Data Mining (KDD), 2016
'''
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


def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=1, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--p', type=float, default=1,
	                    help='Return hyperparameter. Default is 1.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

def read_graph():
	'''
	Reads the input network in networkx.
	'''
	if args.weighted:
		G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G

def learn_embeddings(walks, dimension, window_size, output):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	walks = [map(str, walk) for walk in walks]
	model = Word2Vec(walks, size=dimension, window=window_size, min_count=0, sg=1, workers=8, iter=1)
	model.wv.save(output)
	return model.wv

#G0, Polyid, Polysynset, _,_,_ = generate_word_graph(True, False, False, 0)
#snap.SaveEdgeList(G0, "G0.txt", "")
#G1, Polyid, Polysynset, _,_,_ = generate_word_graph(True, False, False, 1)
#snap.SaveEdgeList(G1, "G1.txt", "")
#G2, Polyid, Polysynset, _,_,_ = generate_word_graph(True, False, False, 2)
#snap.SaveEdgeList(G2, "G2.txt", "")
G0 = nx.read_edgelist("G0.txt", nodetype=int)
for edge in G0.edges():
	G0[edge[0]][edge[1]]['weight'] = 1.0
G1 = nx.read_edgelist("G1.txt", nodetype=int, create_using=nx.DiGraph())
for edge in G1.edges():
	G1[edge[0]][edge[1]]['weight'] = 1.0
G2 = nx.read_edgelist("G2.txt", nodetype=int, create_using=nx.DiGraph())
for edge in G2.edges():
	G2[edge[0]][edge[1]]['weight'] = 1.0
p = 100000
q = 1
walk_length = 20
window_size = 20
num_walks = 100
dimension = 50
G1 = node2vec.Graph(G1, False, p, q)
G1.preprocess_transition_probs()
walks = G1.simulate_walks(num_walks, walk_length)
wordvecs = learn_embeddings(walks, dimension, window_size, "uptree.emb")
G0 = node2vec.Graph(G0, False, p, q)
G0.preprocess_transition_probs()
walks = G0.simulate_walks(num_walks, walk_length)
wordvecs = learn_embeddings(walks, dimension, window_size, "undir.emb")
G2 = node2vec.Graph(G2, False, p, q)
G2.preprocess_transition_probs()
walks = G2.simulate_walks(num_walks, walk_length)
wordvecs = learn_embeddings(walks, dimension, window_size, "downtree.emb")
