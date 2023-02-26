from random import choice
from argparse import ArgumentParser

parser = ArgumentParser(
	prog = "Bulls and cows",
	description = "03 task",
)

parser.add_argument("dictionary", action = "store_const", type=str,
	help = "URL or path to the dictionary")

parser.add_argument("length",  action = "store_const", default = "5", type = int,
	help = "Length of the words in dictionary")

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
    guess = ask("Введите слово: ", words)
    b, c = bullscows(guess, secret)
    inform("Быки: {}, Коровы: {}", b, c)
    attemps += 1
  print(attemps)

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