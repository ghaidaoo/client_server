import socket
import threading
import sys

# Connection Settings
HOST = '127.0.0.1'  # Localhost inside Codespaces
PORT = 55555

# Request nickname from the user before connecting
nickname = input("Choose your nickname: ")

# Initialize socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"[-] Could not connect to the server: {e}")
    sys.exit()

def receive_messages():
    """Continuously listen for incoming messages from the server"""
    while True:
        try:
            # Receive and decode message
            message = client.recv(1024).decode('utf-8')
            
            # If the server requests the nickname, send it back immediately
            if message == 'NICKNAME_REQUEST':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # In case of an error or server shutdown
            print("[-] Connection to the server was lost!")
            client.close()
            break

def send_messages():
    """Read user input from terminal and send it to the server"""
    while True:
        try:
            text = input("")
            if text.strip() == "":
                continue
                
            # If the client wants to exit gracefully
            if text.lower() == 'exit':
                client.close()
                break
                
            # Format the final message (Nickname: Message)
            full_message = f"{nickname}: {text}"
            client.send(full_message.encode('utf-8'))
        except:
            break

# Start a background thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Run the sending function in the main thread
send_messages()