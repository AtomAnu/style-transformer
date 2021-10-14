from data import jsonl_reader, write_file

"""
Data:
    - hateful_founta_filt_nontox/train.jsonl -> train.pos dev.pos
    - hateful_founta_filt_tox/train.jsonl -> train.neg dev.neg
    - val.jsonl -> test.pos test.neg

"""

nontox_train_path = 'data/tweet/hateful_founta_filt_nontox/train.jsonl'
tox_train_path = 'data/tweet/hateful_founta_filt_tox/train.jsonl'
val_path = 'data/tweet/val.jsonl'

nontox_train_text_list = jsonl_reader(nontox_train_path)
tox_train_text_list = jsonl_reader(tox_train_path)
val_text_list = jsonl_reader(val_path)

train_pos_path = 'data/tweet/train.pos'
train_neg_path = 'data/tweet/train.neg'
dev_pos_path = 'data/tweet/dev.pos'
dev_neg_path = 'data/tweet/dev.neg'
test_pos_path = 'data/tweet/test.pos'
test_neg_path = 'data/tweet/test.neg'

write_file(train_pos_path, nontox_train_text_list)
write_file(dev_pos_path, nontox_train_text_list)
write_file(train_neg_path, tox_train_text_list)
write_file(dev_neg_path, tox_train_text_list)
write_file(test_pos_path, val_text_list)
write_file(test_neg_path, val_text_list)
