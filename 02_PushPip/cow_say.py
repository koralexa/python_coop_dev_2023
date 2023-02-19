from argparse import ArgumentParser
import cowsay

parser = ArgumentParser(prog = 'Cowsay', description='Configurable speaking/thinking cow (and a bit more).')

parser.add_argument('-e', dest='eyes', action='store', required=False, default='oo',
                    help='The appearance of the cow\'s eyes. The first two characters of the argument string eye_string will be used. The default eyes are \'oo\'')
parser.add_argument('-f', dest='cowfile', action='store', required=False, default='',
                    help='Specifies a particular cow picture file ("cowfile") to use')
parser.add_argument('-n', dest='wrap_text', action='store_false', required=False,
                    help='If specified, the given message will not be word-wrapped')
parser.add_argument('-l', dest='l', action='store_true', required=False,
                    help='List all cowfiles on the current COWPATH')
parser.add_argument('-T', dest='tongue', action='store', required=False, default='',
                    help='The appearance of the cow\'s tongue. Must be two characters and does not appear by default. However, it does appear in the \'dead\' and \'stoned\' modes')
parser.add_argument('-W', dest='width', action='store', required=False, default=40, type=int,
                    help='Specifies roughly where the message should be wrapped. The default is equivalent to -W 40 i.e. wrap words at or before the 40th column')
parser.add_argument('-b', dest='preset', action='append_const', const='b', default=[''], required=False,
                    help='Initiates Borg mode')
parser.add_argument('-d', dest='preset', action='append_const', const='d', default=[''], required=False,
                    help='Causes the cow to appear dead')
parser.add_argument('-g', dest='preset', action='append_const', const='g', default=[''], required=False,
                    help='Invokes greedy mode')
parser.add_argument('-p', dest='preset', action='append_const', const='p', default=[''], required=False,
                    help='Causes a state of paranoia to come over the cow')
parser.add_argument('-s', dest='preset', action='append_const', const='s', default=[''], required=False,
                    help='Makes the cow appear thoroughly stoned')
parser.add_argument('-t', dest='preset', action='append_const', const='t', default=[''], required=False,
                    help='Yields a tired cow')
parser.add_argument('-w', dest='preset', action='append_const', const='w', default=[''], required=False,
                    help='Somewhat the opposite of -t, and initiates wired mode')
parser.add_argument('-y', dest='preset', action='append_const', const='y', default=[''], required=False,
                    help='Brings on the cow\'s youthful appearance')
parser.add_argument('message', action='store', default=' ', nargs='?',
                    help='A string to wrap in the text bubble')               

args = parser.parse_args()

cow = 'default'
if args.cowfile.find("/") == -1 and args.cowfile in cowsay.list_cows():
  cow = args.cowfile
cowfile = None
if args.cowfile.find("/") != -1:
  cowfile = args.cowfile

if args.l and args.message == " ":
  print(cowsay.list_cows())
else:
  print(cowsay.cowsay(args.message,
                      eyes=args.eyes[0:2],
                      cowfile=cowfile,
                      wrap_text=args.wrap_text,
                      tongue=args.tongue[0:2],
                      width=args.width,
                      preset=max(args.preset),
                      cow=cow))