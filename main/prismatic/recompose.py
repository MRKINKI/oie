# -*- coding: utf-8 -*-
import itertools

class RECOMPOSE:
    def __init__(self):
        pass
    
    
    
    def get_obj_type(self,arc):                      #限制宾语的类型 ccomp
        #for _type in ['dobj','nmod:prep']:
        if 'dobj' in arc.children:
            return 'dobj'
        elif 'nmod:range' in arc.children:
            if len(arc.children['nmod:range']) == 1:
                return 'nmod:range'
        elif 'nmod:prep' in arc.children:
            if len(arc.children['nmod:prep']) == 1:
                return 'nmod:prep'
        else:
            return ''
        
    def get_subj_num(self,arc):
        if 'nsubj' not in arc.children:
            return 0 
        else:
            return len(arc.children['nsubj'])
    
    def get_compose_route(self,arcs):
            
        compose_route = []
        for arc in arcs:
            if arc.postag in ['VV','VC','VE','P'] and 'nsubj' in arc.children \
                and self.get_obj_type(arc):   #and arc.relation != 'conj':
                subjs = []
                verbs = []
                verbs.append(arc)
                if 'conj' in arc.children:
                    for conj_node in arc.children['conj']:
                        if arcs[conj_node].postag in ['VV','VC','VE','P'] and \
                            self.get_obj_type(arcs[conj_node]) and\
                            self.get_subj_num(arcs[conj_node]) == 0:
                                verbs.append(arcs[conj_node])
                
                subj = arc.children['nsubj'][0]
                subjs.append(arcs[subj])
                
                if 'conj' in arcs[subj].children:
                    for conj_node in arcs[subj].children['conj']:
                        subjs.append(arcs[conj_node])
                for verb in verbs:
                    objs = []
                    c_type = self.get_obj_type(verb)
                    if c_type:
                        obj = arcs[verb.children[c_type][0]]
                        objs.append(obj) 
                        if 'conj' in obj.children:
                            objs.extend([arcs[idx] for idx in obj.children['conj']])
    #                            print([s.word for s in subjs])
    #                            print([o.word for o in objs])
                        if len(subjs) == 1 or len(objs) == 1:
                            compose_route.extend(list(itertools.product(subjs,[verb],objs)))
                        elif len(subjs) == len(objs):
                            for subj,obj in zip(subjs,objs):
                                compose_route.append((subj,verb,obj))
        return compose_route