import sys
import cmd
import readline
import shlex
import socket
import threading

lock = threading.Lock()

class CowsayClient(cmd.Cmd):
  @staticmethod
  def send_recv_server(msg, need=True):
    sock.send((msg.strip() + "\n").encode())
    if need:
      return sock.recv(1024).decode().strip().replace("'", "")

  def do_login(self, args):
    print(CowsayClient.send_recv_server("login " + args.strip()))

  def do_cows(self, args):
    print(CowsayClient.send_recv_server("cows"))

  def do_who(self, args):
    print(CowsayClient.send_recv_server("who"))

  def do_say(self, args):
    CowsayClient.send_recv_server("say " + args.strip(), need=False)

  def do_yield(self, args):
    CowsayClient.send_recv_server("yield " + args.strip(), need=False)

  def complete_login(self, text, line, *args):
    with lock:
      cow_list = shlex.split(CowsayClient.send_recv_server("cows")[13:].replace(",", ""))
      return [name for name in cow_list if name.startswith(text)]

  def complete_say(self, text, line, *args):
    with lock:
      if len(text.split()) <= 1:
        who_list = shlex.split(CowsayClient.send_recv_server("who")[12:].replace(",", ""))
        return [name for name in who_list if name.startswith(text)]

  def do_exit(self, args):
    return 1

def target():
  while True:
    if not lock.locked():
      ans = sock.recv(1024).decode().strip().replace("'", "")
      if ans:
        print(ans + "\n")
        print(f"\n(Cowsay){readline.get_line_buffer()}", end="", flush=True)

if __name__ == "__main__":
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((sys.argv[1], int(sys.argv[2])))
    global cmd_line
    cmd_line = CowsayClient()
    threading.Thread(target=target, args=()).start()
    cmd_line.cmdloop()