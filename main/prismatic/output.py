# -*- coding: utf-8 -*-


class FrameOutput:
    def __init__(self):
        pass
            
    def print_frame(self, frames):
        def sub_print(relation_name,  sub_frame):
            print(relation_name+'  '+sub_frame['word'])
            for sub_relation_name in sub_frame['SLR']:
                if sub_relation_name not in ['type'] and 'node' not in sub_relation_name:
                    print('  ' + sub_relation_name + '  '+' '.join(sub_frame['SLR'][sub_relation_name]))
                else:
                    print('  ' + sub_relation_name + '  '+sub_frame['SLR'][sub_relation_name])
        for frame_name in frames:
            print(frame_name)
            frame = frames[frame_name]

            for relation_name in frame:
                if isinstance(frame[relation_name], dict):
                    sub_print(relation_name, frame[relation_name])
                elif isinstance(frame[relation_name], str):
                    print(relation_name+'  '+frame[relation_name])
                elif isinstance(frame[relation_name], list):
                    for sub_frame in frame[relation_name]:
                        if isinstance(sub_frame, dict):
                            sub_print(relation_name, sub_frame)
                        else:
                            print(relation_name+'  '+sub_frame)
            print('\n')
            
    def print_change_frame(self, frames):
        for frame_name, frame in frames.items():
            print(frame_name)
            for relation, value in frame.items():
                print(relation+' '+str(value))
            print('\n')
