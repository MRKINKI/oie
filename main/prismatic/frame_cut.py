class FrameCut:
    def __init__(self):
        self.routes = [{'sbj': [{'frame_item': 'nsubj'}],
                        'pred': [{'frame_item': 'ROOT',
                                  'pos': ['VV', 'VC', 'VE']},
                                 {'frame_item': 'head_node',
                                  'pos': ['VV', 'VC', 'VE']}],
                        'obj': [{'frame_item': 'dobj'}]}]
        self.conj = 'conj'

    def frame_route_match(self, frame, route):
        for route_key, route_value in route.items():
            for sub_match_frame in route_value:
                match_frame_item = False
                match_frame_child_item_formal = False if len(sub_match_frame) > 1 else True
                frame_item = sub_match_frame['frame_item']
                if frame_item in frame:
                    match_frame_item = True

                for frame_child_item, frame_child_value in sub_match_frame.items():
                    if frame_child_item != 'frame_item':
                        frame_child_item_formal = frame_item + '@' + frame_child_item
                        sub_match_frame_value = frame.get(frame_child_item_formal, '')
                        if sub_match_frame_value in frame_child_value:
                            match_frame_child_item_formal = True
                            break
                if match_frame_item and match_frame_child_item_formal:
                    break
            if not match_frame_item or not match_frame_child_item_formal:
                return False
        return True

    def get_master_frame(self, frames, route):
        master_frames = []
        for frame_id, frame in frames.items():
            if self.frame_route_match(frame, route):
                master_frames.append(frame)
        return master_frames

    def extract(self, frame, route):
        result = route.copy()
        for route_key, route_value in route.items():
            result[route_key] = frame[route_value]
        return result

    def get_conj_frame_id(self, frame):
        conj_frame_ids = []
        if self.conj in frame:
            conjs = frame[self.conj]
            if isinstance(conjs, list):
                conj_frame_ids.extend(conjs)
            elif isinstance(conjs, str):
                conj_frame_ids.append(conjs)
        return conj_frame_ids

    def del_frame_item(self, frame, route, item):
        sub_match_frames = route[item]
        copy_frame = frame.copy()
        for sub_match_frame in sub_match_frames:
            frame_item = sub_match_frame['frame_item']
            for sub_frame_item in copy_frame:
                if frame_item in sub_frame_item and sub_frame_item in frame:
                    del frame[sub_frame_item]

    def frame_conj(self, master_frame, frames, route):
        conj_frames = []
        conj_frame_ids = self.get_conj_frame_id(master_frame)
        for conj_frame_id in conj_frame_ids:
            conj_frame = frames[conj_frame_id]
            master_frame_copy = master_frame.copy()

            self.del_frame_item(master_frame_copy, route, 'pred')
            self.del_frame_item(master_frame_copy, route, 'obj')
            if 'conj' in master_frame_copy:
                del master_frame_copy['conj']

            master_frame_copy.update(conj_frame)
            conj_frames.append(master_frame_copy)
        return conj_frames

    def match_frame_extract(self, master_frame, frames, route):
        match_frames = [master_frame]
        conj_frames = self.frame_conj(master_frame, frames, route)
        match_frames.extend(conj_frames)
        return match_frames

    def item_conj(self, cand_frame):
        pass
        #for cand_frame in

    def run(self, frames):
        results = []
        for route in self.routes:
            master_frames = self.get_master_frame(frames, route)
            for master_frame in master_frames:
                match_frames = self.match_frame_extract(master_frame, frames, route)
                results.extend(match_frames)
        return results
