import socket 

def send_file(file_path): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5001))

    # Step 1: Send hello to server 
    client_socket.send("Hello from Client!".encode())

    # Step 1: Receive hello from server 
    server_hello = client_socket.recv(1024).decode() 
    print(f"Server says: {server_hello}")

    # Step 2: Send file name 
    filename = file_path.split('/')[-1]
    client_socket.send(filename.encode())

    # Step 2: Send file data 
    with open(file_path, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            client_socket.send(bytes_read)

    print("File sent successfully.")
    client_socket.close()

# Run the client 

send_file("pk.txt")


# Server

import socket

def receive_file():

    # Create TCP socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('127.0.0.1', 5001))

    server_socket.listen(1)

    print("Server listening on port 5001...")

    # Accept client connection

    conn, addr = server_socket.accept()

    print(f"Connection from {addr}")

    # Step 1: Receive hello from client

    client_hello = conn.recv(1024).decode()

    print(f"Client says: {client_hello}")

    # Step 1: Send hello to client

    conn.send("Hello from Server!".encode())

    # Step 2: Receive file name

    filename = conn.recv(1024).decode()

    print(f"Receiving file: {filename}")

    # Step 2: Receive file data and save it

    with open("received_" + filename, 'wb') as f:

        while True:

            data = conn.recv(1024)

            if not data:

                break

            f.write(data)

    print("File received successfully.")

    conn.close()

    server_socket.close()

# Run the server

receive_file()






'''

import socket

Imports the Python standard library socket module which provides low-level network I/O (TCP/UDP). Required to create sockets and connect to remote endpoints.


def send_file(file_path):

Defines a function send_file which accepts file_path (string): the path to the file on the client machine that will be sent.


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Creates a new socket object named client_socket.

AF_INET — address family IPv4.

SOCK_STREAM — type TCP (stream-oriented, reliable).

This socket will be used to connect to the server and send data.


client_socket.connect(('127.0.0.1', 5001))

Connects the socket to the server at IP 127.0.0.1 (localhost) on port 5001.

This is a blocking call: it waits until the connection is established or fails.


# Step 1: Send hello to server 
    client_socket.send("Hello from Client!".encode())

Sends a small greeting message to the server as a simple application-level handshake.

.encode() converts the Python str to bytes using UTF-8.

send() sends bytes. Note: send() may send fewer bytes than requested; sendall() is safer when you must ensure all bytes are written.


# Step 1: Receive hello from server 
    server_hello = client_socket.recv(1024).decode() 
    print(f"Server says: {server_hello}")

recv(1024) reads up to 1024 bytes from the socket (blocking until some data arrives).

.decode() converts bytes back to a str assuming UTF-8.

The server’s hello message is printed.

Important: The code assumes the entire server hello fits in 1024 bytes (it does) and that recv returns the full message in one call (likely for small messages).


# Step 2: Send file name 
    filename = file_path.split('/')[-1]
    client_socket.send(filename.encode())

file_path.split('/')[-1] takes the last segment after / to extract the filename (works for Unix-style paths). If running on Windows with backslashes, this may not work—os.path.basename(file_path) is safer.

Sends the filename as a UTF-8 encoded bytes string to the server. The server needs to know what to call the received file.


# Step 2: Send file data 
    with open(file_path, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            client_socket.send(bytes_read)

Opens the file in binary read mode 'rb' (important for non-text files).

Enters a loop reading the file in chunks of 1024 bytes.

f.read(1024) returns up to 1024 bytes; when EOF is reached it returns an empty b'' which is falsy, and the loop breaks.

client_socket.send(bytes_read) sends the chunk to the server.

Again, send() might not send all bytes in one call for very large chunks; sendall() is safer to ensure the whole chunk is transmitted.


This streaming approach avoids loading the entire file into memory.


print("File sent successfully.")
    client_socket.close()

Prints a success message and closes the socket connection — this sends a FIN to the server, indicating the client finished sending. The server’s recv() will eventually return empty bytes when the client closes, which signals EOF on the socket.


# Run the client 
send_file("pk.txt")

Calls send_file with "pk.txt" — this will attempt to connect to 127.0.0.1:5001 and send the file pk.txt from the client’s current working directory.



---

Server — line-by-line

import socket

Same socket import as client.


def receive_file():

Defines receive_file() function which implements the server logic to accept one client and receive a file.


# Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Creates a TCP socket for listening.


server_socket.bind(('127.0.0.1', 5001))

Binds the server socket to IP 127.0.0.1 (localhost) and port 5001.

Only local processes can reach this server (not remote hosts). To accept connections from other machines, bind to '0.0.0.0' or a specific network IP.


server_socket.listen(1)

Puts the socket into listening state and sets the backlog (number of unaccepted connections before new ones are refused) to 1.

The server will accept one connection at a time.


print("Server listening on port 5001...")

Prints a status message.


# Accept client connection
    conn, addr = server_socket.accept()

accept() blocks until a client connects. It returns a new socket object conn (used for communicating with the connected client) and addr which is the client’s address tuple (ip, port).


print(f"Connection from {addr}")

Logs the client address (IP and port).


# Step 1: Receive hello from client
    client_hello = conn.recv(1024).decode()
    print(f"Client says: {client_hello}")

Reads up to 1024 bytes from the connected socket conn, decodes it, and prints the greeting. This matches the client's initial send() of "Hello from Client!".


# Step 1: Send hello to client
    conn.send("Hello from Server!".encode())

Sends a greeting back to the client. Again, small message, so send() is fine.


# Step 2: Receive file name
    filename = conn.recv(1024).decode()
    print(f"Receiving file: {filename}")

Receives the filename sent by the client (expects it to arrive in a single recv call) and decodes it from UTF-8.

Prints the filename. The server uses this to name the received file.


# Step 2: Receive file data and save it
    with open("received_" + filename, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

Opens a file named "received_" + filename in binary write mode.

Then enters a loop receiving up to 1024 bytes at a time from the socket.

If recv() returns an empty bytes object (b''), that indicates the client closed the connection (EOF), and the loop breaks.

Each received chunk is written to the file. This reconstructs the file on the server side.


print("File received successfully.")
    conn.close()
    server_socket.close()

Prints success message.

Closes the client connection socket conn.

Closes the listening server socket server_socket.

After closing, the server stops running — this implementation handles only one client and then exits.


# Run the server
receive_file()

Calls the receive_file() function to start the server and wait for a client.



What is a socket?

A socket is an endpoint of a two-way communication link between two programs running over a network.

It acts like a door between an application and the network.

A socket allows sending and receiving data using protocols like TCP or UDP.

Each socket is identified by an IP address and a port number.


👉 In Python, socket.socket() is used to create a socket object.


---

2️⃣ What is TCP?

TCP (Transmission Control Protocol) is a connection-oriented, reliable, and byte-stream protocol used for data transmission.

Connection-oriented: A connection must be established before data transfer (like a phone call).

Reliable: Ensures all data is delivered in the correct order without loss or duplication.

Stream-based: Data is sent as a continuous stream of bytes, not fixed-size packets.


👉 Used in applications like HTTP, FTP, Email, etc.


---

3️⃣ What is the difference between TCP and UDP?

Feature	TCP (Transmission Control Protocol)	UDP (User Datagram Protocol)

Type	Connection-oriented	Connectionless
Reliability	Reliable (acknowledges and retransmits lost packets)	Unreliable (no guarantee of delivery)
Speed	Slower due to error checking and acknowledgment	Faster because of less overhead
Order	Maintains data order	May deliver out of order
Use cases	Web (HTTP), Email, File Transfer	Video Streaming, VoIP, Online Games


👉 In your program, TCP is used to ensure the file is transferred correctly.


---

4️⃣ Which layer uses TCP?

TCP operates at the Transport Layer of the OSI Model (Layer 4).

It provides end-to-end communication, reliability, and flow control between devices.



---

5️⃣ What are the functions of socket(), bind(), listen(), and accept()?

Function	Used By	Description

socket()	Both client & server	Creates a new socket object for communication.
bind()	Server	Assigns (binds) the socket to a specific IP address and port number.
listen()	Server	Puts the server socket in listening mode to wait for incoming connections.
accept()	Server	Accepts an incoming client connection and returns a new socket for communication.


👉 Example in your server:

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5001))
server_socket.listen(1)
conn, addr = server_socket.accept()


---

6️⃣ What is a client and a server in a socket program?

Server:
The machine or program that waits for incoming connections, accepts them, and provides services (like file transfer or data).
Example: receive_file() function in your code.

Client:
The machine or program that initiates the connection to the server and sends requests or data.
Example: send_file() function in your code.



---

7️⃣ How does TCP ensure reliable data transfer?

TCP ensures reliability using several mechanisms:

1. Three-way handshake → Establishes connection before data transfer.


2. Acknowledgment (ACK) → Confirms receipt of packets.


3. Sequence numbers → Keeps data in correct order.


4. Retransmission → Resends lost or corrupted packets.


5. Error detection (Checksum) → Detects errors in transmission.


6. Flow control → Manages sender speed so receiver isn’t overwhelmed.



So TCP guarantees that all data is delivered accurately and in sequence.


---

8️⃣ What is a port number?

A port number is a logical identifier assigned to each application or process that uses a network connection.

It helps differentiate multiple network services on the same device.

Example:

HTTP → Port 80

HTTPS → Port 443

Your program uses Port 5001



A socket is uniquely identified by:
IP address + Port number


---

9️⃣ What is the output of the “Say Hello” program?

In your file transfer code, before the actual file is sent, both client and server exchange greetings (“Hello” messages).
So, the output is:

On Server side:

Server listening on port 5001...
Connection from ('127.0.0.1', <some_port>)
Client says: Hello from Client!
Receiving file: pk.txt
File received successfully.

On Client side:

Server says: Hello from Server!
File sent successfully.


---

🔟 How is file transfer verified?

The transfer is verified by:

1. Checking the output message → “File sent successfully.” on client and “File received successfully.” on server.


2. Checking that a new file received_pk.txt is created on the server.


3. Comparing contents of both files:

You can open both and verify they are identical.

Or use Python to verify:




open('pk.txt','rb').read() == open('received_pk.txt','rb').read()

If True, the file was successfully transferred without corruption.
'''