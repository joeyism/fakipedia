import torch
import numpy as np

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from tqdm import tqdm
from lib import objects
from lib import wikitext_to_html
from lib import constants as c

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

tokenizer = GPT2Tokenizer.from_pretrained(c.GPT2_NAME)
model = GPT2LMHeadModel.from_pretrained(c.GPT2_NAME)
model = model.to(device)
EOD_ID = tokenizer.encode("<|endoftext|>")[0]
EQUAL_ID = tokenizer.encode(" = ")[0]
NEW_LINE_ID = 198
HEADER_ID = 796

test_article = """ = Toronto Raptors = 

 Toronto Raptors are the best team in the world

 = = History = = 
 Founded in 1996, they had to endure Vince Carter before winning the 2018-2019 NBA Championship
"""

def generate_text(input_str, text_len=c.MAX_TEXT_LENGTH, end_of_text_id=EOD_ID, top_random=5, test=False, memory=c.DEFAULT_MODEL_MEMORY):
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
    return output_text

def choose_from_top(probs, n=5):
  ind = np.argpartition(probs, -n)[-n:]
  top_prob = probs[ind]
  top_prob = top_prob / np.sum(top_prob) # Normalize
  if EQUAL_ID in ind and np.where(ind == EQUAL_ID)[0][0] == np.argmax(top_prob): # return =
    return EQUAL_ID
  choice = np.random.choice(n, 1, p = top_prob)
  token_id = ind[choice][0]
  return int(token_id)

def clean_starting_text(title):
  title = " ".join([word.capitalize() for word in title.replace("_", " ").split()])
  return title

def create_starting_text(title):
  return f""" = {title} =

"""

def generate_page(title, text_len, memory, cutoff=True):
  page = objects.GeneratedPage.get_page_by_query(title, text_len, memory)
  if page is None:
    cleaned_title = clean_starting_text(title)
    starting_text = create_starting_text(cleaned_title)
    source = generate_text(starting_text, test=c.ENV.lower()=='test', text_len=text_len, memory=memory)
    source = wikitext_to_html.run(source)
    if cutoff:
      source = ". ".join(source.split(". ")[:-1] + [""])
    page = objects.GeneratedPage(title, cleaned_title, source, text_len, memory)
    page.save()
  return page
