import torch


eos = 200
pad = 100

a = torch.tensor([[1,2,3,4,5,eos,pad,pad],
                 [1,2,3,4,5,6,7,eos],
                 [1,2,3,4,5,6,eos,pad],
                 [1,2,3,4,eos,pad,pad,pad]])

shorten_a = a[:,:7]

tmp = shorten_a.eq(eos).to(torch.int64)

# print(tmp.sum(1))

eos_pad_col = torch.tensor([eos]*a.size(0)) - (tmp.sum(1) * 100)

print(eos_pad_col.unsqueeze(1).shape)

print(shorten_a.shape)

shorten_a = torch.cat([shorten_a, eos_pad_col.unsqueeze(1)], dim=1)

print(shorten_a)
print(shorten_a.shape)

# print(a.size())