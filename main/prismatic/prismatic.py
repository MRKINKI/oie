# -*- coding: utf-8 -*-

from .frame_extraction import FrameExtraction
from .output import FrameOutput
from .frame_change import FrameChange


class Prismatic:
    def __init__(self):
        self.frame_extraction = FrameExtraction()
        self.frame_output = FrameOutput()
        self.frame_change = FrameChange()
    
    def extract_frame(self, arcs):
        frames = self.frame_extraction.build_frames(arcs)
        return frames
