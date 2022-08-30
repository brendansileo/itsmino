import json
import pandas as pd
import sys
import requests

#https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html

levels = ['BC', 'LOW', 'MID', 'HIGH', 'MAX']

def train():
   data = pd.read_csv('playedh_cedhddb.csv', sep=';',
   header=None, names=['Power', 'Decklist'])
   print(data['Power'].value_counts(normalize=False))
   training_set = data

   #cleaning
   training_set['Decklist'] = training_set['Decklist'].str.lower()

   training_set['Decklist'] = training_set['Decklist'].str.split('~')

   card_list = []
   for deck in training_set['Decklist']:
      for card in deck:
         card_list.append(card)

   card_list = list(set(card_list))

   card_counts_per_deck = {unique_word: [0] * len(training_set['Decklist']) for unique_word in card_list}

   for index, deck in enumerate(training_set['Decklist']):
      for card in deck:
         card_counts_per_deck[card][index] += 1

   card_counts = pd.DataFrame(card_counts_per_deck)

   training_set_clean = pd.concat([training_set, card_counts], axis=1)

   decks = {}
   for level in levels:
      decks[level] = training_set_clean[training_set_clean['Power'] == level]

   # P(Spam) and P(Ham)
   p_levels = {}
   for level in levels:
      p_levels[level] = len(decks[level]) / len(training_set_clean)

   # N_Spam
   n_cards_per_level_deck = {}
   n_level = {}
   for level in levels:
      n_cards_per_level_deck[level] = decks[level]['Decklist'].apply(len)
      n_level[level] = n_cards_per_level_deck[level].sum()

   # N_Vocabulary
   n_cards = len(card_list)

   # Laplace smoothing
   alpha = 1

   # Initiate parameters
   parameters = {}
   for level in levels:
      parameters[level] = {unique_card:0 for unique_card in card_list}

   # Calculate parameters
   parameters_level = {}
   for level in levels:
      parameters_level[level] = {}
      for card in card_list:
         n_card_given_level = {}
         p_card_given_level = {}
         n_card_given_level[level] = decks[level][card].sum()
         p_card_given_level[level] = (n_card_given_level[level] + alpha) / (n_level[level] + alpha*n_cards)
         parameters_level[level][card] = p_card_given_level[level]

   data = {}
   data['levels'] = levels
   data['p_levels'] = p_levels
   data['parameters_level'] = parameters_level
   with open('trained.json', 'w') as f:
      f.write(json.dumps(data))

def rate(decklist):
   with open('/home/pi/itsmino/projects/power_level/trained.json', 'r') as f:
      data = json.loads(f.read())
   deck_list = list(decklist.keys())
   deck_string = '~'.join(deck_list)
   deck = deck_string.lower().split('~')
   p_level_given_deck = {}
   for level in data['levels']:
      p_level_given_deck[level] = data['p_levels'][level]
   for card in deck:
      for level in data['levels']:
         if card in data['parameters_level'][level]:
            p_level_given_deck[level] *= data['parameters_level'][level][card]
   return max(p_level_given_deck, key=p_level_given_deck.get)

if __name__ == '__main__':
   mode = sys.argv[1]
   if mode == 'train':
      train()
   elif mode == 'rate':
      links = sys.argv[2:]
      rate(links)