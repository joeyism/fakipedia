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

def generate_text(input_str, text_len=250, end_of_text_id=EOD_ID, top_random=10):
  cur_ids = torch.tensor(tokenizer.encode(input_str)).unsqueeze(0).long().to(device)
  model.eval()
  with torch.no_grad():
    for i in tqdm(range(text_len)):
      try:
        outputs = model(cur_ids[:, -1024:], labels=cur_ids[:, -1024:])
      except:
        import ipdb; ipdb.set_trace()
      loss, logits = outputs[:2]
      softmax_logits = torch.softmax(logits[0,-1], dim=0)
      next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=top_random)
      if next_token_id == end_of_text_id:
          break
      cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim=1)
    output_list = list(cur_ids.squeeze().to('cpu').numpy())
    output_text = tokenizer.decode(output_list)
    return output_text

def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)
