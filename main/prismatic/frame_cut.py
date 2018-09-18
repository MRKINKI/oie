class FrameCut:
    def __init__(self):
        self.routes = [{'sbj': 'nsubj', 'pred': 'ROOT', 'obj': 'dobj'}]
        self.conj = 'conj'

    def frame_route_match(self, frame, route):
        for route_key, route_value in route.items():
            if route_value not in frame:
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

    def match_frame_extract(self, master_frame, frames, route):
        match_frames = [master_frame]
        conj_frame_ids = self.get_conj_frame_id(master_frame)
        for conj_frame_id in conj_frame_ids:
            conj_frame = frames[conj_frame_id]
            master_frame_copy = master_frame.copy()
            del master_frame_copy[route['pred']]
            del master_frame_copy[route['obj']]
            master_frame_copy.update(conj_frame)
            match_frames.append(master_frame_copy)
        return match_frames

    def run(self, frames):
        results = []
        for route in self.routes:
            master_frames = self.get_master_frame(frames, route)
            for master_frame in master_frames:
                match_frames = self.match_frame_extract(master_frame, frames, route)
                results.extend(match_frames)
        return results
