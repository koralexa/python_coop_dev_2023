import cowsay
import cmd
import shlex

def complete_cowsay_and_cowthink(text, line, begidx, endidx):
  args = shlex.split(line)
  args_num = len(args)
  eyes = ["OO", "XX", "QQ", "DD", "WW", "CC", "TT"]
  tongues = ["II", "VV", "UU", "JL"]
  text_in_args = text == args[-1]
  args_2 = args_num == 2
  args_3 = args_num == 3
  args_4 = args_num == 4
  args_5 = args_num == 5
  if (text_in_args and args_3 or not text_in_args and args_2):
    return [cow for cow in cowsay.list_cows() if cow.startswith(text)]
  elif (text_in_args and args_4 or not text_in_args and args_3):
    return [eye for eye in eyes if eye.startswith(text)]
  elif (text_in_args and args_5 or not text_in_args and args_4):
    return [tongue for tongue in tongues if tongue.startswith(text)]

def cowsay_and_cowthink(args):
  message, *options = shlex.split(args)
  cow = 'default'
  eyes = 'OO'
  tongue = '  '
  if options:
    if options[0]:
      cow = options[0]
    if len(options) > 1 and options[1]:
      eyes = options[1]
    if len(options) > 2 and options[2]:
      tongue = options[2]
  return [message, eyes, tongue, cow]

class CmdCowSay(cmd.Cmd):
  intro = "Welcome to cow command line"
  prompt = "mu> "

  def do_list_cows(self, arg):
    """
		list_cows [dir]
		Lists all cow file names in the given directory or default cow list
		"""
    cowpath = None
    if arg: 
      cowpath = shlex.split(arg)[0]
    print(*cowsay.list_cows(cowpath))

  def do_make_bubble(self, arg):
    """
		make_buble [wrap_text [width [brackets ]]]
		The text that appears above the cows
		"""
    message, *options = shlex.split(arg)
    wrap_text = True
    width = 40
    brackets = cowsay.THOUGHT_OPTIONS['cowsay']
    if options:
      if options[0]:
        wrap_text = bool(options[0] == 'True')
      if len(options) > 1 and options[1]:
        width = int(options[1])
      if len(options) > 2 and options[2]:
        brackets = options[2]
    print(cowsay.make_bubble(message, brackets=brackets, width=width, wrap_text=wrap_text))

  def complete_make_bubble(self, text, line, begidx, endidx):
    args = shlex.split(line)
    args_num = len(args)
    text_in_args = args[-1] == text
    args_2 = args_num == 2
    args_3 = args_num == 3
    if (args_2 and not text_in_args or args_3 and text_in_args):
      return [res for res in ['True', 'False'] if res.lower().startswith(text.lower())]

  def do_cowsay(self, arg):
    """
		cowsay message [cow [eyes [tongue]]]
		Display a message as cow phrase
		"""
    message, eyes, tongue, cow = cowsay_and_cowthink(arg)
    print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))

  def complete_cowsay(self, text, line, begidx, endidx):
    return complete_cowsay_and_cowthink(text, line, begidx, endidx)

  def do_cowthink(self, arg):
    """
		cowthink message [cow [eyes [tongue]]]
		Display a message as cow thought
		"""
    message, eyes, tongue, cow = cowsay_and_cowthink(arg)
    print(cowsay.cowthink(message, eyes=eyes, tongue=tongue, cow=cow))

  def complete_cowthink(self, text, line, begidx, endidx):
    return complete_cowsay_and_cowthink(text, line, begidx, endidx)

  def do_exit(self, arg):
    """
    Exit cow command line
    """
    return True

CmdCowSay().cmdloop()