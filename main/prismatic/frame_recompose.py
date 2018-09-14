# -*- coding: utf-8 -*-


class FrameRecompose:
    def __init__(self):
        self.verb_type = ['VV','VC','VE','P']
        self.sbj_type = ['nsubj']
        self.obj_type = ['dobj','nmod:range','nmod:prep']        #注意顺序
        self.coord_type = 'conj'
        self.root = 'ROOT'
        self.head_node = 'head_node'        
        
    def get_head_node_type(self,frame):
        return frame[self.root] if self.root in frame else frame[self.head_node]

    def get_sbj_type(self,frame):
        for sbj_type in self.sbj_type:
            if sbj_type in frame:
                return sbj_type
        return ''
        
    def get_obj_type(self,frame):
        for obj_type in self.obj_type:
            if obj_type in frame:
                return obj_type
        return ''
    
    def get_master_frame(self,frames):
        master_frames = []
        for frame in frames:
            sbj_type = self.get_sbj_type(frame)
            obj_type = self.get_obj_type(frame)
            if sbj_type and  obj_type and self.coord_type in frame:
                master_frames.append((frame,sbj_type,obj_type))
        return master_frames
            
    def recompose_frame(self,frames):
        master_frames = self.get_master_frame(frames)
        
        for frame in master_frames:
            coord_terms = frame[self.coord_type]
            if not isinstance(coord_terms,list):
                print(coord_terms)
                return
            for coord_term in coord_terms:
                if isinstance(coord_term,str):
                    coord_frame = frames[coord_term]
                    
        



