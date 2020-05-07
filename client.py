import socket
import select
import errno
import sys

HEADER_LENGTH = 10

my_username = input("Username: ")
my_password = input("Password: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5050))
s.setblocking(False)

password = my_password.encode("utf-8")
password_header = f"{len(password):<{HEADER_LENGTH}}".encode("utf-8")
s.send(password_header + password)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
s.send(username_header + username)

while True:

    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        s.send(message_header + message)
    try:  
        while True:
            #Receive all messages
            username_header = s.recv(HEADER_LENGTH)

            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            
            username_length = int(username_header.decode("utf-8"))
            username = s.recv(username_length).decode("utf-8")

            message_header = s.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8"))
            message = s.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()