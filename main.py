import os
import torch
import time
from data import load_dataset
from models import StyleTransformer, Discriminator
from train import train, auto_eval


class Config():
    # data_path = './data/yelp/'
    data_path = './data/tweet/'
    log_dir = 'runs/exp'
    save_path = './save'
    pretrained_embed_path = './embedding/'
    preload_F = './save/Oct21175706/ckpts/30600_F.pth'
    preload_D = './save/Oct21175706/ckpts/30600_D.pth'
    device = torch.device('cuda' if True and torch.cuda.is_available() else 'cpu')
    discriminator_method = 'Multi' # 'Multi' or 'Cond'
    load_pretrained_embed = False
    min_freq = 3
    # max_length = 16
    max_length = 80
    embed_size = 256
    d_model = 256
    h = 4
    num_styles = 2
    num_classes = num_styles + 1 if discriminator_method == 'Multi' else 2
    num_layers = 4
    batch_size = 64
    lr_F = 0.0001
    lr_D = 0.0001
    L2 = 0
    iter_D = 10
    iter_F = 5
    F_pretrain_iter = 500
    log_steps = 5
    eval_steps = 25
    learned_pos_embed = True
    dropout = 0
    drop_rate_config = [(1, 0)]
    temperature_config = [(1, 0)]

    slf_factor = 0.25
    cyc_factor = 0.5
    adv_factor = 1

    inp_shuffle_len = 0
    inp_unk_drop_fac = 0
    inp_rand_drop_fac = 0
    inp_drop_prob = 0


def main():
    config = Config()
    train_iters, dev_iters, test_iters, vocab = load_dataset(config)
    print('Vocab size:', len(vocab))
    model_F = StyleTransformer(config, vocab).to(config.device)
    model_D = Discriminator(config, vocab).to(config.device)

    if os.path.isfile(config.preload_F):
        temp = torch.load(config.preload_F)
        model_F.load_state_dict(temp)
    if os.path.isfile(config.preload_D):
        temp = torch.load(config.preload_D)
        model_D.load_state_dict(temp)

    print(config.discriminator_method)
    
    train(config, vocab, model_F, model_D, train_iters, dev_iters, test_iters)
    

if __name__ == '__main__':
    main()
