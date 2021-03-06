import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd
import pdb

class CNN(nn.Module):
	def __init__(self, args, embeddings):
		super(CNN,self).__init__()
		self.args = args
		
		V = args.embed_num
		D = args.embed_dim
		Ci = 1
		Co = args.kernel_num
		Ks = args.kernel_sizes

		# initialize embeddingl layer 
		self.embed = nn.Embedding(V, D)
		self.embed.weight.data = torch.from_numpy(embeddings)
		# don't want to re-train embeddings
		self.embed.weight.requires_grad=False

		# convolution step
		self.convs1 = nn.ModuleList([nn.Conv2d(Ci, Co, (K, D)) for K in Ks])

	def forward(self, x):
		x = self.embed(x) # (N,W,D)
		
		#y = self.embed(y)	   
 
		if self.args.static:
			x = Variable(x)
			#y = Variable(y)			

		x = x.unsqueeze(1) # (N,Ci,W,D)
		#y = y.unsqueeze(1) # (N,Ci,W,D)

		x = [F.relu(conv(x)).squeeze(3) for conv in self.convs1] #[(N,Co,W), ...]*len(Ks)
		#y = [F.relu(conv(y)).squeeze(3) for conv in self.convs1] #[(N,Co,W), ...]*len(Ks)
		
#		pdb.set_trace()


		x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x] #[(N,Co), ...]*len(Ks)
		#y = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in y] #[(N,Co), ...]*len(Ks)

		x = torch.cat(x, 1)
		#y = torch.cat(y, 1)
 
		return x #nn.CosineSimilarity(x,y)


class LSTM(nn.Module):
	def __init__(self, args, embeddings):
		super(LSTM, self).__init__()

		self.args = args
		
		V = args.embed_num
		D = args.embed_dim

		# initialize embedding layer 
		self.embed = nn.Embedding(V, D)
		self.embed.weight.data = torch.from_numpy(embeddings)
		
		self.embed.weight.requires_grad=False
		
		
		self.lstm = nn.LSTM(input_size=D,
						  hidden_size=args.hidden_size,
						  num_layers=1,
						  batch_first=True)
		

	def forward(self, x):
		
		
		x = self.embed(x) # (N,W,D) 
 
		if self.args.static:
			x = autograd.Variable(x)
			
		hidden = (autograd.Variable(torch.zeros(1, len(x), self.args.hidden_size)),
			autograd.Variable(torch.zeros(1, len(x), self.args.hidden_size)))
		
		out, hidden = self.lstm(x, hidden)
#		_, h_k = self.lstm(packed, (h0, c0))
		
		out = out.permute(0,2,1)		# swap axes
		
		return F.max_pool1d(out, out.size(2)).squeeze(2)
#		
#		x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x] #[(N,Co), ...]*len(Ks)
#
#		x = torch.cat(x, 1)
 
#		return out