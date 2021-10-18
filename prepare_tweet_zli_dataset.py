from data import jsonl_reader, write_file
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

"""
Data:
    - hateful_founta_filt_nontox/train.jsonl -> train.pos dev.pos
    - hateful_founta_filt_tox/train.jsonl -> train.neg dev.neg
    - val.jsonl -> test.pos test.neg

"""

tox_zli_path = 'train_zli_toxic.jsonl'
nontox_zli_path = 'train_zli_nontoxic.jsonl'

tox_zli_title = jsonl_reader(tox_zli_path, key='title')
tox_zli_text = jsonl_reader(tox_zli_path)
nontox_zli_title = jsonl_reader(nontox_zli_path, key='title')
nontox_zli_text = jsonl_reader(nontox_zli_path)

print('Sanity Check')

print('tox title: {}'.format(len(tox_zli_title)))
print('tox text: {}'.format(len(tox_zli_text)))
print('nontox title: {}'.format(len(nontox_zli_title)))
print('nontox text: {}'.format(len(nontox_zli_text)))

tox_zli_title_path = 'data/tweet/tox_zli_title.neg'
tox_zli_text_path = 'data/tweet/tox_zli_text.neg'
nontox_zli_title_path = 'data/tweet/nontox_zli_title.pos'
nontox_zli_text_path = 'data/tweet/nontox_zli_text.pos'

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

write_file(tox_zli_title_path, tox_zli_title, text_processor)
write_file(tox_zli_text_path, tox_zli_text, text_processor)
write_file(nontox_zli_title_path, nontox_zli_title, text_processor)
write_file(nontox_zli_text_path, nontox_zli_text, text_processor)

