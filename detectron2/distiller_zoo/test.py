from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
import pdb


def cosine_similarity_loss(output_net, target_net, eps=0.0000001):
    # Normalize each vector by its norm
    output_net_norm = torch.sqrt(torch.sum(output_net ** 2, dim=1, keepdim=True))
    output_net = output_net / (output_net_norm + eps)
    output_net[output_net != output_net] = 0

    target_net_norm = torch.sqrt(torch.sum(target_net ** 2, dim=1, keepdim=True))
    target_net = target_net / (target_net_norm + eps)
    target_net[target_net != target_net] = 0

    # Calculate the cosine similarity
    model_similarity = torch.mm(output_net, output_net.transpose(0, 1))
    target_similarity = torch.mm(target_net, target_net.transpose(0, 1))
    pdb.set_trace()

    # Scale cosine similarity to 0..1
    model_similarity = (model_similarity + 1.0) / 2.0
    target_similarity = (target_similarity + 1.0) / 2.0

    # Transform them into probabilities, Normalize each vector by its norm
    model_similarity = model_similarity / torch.sum(model_similarity, dim=1, keepdim=True)
    target_similarity = target_similarity / torch.sum(target_similarity, dim=1, keepdim=True)

    # Calculate the KL-divergence
    loss = torch.mean(target_similarity * torch.log((target_similarity + eps) / (model_similarity + eps)))

    return loss

student = torch.tensor([[0,1,2],[2,3,4],[2,3,5]], dtype=torch.float)
teacher = torch.tensor([[1,2,2],[3,4,5],[3,4,0]], dtype=torch.float)
student2 = torch.tensor([[[0,1],[0,3]]], dtype=torch.float)
teacher2 = torch.tensor([[[1,2],[4,3]]], dtype=torch.float)
a = torch.tensor([[0,1]], dtype=torch.float)
b = torch.tensor([[1,2]], dtype=torch.float)

cosine_similarity_loss(student,teacher)