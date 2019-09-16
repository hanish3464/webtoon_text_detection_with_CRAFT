"""train.py"""

import torch
from torch import optim
from torch.utils.data import DataLoader
import os

from wtd import WTD
import config
import file
import dataset

import debug


import time
import preprocess
import postprocess
import numpy as np
import sys

def train_net(myNet, device, dataloader, optimizer, iteration):

    for i in range(config.epoch):
        print('epoch :{} entered'.format(i))
        for i_batch, sample in enumerate(dataloader):
            x = sample['image'].to(device, dtype=torch.float)
            print(x.shape)

            y, _ = myNet(x)

            score_text = y[0, :, :, 0].cpu().data.numpy() #what is y dimension
            score_affinity = y[0, :, :, 1].cpu().data.numpy()
            print(score_text.shape)
            np.set_printoptions(threshold=sys.maxsize)
            print(score_text)

            #loss function

            #optimizer.zero_grad()
            #loss.backward()
            #optimizer.step()


            if iteration % 5 is 0: #exist bug
                debug.printing(score_text)
                debug.printing(score_affinity)

            iteration += 1




def train():
    """there is under developing"""

    datasets = dataset.webtoon_text_detection_dataset(config.train_images_folder_path, config.train_ground_truth_folder)
    dataloader = DataLoader(datasets, batch_size = config.batch_size, shuffle = True, num_workers = config.num_of_gpu)
    myNet = WTD()
    print('model initialize')

    if config.cuda: #GPU
        device = torch.device("cuda:0")
        myNet = myNet.cuda()

    else: #CPU
        device = torch.device("cpu")

    #myNet.apply(weight_init)
    parameters = myNet.parameters()
    optimizer =optim.Adam(parameters, lr = config.learning_rate)

    if not os.path.isdir(config.train_prediction_folder):
        os.mkdir(config.train_prediction_folder)

    iteration = 0
    train_net(myNet, device, dataloader, optimizer, iteration)