# -*- coding: utf-8 -*-

#from stanfordcorenlp import StanfordCoreNLP
from nlp.OpenNLP.stanfordcorenlp import StanfordCoreNLP
import collections

class buildArcs:
    def __init__(self,scn_host_or_path,scn_port=9000,lang = 'zh'):
        #self.scn = StanfordCoreNLP(scn_host_or_path,port = scn_port,lang=lang)
        self.scn = StanfordCoreNLP(path_or_host=scn_host_or_path, port=scn_port, lang='zh')
        
    def build_parse_arcs(self,raw_arcs,words,postags,netags):
        
        class node:
            def __init__(self,head,relation,word,postag,netag,idx):
                self.head = head - 1 
                self.relation = relation
                self.children = collections.defaultdict(list)
                self.postag = postag
                self.netag = netag
                self.word = word
                self.idx = idx
                self.children_indexes = set()
        _raw_arcs = [0 for i in range(len(raw_arcs))]
        for arc in  raw_arcs:
            _raw_arcs[arc[2] - 1] = arc
        arcs = []
        _raw_arcs = [t for t in _raw_arcs if t!=0]
        for idx,arc in enumerate(_raw_arcs):
            _node = node(head = arc[1],
                         relation = arc[0],
                        word = words[idx],
                        postag = postags[idx],
                        netag = netags[idx],
                        idx = idx)
            arcs.append(_node)
        for idx,arc in enumerate(arcs):
            if arc.head != -1:
                arcs[arc.head].children[arc.relation].append(idx)
                arcs[arc.head].children_indexes.add(idx)
        return arcs
        
    def revise_arcs(self,arcs):
        for idx,arc in enumerate(arcs):
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
                    
                for _type in ['conj','ccomp']:
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
    def build_arcs(self,sentence):
        scn_result = self.scn.mutiparse(sentence, models='pos,ner,depparse')
        words = [t[0] for t in scn_result]
        postags = [t[1] for t in scn_result]
        netags = [t[2] for t in scn_result]
        scn_raw_arcs = [(t[3][0],t[3][1],idx+1) for idx,t in enumerate(scn_result)]
                        
        dependencys = collections.Counter([t[0] for t in scn_raw_arcs])
        if dependencys['ROOT'] >1:
            return {},[]
        
        arcs = self.build_parse_arcs(scn_raw_arcs,words,postags,netags)
        arcs = self.revise_arcs(arcs)
        return arcs
        
    