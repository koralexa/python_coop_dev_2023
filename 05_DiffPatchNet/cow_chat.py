import asyncio
from cowsay import cowsay, list_cows

clients = {}
cows_list = list_cows()

async def chat(reader, writer):
  registered = False
  me = ""
  queue = asyncio.Queue()
  send = asyncio.create_task(reader.readline())
  receive = asyncio.create_task(queue.get())
  while not reader.at_eof():
    done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
    for q in done:
      if q is send:
        send = asyncio.create_task(reader.readline())
        message = q.result().decode().split()
        if len(message < 1):
          continue
        elif message[0] == "login":
          if registered:
            writer.write(f"You are already registered as {me}\n".encode())
          elif (message[1] in cows_list) and not registered:
            me = message[1]
            clients[me] = asyncio.Queue()
            cows_list.remove(message[1])
            registered = True
            writer.write("You are successfully registered\n".encode())
            await writer.drain()
            receive.cancel()
            receive = asyncio.create_task(clients[me].get())
          else:
            writer.write("Name is invalid or already taken\n".encode())
            await writer.drain()
        elif message[0] == "quit":
          send.cancel()
          receive.cancel()
          if registered:
            del clients[me]
            cows_list.append(me)
          writer.close()
          await writer.wait_closed()
          return
        elif (message[0] == 'cows'):
          writer.write(f"Available usernames (cows): {', '.join(cows_list)}\n".encode())
          await writer.drain()
        elif (message[0] == 'who'):
          writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
          await writer.drain()
        elif (message[0] == "say"):
          if not registered:
            writer.write("Please, register to be able to send messages\n".encode())
            await writer.drain()
            continue
          if (message[1] in clients.keys()):
            await clients[message[1]].put(f"Message from {me}:\n {cowsay.cowsay((' '.join(message[2:])).strip(), cow=me)}")
            writer.write("Message is sent\n".encode())
            await writer.drain()
          else:
            writer.write("User with this name is not registered\n".encode())
            await writer.drain()
        elif (message[0] == 'yield'):
          if not registered:
            writer.write("Please, register to be able to send messages\n".encode())
            await writer.drain()
            continue
          for dst in clients.values():
            if dst is not clients[me]:
              await dst.put(f"Message from {me}:\n {cowsay(' '.join(message[1:]).strip(), cow=me)}")
          writer.write("Message is sent \n".encode())
          await writer.drain()
        else:
          writer.write("Wrong command \n".encode())
          await writer.drain()
      elif q is receive:
        receive = asyncio.create_task(clients[me].get())
        writer.write(f"{q.result()}\n".encode())
        await writer.drain()
  send.cancel()
  receive.cancel()
  print(me, "DONE")
  del clients[me]
  writer.close()
  await writer.wait_closed()

async def main():
  server = await asyncio.start_server(chat, '0.0.0.0', 1337)
  async with server:
    await server.serve_forever()

asyncio.run(main())