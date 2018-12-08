import json
import networkx as nx
from nltk.corpus import wordnet as wn
import numpy as np
import random



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
def getNode(G, listNode, id1, synset1):
    for node in listNode:
        getName = id1[node]
        print (getName, node)

listMeaning =[3, 141, 175, 628, 666, 748, 890, 1077, 2004, 2399, 2551, 3060, 3116, 3208, 3408, 3447, 3628, 4215, 4220, 4331, 4662, 6265, 6482, 6649, 6926, 6959, 7333, 7664, 7789, 7839, 7994, 8478, 8687, 8770, 8891, 9186, 9680, 9780, 9850, 10561, 10571, 10584, 11409, 11511, 11525, 11789, 12858, 13083, 13291, 13424, 13524, 13590, 14384, 14573, 14627, 14717, 16311, 16758, 17610, 18728, 18860, 19285, 19343, 19766, 19819, 20273, 20420, 20895, 20972, 21325, 21999, 22033, 22152, 22154, 22199, 22416, 22418, 23443, 23586, 24829, 25153, 25259, 25669, 25734, 25763, 26567, 26871, 26888, 27183, 27313, 27495, 27618, 28121, 28196, 28490, 28621, 28836, 29190, 29607, 29759, 29878, 30246, 30647, 30663, 30845, 32587, 32609, 32667, 33124, 33282, 34165, 34262, 34902, 34961, 35088, 35307, 35393, 35654, 35783, 36235, 36268, 36342, 37331, 37530, 38456, 38667, 39892, 39911, 39932, 41178, 41836, 41889, 42053, 42479, 42549, 42871, 42991, 43212, 43596, 44065, 44068, 44195, 44306, 44501, 44587, 45219, 45278, 45361, 45362, 45406, 45475, 45696, 46074, 46103, 46197, 46774, 46838, 47113, 48580, 49048, 49057, 49419, 49739, 49855, 50024, 50186, 50821, 51036, 51300, 51953, 51956, 52041, 52050, 52136, 52964, 54811, 54838, 54923, 55397, 55705, 55950, 56016, 56031, 57254, 57500, 57611, 57658, 58238, 58717, 59753, 59846, 59902, 60299, 60691, 60789, 61615, 62293, 62439, 62816, 63217, 63719, 63918, 63941, 63986, 64202, 66534, 66557, 66935, 66939, 67085, 67175, 67236, 67415, 68316, 68506, 68749, 69179, 69459, 69712, 70103, 70255, 70317, 70563, 70794, 70832, 71106, 71499, 71850, 71929, 71966, 72041, 72339, 72381, 72747, 73258, 73321, 73856, 74032, 74579, 74867, 75064, 75524, 75922, 75954, 76033, 76907, 76910, 77568, 78255, 78336, 78657, 78878, 79670, 80174, 80232, 80897, 81098, 81311, 81633, 81690, 82138, 82191, 82559, 82772, 82834, 83556, 84596, 84695, 85358, 85375, 85538, 85919, 87241, 88101, 88445, 88540, 88697, 89198, 89438, 89448, 89452, 90606, 90648, 90943, 91155, 91554, 91707, 91753, 91772, 92086, 92298, 92556, 93026, 93716, 93895, 93968, 93973, 94112, 94576, 94976, 95122, 95501, 95866, 96713, 97327, 97792, 98177, 98221, 98315, 98884, 98968, 99084, 99584, 99831, 100378, 100479, 101067, 101118, 101216, 101292, 102507, 103132, 103318, 103594, 103869, 104448, 104709, 105908, 106264, 106323, 106331, 106351, 106375, 106645, 106712, 106889, 107180, 108108, 108208, 108373, 109243, 109274, 109428, 109614, 109694, 109807, 109922, 110554, 110764, 111207, 111316, 112588, 112649, 112931, 113099, 113169, 113170, 113214, 113343, 113530, 113710, 114254, 114396, 114503, 115482, 115705, 116133, 116331, 116887, 117062, 117063, 117098]
listWord = [3, 24, 36, 41, 43, 51, 95, 125, 126, 127, 128, 168, 328, 581, 606, 699, 723, 927, 1245, 1264, 1594, 1692, 1738, 1873, 2012, 2013, 2028, 2034, 2273, 2301, 2506, 2741, 2774, 2787, 2825, 3162, 3199, 3276, 3723, 4255, 4260, 4297, 4303, 4319, 4371, 4559, 4560, 4632, 4743, 4766, 4768, 4802, 4807, 4839, 4842, 5162, 5185, 5200, 5207, 5224, 5234, 5421, 5485, 5487, 5599, 5627, 5629, 5637, 5657, 5741, 5744, 5827, 5878, 6007, 6009, 6319, 6398, 6473, 6683, 7449, 9173, 10926, 12694, 12717, 13192, 14409, 15328, 15669, 16255, 16256, 16350, 16872, 16873, 16874, 16875, 16876, 17263, 17264, 17614, 17971, 18137, 18167, 18445, 18483, 18484, 18485, 18841, 18923, 18990, 18991, 19363, 19560, 19580, 19622, 20095, 20445, 20463, 20608, 21114, 21839, 21885, 21886, 21887, 22468, 22546, 22579, 22580, 22586, 23359, 23360, 23441, 23581, 23847, 24646, 24647, 24708, 24709, 25393, 25801, 26081, 26090, 26421, 26423, 26861, 26862, 27347, 27728, 27789, 27791, 28063, 28086, 28217, 28219, 28228, 28359, 28409, 28410, 28496, 28500, 28600, 28705, 28754, 28838, 30615, 30617, 30722, 30963, 30967, 31133, 31154, 31155, 31163, 31175, 31177, 31254, 31262, 31325, 31463, 31466, 31482, 31487, 31636, 31662, 31663, 31769, 31784, 31807, 31865, 31892, 31893, 31940, 31970, 31991, 31998, 32014, 32076, 32094, 32129, 32297, 32298, 32313, 32451, 32453, 32500, 32515, 32715, 32716, 32724, 32726, 33015, 33791, 33824, 33983, 34014, 34180, 34216, 34382, 34716, 34721, 34752, 34794, 34930, 35074, 35250, 35332, 35402, 35403, 35429, 35434, 35503, 35540, 35583, 35711, 35816, 36025, 36136, 36278, 36279, 36291, 36412, 36626, 36683, 36718, 37173, 37897, 37918, 37929, 37951, 37976, 38378, 38392, 38459, 38471, 38487, 38515, 38946, 38947, 38957, 39454, 39544, 39611, 39624, 39625, 39638, 39735, 39773, 40143, 40163, 40302, 40304, 40342, 40499, 40523, 40561, 40562, 40566, 40765, 41028, 42256, 43501, 43661, 43912, 44263, 44557, 44868, 44954, 46071, 46141, 46585, 46839, 46915, 49334, 49707, 51176, 51185, 51298, 52626, 53712, 55989, 56167, 56422, 56423, 57613, 58100, 58101, 62017, 62042, 62232, 66635, 70663, 70707, 70790, 70880, 70881, 70893, 71129, 71217, 71411, 71888, 72079, 72370, 72372, 72415, 72485, 72534, 72663, 72669, 72915, 73372, 73540, 73660, 73785, 73798, 74231, 74611, 74673, 75294, 75699, 77224, 77260, 77280, 77340, 77455, 77553, 77575, 77819, 78103, 78345, 78346, 79956, 81128, 81818, 81870, 81900, 82112]
#G1, id1, synset1, _,_,_ = generate_word_graph(False, True, False)
G2, id2, synset2, _,_,_ = generate_meaning_graph(False, True, False)
listMeaning = [101, 31631, 40157, 71890, 72375]
getNode(G2, listMeaning, id2, synset2)

#getNode(G1, listWord, id1, synset1)