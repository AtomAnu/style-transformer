import time
import numpy as np
import torchtext
from torchtext import data
import json

from utils import tensor2text

class DatasetIterator(object):
    def __init__(self, pos_iter, neg_iter):
        self.pos_iter = pos_iter
        self.neg_iter = neg_iter

    def __iter__(self):
        for batch_pos, batch_neg in zip(iter(self.pos_iter), iter(self.neg_iter)):
            if batch_pos.text.size(0) == batch_neg.text.size(0):
                yield batch_pos.text, batch_neg.text

def load_dataset(config, train_pos='train.pos', train_neg='train.neg',
                 dev_pos='dev.pos', dev_neg='dev.neg',
                 test_pos='test.pos', test_neg='test.neg'):

    root = config.data_path
    TEXT = data.Field(batch_first=True, eos_token='<eos>')
    
    dataset_fn = lambda name: data.TabularDataset(
        path=root + name,
        format='tsv',
        fields=[('text', TEXT)]
    )

    train_pos_set, train_neg_set = map(dataset_fn, [train_pos, train_neg])
    dev_pos_set, dev_neg_set = map(dataset_fn, [dev_pos, dev_neg])
    test_pos_set, test_neg_set = map(dataset_fn, [test_pos, test_neg])

    TEXT.build_vocab(train_pos_set, train_neg_set, min_freq=config.min_freq)

    if config.load_pretrained_embed:
        start = time.time()
        
        vectors=torchtext.vocab.GloVe('6B', dim=config.embed_size, cache=config.pretrained_embed_path)
        TEXT.vocab.set_vectors(vectors.stoi, vectors.vectors, vectors.dim)
        print('vectors', TEXT.vocab.vectors.size())
        
        print('load embedding took {:.2f} s.'.format(time.time() - start))

    vocab = TEXT.vocab
        
    dataiter_fn = lambda dataset, train: data.BucketIterator(
        dataset=dataset,
        batch_size=config.batch_size,
        shuffle=train,
        repeat=train,
        sort_key=lambda x: len(x.text),
        sort_within_batch=False,
        device=config.device
    )

    train_pos_iter, train_neg_iter = map(lambda x: dataiter_fn(x, True), [train_pos_set, train_neg_set])
    dev_pos_iter, dev_neg_iter = map(lambda x: dataiter_fn(x, False), [dev_pos_set, dev_neg_set])
    test_pos_iter, test_neg_iter = map(lambda x: dataiter_fn(x, False), [test_pos_set, test_neg_set])

    train_iters = DatasetIterator(train_pos_iter, train_neg_iter)
    dev_iters = DatasetIterator(dev_pos_iter, dev_neg_iter)
    test_iters = DatasetIterator(test_pos_iter, test_neg_iter)
    
    return train_iters, dev_iters, test_iters, vocab

def jsonl_reader(filename, flag=True, key='text'):

    with open(filename, 'r') as f:
        records = f.readlines()

    if flag:
        samples = list()

        for record in records:
            jdata = json.loads(record)
            samples.append(str(jdata[key]))

        return samples

    else:
        for record in records:
            jdata = json.loads(record)
            if len(jdata[key]) == 0:
                print('Empty line')


def write_file(filename, text_list, text_processor=None):

    len_list = []
    counter = 0

    with open(filename, 'w') as f:
        for text in text_list:
            if text_processor is None:
                f.write(text + '\n')
            else:
                processed_text = " ".join(text_processor.pre_process_doc(text))
                processed_text = processed_text.strip()
                len_list.append(len(processed_text))
                if len(processed_text) == 0:
                    print('Empty line found in {} at line {}'.format(filename, text_list.index(text)))
                    f.write('.' + '\n   ')
                    counter += 1
                else:
                    f.write(processed_text + '\n    ')

if __name__ == '__main__':
    train_iter, _, _, vocab = load_dataset('../data/yelp/')
    print(len(vocab))
    for batch in train_iter:
        text = tensor2text(vocab, batch.text)
        print('\n'.join(text))
        print(batch.label)
        break
