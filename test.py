from main.tool import tokenize
from main.tool.sentence.sentence_split import SentenceSplitter
from main.tool.arcs.build_arcs import BuildArcs
from main.tool.clean.cleaner import Cleaner
from main.prismatic.prismatic import Prismatic


if __name__ == '__main__':
    text = '鲢鱼（学名：Hypophthalmichthys molitrix），又叫白鲢、跳鲢、水鲢、鲢子等，' \
           '为辐鳍鱼纲鲤形目鲤科的其中一种，是著名的四大家鱼之一。'
    sp = SentenceSplitter()
    tokenizer = tokenize.get_class('corenlp')()
    ba = BuildArcs()
    cleaner = Cleaner()
    text = cleaner.clean(text)
    pri = Prismatic()
    print(text)
    sentences = sp.split(text)
    sentence = sentences[0]
    deps, words, postags, netags = tokenizer.tokenize(sentence)
    arcs = ba.build_arcs(deps, words, postags, netags)
    frames = pri.extract_frame(arcs)
    pri.frame_output.print_frame(frames)
    cfames = pri.frame_change.change_frame(frames.copy())
    # for arc in arcs:
    #     print(arc.word, arc.postag, arc.relation, arc.head)
    # print(deps)
