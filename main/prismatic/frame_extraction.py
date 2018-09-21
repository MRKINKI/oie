# -*- coding: utf-8 -*-
import collections


class NodeQueue:
    def __init__(self):
        self._list = collections.deque([])

    def add(self, node):
        if not len(self._list):
            self._list.append(node)
        else:
            m = 0
            for i in range(len(self._list)):
                if node.idx == self._list[i].idx:
                    m = 1
                    break
                if node.node_depth >= self._list[i].node_depth:
                    self._list.insert(0, node)
                    m = 1
                    break
            if m == 0:
                self._list.append(node)

    def pop(self):
        return self._list.popleft()

    def __len__(self):
        return len(self._list)


class FrameExtraction:
    
    def __init__(self):
        self.unused_relation = ['punct']

    def get_head_idx(self, arcs):
        for arc in arcs:
            if arc.relation == 'ROOT':
                idx = arc.idx
        return idx

    def second_level_frame(self, arcs, node):  # 最底层叶节点合并
        frame = {'ner': node.netag, 'pos': node.postag}
        for relation_type in node.children:
            if relation_type in self.unused_relation:
                continue
            child_idxes = node.children[relation_type]
            frame[relation_type] = []
            for child_idx in child_idxes:
                frame[relation_type].append(arcs[child_idx].word)
                frame[relation_type+'@node'] = str(arcs[child_idx].idx)
        return frame

    def first_level_frame(self, arcs, node):  # SLR second_level_relation
        frame = {'head_node': {'word': node.word, 'node': node.idx, 'SLR': {'ner': node.netag, 'pos': node.postag}}}
        for relation_type in node.children:
            if relation_type in self.unused_relation:
                continue
            for child_idx in node.children[relation_type]:
                frame[relation_type] = {'word': arcs[child_idx].word, 'node': arcs[child_idx].idx,
                                        'SLR': self.second_level_frame(arcs, arcs[child_idx])}
        return frame

    def add_depth_arcs(self, arcs, idx, depth):  # 每个节点记录距根节点距离及到叶节点距离
        depth = depth+1
        node = arcs[idx]
        node.node_depth = depth
        if not len(node.children_indexes):
            node.tree_depth = 0
            return 0
        depths = []
        for child_index in node.children_indexes:
            depths.append(self.add_depth_arcs(arcs, child_index, depth))
        node.tree_depth = max(depths) + 1
        return max(depths) + 1
        
    def build_frames(self, arcs):

        root_idx = self.get_head_idx(arcs)
        self.add_depth_arcs(arcs, root_idx, -1)
        
        depth_restriction = 2
        frames = {}
        node2frame_dict = {}
        frame_idx = 0        
        node_queue = NodeQueue()
        
        for node in arcs:
            if node.tree_depth == depth_restriction and node.idx != root_idx:
                frame = self.first_level_frame(arcs, node)
                frame_name = 'frame'+str(frame_idx)
                frames[frame_name] = frame
                node2frame_dict[node.idx] = frame_name
                frame_idx += 1        
        
        for frame_name, frame in frames.items():
            node_idx = arcs[frame['head_node']['node']].head
            node_queue.add(arcs[node_idx])
        
        if not len(node_queue):
            node_queue.add(arcs[root_idx])
        
        while len(node_queue):
            node = node_queue.pop()
            if node.relation == 'ROOT':
                frame = {'ROOT': {'word': node.word, 'node': node.idx,
                                  'SLR': {'ner': node.postag, 'pos': node.postag}}}
            else:
                frame = {'head_node': {'word': node.word, 'node': node.idx,
                                       'SLR': {'ner': node.netag, 'pos': node.postag}}}
            
            for relation_type in node.children:
                if relation_type in self.unused_relation:
                    continue
                frame[relation_type] = []   # 最末两级不是list 两级之上是list
                for child_idx in node.children[relation_type]:
                    if child_idx in node2frame_dict:
                        frame[relation_type].append(node2frame_dict[child_idx])
                    else:
                        frame[relation_type].append({'word': arcs[child_idx].word, 'node': arcs[child_idx].idx,
                                                     'SLR': self.second_level_frame(arcs, arcs[child_idx])})
            
            frame_name = 'frame' + str(frame_idx)
            frame_idx = frame_idx + 1
            node2frame_dict[node.idx] = frame_name
            frames[frame_name] = frame
            if node.relation == 'ROOT':
                break
            else:
                node_queue.add(arcs[node.head])
        return frames
