import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available interfaces in Codespaces
PORT = 55555

# Server Socket Initialization (IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists to keep track of connected clients and their nicknames
clients = []
nicknames = []

def broadcast(message, sender_client):
    """Send a message to all clients except the sender"""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                # If sending fails, the client might have disconnected
                remove_client(client)

def remove_client(client):
    """Safely handle client disconnection without crashing the server"""
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        
        nickname = nicknames[index]
        # Notify other clients in English
        broadcast(f"📢 {nickname} has left the chat.".encode('utf-8'), client)
        nicknames.remove(nickname)
        
        print(f"[-] Connection closed with {nickname}")

def handle_client(client):
    """Thread function to continuously listen for messages from a specific client"""
    while True:
        try:
            # Receive message (Buffer size 1024 bytes)
            message = client.recv(1024)
            if not message:
                break
            # Broadcast the received message to everyone else
            broadcast(message, client)
        except:
            break
    
    remove_client(client)

def receive_connections():
    """Main loop to accept incoming client connections"""
    print(f"[+] Server is running and listening on port {PORT}...")
    
    while True:
        try:
            # Accept a new connection
            client, address = server.accept()
            print(f"[+] New connection from {str(address)}")

            # Request nickname from the client upon joining
            client.send("NICKNAME_REQUEST".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            nicknames.append(nickname)
            clients.append(client)

            print(f"[+] Client nickname: {nickname}")
            broadcast(f"🎉 {nickname} joined the chat!".encode('utf-8'), client)
            client.send("✅ Successfully connected to the chat room!".encode('utf-8'))

            # Start a dedicated thread for this client
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except KeyboardInterrupt:
            print("\n[-] Shutting down the server...")
            break

if __name__ == "__main__":
    receive_connections()