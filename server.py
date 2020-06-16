from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
print(ADDR)
SERVER.bind(ADDR)

# print(AF_INET)
print(SERVER.getsockname())

def accept_connections():
    print("Now accepting connections.")
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from ChatApp! Please type your name and press ENTER.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, )).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Welcome %s! If you want to quit, please type {quit} to exit." % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the group chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the group chat." % name))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
