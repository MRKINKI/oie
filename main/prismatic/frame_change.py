# -*- coding: utf-8 -*-


class FrameChange:
    def __init__(self):
        pass
    
    def get_change_sub_frame(self, relation, sub_frame):
        frame = {}
        if isinstance(sub_frame, dict):
            frame[relation] = sub_frame['word']
            frame[relation+'@node'] = sub_frame['node']
            for sub_relation, value in sub_frame['SLR'].items():
                if sub_relation == 'ner' and '-' in value:
                    value = value.split('-')[1]
                if isinstance(value, list):
                    if len(value) > 1:
                        value = value
                    else:
                        value = value[0]
                    # value = ' '.join(value)
                frame[relation+'@'+sub_relation] = value
        return frame
    
    def change_frame(self, frames):
        for frame_name, frame in frames.items():
            new_frame = {}
            for relation, sub_frame in frame.items():
                new_frame.update(self.get_change_sub_frame(relation, sub_frame))
                if isinstance(sub_frame, list):
                    # print(sub_frame)
                    if len(sub_frame) > 1:
                        new_frame[relation] = sub_frame
                    else:
                        sub_frame = sub_frame[0]
                        if isinstance(sub_frame, str):
                            new_frame[relation] = sub_frame
                        else:
                            new_frame.update(self.get_change_sub_frame(relation, sub_frame))
            frames[frame_name] = new_frame
        return frames
