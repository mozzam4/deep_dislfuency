from __future__ import print_function
#from tabulate import tabulate
from nltk.tag import CRFTagger
import os

TAGGER_PATH = "crfpostagger"   # pre-trained POS-tagger

tagger = CRFTagger()  # initialize tagger
tagger.set_model_file(TAGGER_PATH)

os.getcwd()
os.chdir('/home/bbb/dev/mozzam/deep_dislfuency')

try:
    import deep_disfluency
except ImportError:
    print ("no installed deep_disfluency package, pathing to source")
    import sys
    sys.path.append("../")

from deep_disfluency.tagger.deep_tagger import DeepDisfluencyTagger


# Initialize the tagger from the config file with a config number
# and saved model directory
MESSAGE = """1. Disfluency tagging on pre-segmented utterances
tags repair structure incrementally and other edit terms <e/>
(Hough and Schlangen Interspeech 2015 with an RNN)
"""
print (MESSAGE)
disf = DeepDisfluencyTagger(
    config_file="/home/bbb/dev/mozzam/deep_dislfuency/deep_disfluency/experiments/experiment_configs.csv",
    config_number=21,
    saved_model_dir="/home/bbb/dev/mozzam/deep_dislfuency/deep_disfluency/experiments/021/epoch_40"
    )

with open('/home/bbb/dev/mozzam/raw_asr_text.txt', 'r') as file:
    sentence = file.read()



with_pos = True
#activation = []
#tag_dic = {}
print ("tagging...")
if with_pos:
     # if POS is provided use this:
    for w in sentence.split():
        tag, dic, lis = disf.tag_new_word(w, pos=tagger.tag([unicode(w.lower())])[0][1])
        tag_dic = dic
        # act = [w.lower()]
        # act.extend(lis[len(lis)-1])
        # activation.append(act)

#To get the activations of the last layer
# print ("final tags:")
# for w, t in zip(sentence.split(), disf.output_tags):
#     print (w, "\t", t)

# sorted_tags = ['BLANK']
# for i in range(0,27):
#     for key, value in tag_dic.items():
#         if value == i:
#             sorted_tags.append(key)
#


#print(tabulate(activation, headers=sorted_tags))



final_str = ''
for w, t in zip(sentence.split(), disf.output_tags):
    if (t.find('<e/>') >= 0) or (t.find('<rm') >= 0):
        continue
    else:
        if final_str == '':
            final_str = w
        else:
            final_str = final_str + ' ' + w

disf.reset()  # resets the whole tagger for new utterance
with open("text_without_disfluency.txt", "w") as text_file:
    text_file.write(final_str)

