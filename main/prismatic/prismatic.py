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
        


if __name__ == '__main__':
    sentence = '日本队主帅西野朗的新闻：北京时间7月5日，日本足协召开新闻发布会，宣布西野朗不再担任日本队主教练。'
    sentence = '德国球星厄齐尔刚刚与阿森纳续约到2021年'
    #sentence = '2015年奥斯卡-罗梅罗加盟阿根廷竞技俱乐部，总计出场44次，为球队打入8粒进球，送出9次助攻。'
    
    #sentence = '张三和李四分别去了美国和印度'
    
    #sentence = '广州大桥长100米，高15米'
    #sentence = '梅西身高1.7米，体重80公斤'
    #sentence = '因为特大暴雪，中国国际航空公司于4月17日起关闭了秦皇岛机场'
    #sentence = '古代人说地球是圆的和方的'
    #sentence = '梅西出场44次，为球队打进10个进球'
    #sentence = '梅西需要对自己有信心'
    
    #sentence = '日本队主帅是谁'
#    sentence = '日本队赢了哥伦比亚,这是亚洲球队首次赢南美球队'
    #sentence = '亚洲球队首次赢南美球队是哪次'
    
#    sentence = '里皮带领球队2-0战胜广州富力'
#    sentence = '里皮带领球队战胜广州富力'
#    sentence = '里皮带领什么战胜广州富力'
#    
#    sentence = '中国女足对阵苹果女足'
#    
#    sentence = '中国女足对阵泰国女足'
#    sentence = '2018年女足亚洲杯揭幕战，中国女足4-0击败泰国女足取得开门红。'
    sentence = '毛泽东是中共创始人'
    sentence = '梅西加盟了哪只球队'

    
    pr = prismatic()
    fo = FrameOutput()
    fc = FrameChange()
    frames = pr.extract_frame(sentence)
    print(frames)
    fo.print_frame(frames)
    cframes = fc.change_frame(frames.copy())
    
    
    
    fo.print_change_frame(cframes)