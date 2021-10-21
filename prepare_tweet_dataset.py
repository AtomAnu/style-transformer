from data import jsonl_reader, write_file
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

"""
Data:
    - hateful_founta_filt_nontox/train.jsonl -> train.pos dev.pos
    - hateful_founta_toxic_full/train_nort.jsonl -> train.neg dev.neg

"""

nontox_train_path = 'data/tweet/hateful_founta_filt_nontox/train.jsonl'
tox_train_path = 'data/tweet/hateful_founta_toxic_full/train_nort.jsonl'
val_path = 'data/tweet/val.jsonl'

nontox_train_text_list = jsonl_reader(nontox_train_path)
tox_train_text_list = jsonl_reader(tox_train_path)
# val_text_list = jsonl_reader(val_path)

print(len(nontox_train_text_list))
print(len(tox_train_text_list))
# print(len(val_text_list))

train_pos_path = 'data/tweet/train.pos'
train_neg_path = 'data/tweet/train.neg'
dev_pos_path = 'data/tweet/dev.pos'
dev_neg_path = 'data/tweet/dev.neg'
test_pos_path = 'data/tweet/test.pos'
test_neg_path = 'data/tweet/test.neg'



text_processor = TextPreProcessor(
    # terms that will be omitted
    omit=['url', 'email', 'percent', 'money', 'phone', 'user',
               'time', 'url', 'date', 'number'],
    # terms that will be normalized
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
               'time', 'url', 'date', 'number'],
    fix_html=True,  # fix HTML tokens
    # corpus from which the word statistics are going to be used
    # for word segmentation
    segmenter="twitter",
    # corpus from which the word statistics are going to be used
    # for spell correction
    corrector="twitter",
    unpack_hashtags=True,  # perform word segmentation on hashtags
    unpack_contractions=False,  # do not unpack contractions (can't -> can not)
    spell_correct_elong=False,  # spell correction for elongated words
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    # replacing emoticons with textual expressions
    dicts=[emoticons]
)

write_file(train_pos_path, nontox_train_text_list, text_processor)
write_file(dev_pos_path, nontox_train_text_list, text_processor)
write_file(train_neg_path, tox_train_text_list, text_processor)
write_file(dev_neg_path, tox_train_text_list, text_processor)
# write_file(test_pos_path, val_text_list, text_processor)
# write_file(test_neg_path, val_text_list, text_processor)

