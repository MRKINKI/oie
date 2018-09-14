
import collections


class BuildArcs:
    def __init__(self):
        pass

    def build_parse_arcs(self, deps, words, postags, netags):

        class Node:
            def __init__(self, head, relation, word, postag, netag, idx):
                self.head = head - 1
                self.relation = relation
                self.children = collections.defaultdict(list)
                self.postag = postag
                self.netag = netag
                self.word = word
                self.idx = idx
                self.children_indexes = set()

        _raw_arcs = [0 for i in range(len(deps))]
        for dep in deps:
            _raw_arcs[dep[2] - 1] = dep
        arcs = []
        _raw_arcs = [t for t in _raw_arcs if t != 0]
        for idx, dep in enumerate(_raw_arcs):
            _node = Node(head=dep[1],
                         relation=dep[0],
                         word=words[idx],
                         postag=postags[idx],
                         netag=netags[idx],
                         idx=idx)
            arcs.append(_node)
        for idx, arc in enumerate(arcs):
            if arc.head != -1:
                arcs[arc.head].children[arc.relation].append(idx)
                arcs[arc.head].children_indexes.add(idx)
        return arcs

    def revise_arcs(self, arcs):
        for idx, arc in enumerate(arcs):
            if 'cop' in arc.children:
                if len(arc.children['cop']) != 1:
                    break
                cop_index = arc.children['cop'][0]

                arcs[cop_index].head = -1
                arcs[cop_index].relation = 'ROOT'

                arcs[cop_index].children['dobj'].append(idx)
                arcs[cop_index].children_indexes.add(idx)
                arcs[idx].children_indexes.remove(cop_index)

                del arcs[idx].children['cop']

                if 'nsubj' in arc.children:
                    sbj_idx = min(arc.children['nsubj'])
                    arcs[cop_index].children['nsubj'].append(sbj_idx)
                    arcs[sbj_idx].head = cop_index
                    arcs[cop_index].children_indexes.add(sbj_idx)
                    arcs[idx].children_indexes.remove(sbj_idx)

                    arcs[idx].children['nsubj'].remove(sbj_idx)

                for _type in ['conj', 'ccomp']:
                    if _type == arc.relation:
                        head_idx = arcs[idx].head
                        arcs[cop_index].head = head_idx
                        arcs[cop_index].relation = arcs[idx].relation
                        arcs[head_idx].children_indexes.remove(idx)
                        arcs[head_idx].children_indexes.add(cop_index)
                        arcs[head_idx].children[_type].remove(idx)
                        arcs[head_idx].children[_type].append(cop_index)
                arcs[idx].relation = 'dobj'
                arcs[idx].head = cop_index
        return arcs

    def build_arcs(self, deps, words, postags, netags):
        arcs = self.build_parse_arcs(deps, words, postags, netags)
        arcs = self.revise_arcs(arcs)
        return arcs
