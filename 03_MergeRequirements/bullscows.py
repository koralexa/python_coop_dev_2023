from random import choice
from argparse import ArgumentParser
import os
from urllib.request import urlretrieve

parser = ArgumentParser(prog = 'Игра \"Быки и коровы\"')

parser.add_argument('dictionary', action = 'store', type=str,
	help = 'URL или путь к словарю')

parser.add_argument('length',  action = 'store', default = 5, type = int,
	help = 'Длина слов в словаре')

args = parser.parse_args()

def bullscows(guess: str, secret: str) -> (int, int):
  guess_set = set(guess)
  secret_set = set(secret)
  cows = len(guess_set.intersection(secret_set))
  bulls = 0
  l = min((len(guess), len(secret)))
  for i in range(l):
    if guess[i] == secret[i]:
      bulls += 1
  return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
  secret = choice(words)
  b = 0
  c = 0
  attemps = 0
  while c != len(set(secret)):
    guess = ask('Введите слово: ')
    b, c = bullscows(guess, secret)
    inform('Быки: {}, Коровы: {}', b, c)
    attemps += 1
  print('Игра окончена, вы угадали слово за ', attemps, ' попыток')

def inform(format_string: str, bulls: int, cows: int) -> None:
	print(format_string.format(bulls, cows))

def ask(prompt: str, valid: list[str] = None) -> str:
  print(prompt)
  guess = input()
  if valid == None:
    while len(guess) != args.length:
      print(prompt)
      guess = input()
  else:
    while not guess in valid:
      print(prompt)
      guess = input()
  return guess

if os.path.exists(args.dictionary):
  file = args.dictionary
else:
  file, _ = urlretrieve(args.dictionary)

with open(file, 'r') as f:
  words = []
  for word in f.readlines():
    word = word.strip()
    if len(word) == args.length:
      words.append(word)
  if len(words) == 0:
    print('В словаре нет слов заданной длины')
  else:
    gameplay(ask, inform, words)