import os
import torch
import numpy as np

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from tqdm import tqdm

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

GPT2_NAME = os.getenv('GPT2_NAME', 'gpt2-medium')
tokenizer = GPT2Tokenizer.from_pretrained(GPT2_NAME)
model = GPT2LMHeadModel.from_pretrained(GPT2_NAME)
model = model.to(device)
EOD_ID = tokenizer.encode("<|endoftext|>")
NEW_LINE_ID = 198
HEADER_ID = 796

test_article = """ = Toronto Raptors = 

 Toronto Raptors are the best team in the world

 = = History = = 
 Founded in 1996, they had to endure Vince Carter before winning the 2018-2019 NBA Championship
"""

def generate_text(input_str, text_len=250, end_of_text_id=EOD_ID, top_random=10, test=False, memory=1024):
  if test:
    return test_article
  cur_ids = torch.tensor(tokenizer.encode(input_str)).unsqueeze(0).long().to(device)
  model.eval()
  with torch.no_grad():
    for i in tqdm(range(text_len)):
      outputs = model(cur_ids[:, -1*memory:], labels=cur_ids[:, -1*memory:])
      loss, logits = outputs[:2]
      softmax_logits = torch.softmax(logits[0,-1], dim=0)
      next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=top_random)
      if next_token_id == end_of_text_id:
        break
      elif next_token_id == NEW_LINE_ID and cur_ids[0][-1] == HEADER_ID and cur_ids[0][-2] != HEADER_ID:
        break
      elif next_token_id == NEW_LINE_ID and cur_ids[0][-1] == NEW_LINE_ID:
        break
      cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim=1)
    output_list = list(cur_ids.squeeze().to('cpu').numpy())
    output_text = tokenizer.decode(output_list)
    return output_text, cur_ids

def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

def clean_starting_text(title):
  title = " ".join([word.capitalize() for word in title.replace("_", " ").split()])
  return title

def create_starting_text(title):
  return f""" = {title} =

"""
