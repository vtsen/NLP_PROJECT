import argparse
import sys
import os
import data_utils
import model
import train
import torch
import operator
import pdb

# model parameters
parser = argparse.ArgumentParser(description=
								'PyTorch project')
parser.add_argument('--lr', type=float, default=0.001, help=
								'initial learning rate [default: 0.001]')
parser.add_argument('--epochs', type=int, default=50, help=
								'number of epochs for train [default: 50]')
parser.add_argument('--batch_size', type=int, default=64, help=
								'batch size for training [default: 64]')
parser.add_argument('-save-dir', type=str, default='snapshot', help='where to save the snapshot')
# data 
parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch' )
# model
parser.add_argument('-embed-dim', type=int, default=200, help='number of embedding dimension [default: 200]')
parser.add_argument('-kernel-num', type=int, default=100, help='number of each kind of kernel')
parser.add_argument('-kernel-sizes', type=str, default='3,4,5', help='comma-separated kernel size to use for convolution')
parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')

parser.add_argument('-hidden-size', type=int, default=100, help='number of hidden layer size')

# device
parser.add_argument('-device', type=int, default=-1, help='device to use for iterate data, -1 mean cpu [default: -1]')
parser.add_argument('-no-cuda', action='store_true', default=True, help='disable the gpu' )
# option
parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')
parser.add_argument('-predict', type=str, default=None, help='predict the sentence given')
parser.add_argument('-test', action='store_true', default=False, help='train or test')
args = parser.parse_args()

def main():
	print("\nParameters:")
	for attr, value in args.__dict__.items():
		print("\t{}={}".format(attr.upper(), value))
	
	# load data
	train_data, embeddings = data_utils.load_dataset()
	
	# initalize necessary parameters
	args.embed_num = embeddings.shape[0]
	args.kernel_sizes = [int(k) for k in args.kernel_sizes.split(',')]
	
	# choose model
	args.model = 'lstm'
#	args.model = 'cnn'
	
	# load model
	if args.model == 'lstm':
		mod = model.LSTM(args, embeddings)
	else:
		mod = model.CNN(args, embeddings)
	
	# train model
	res = train.train_model(train_data, mod, args)

if __name__=="__main__":
	main()


