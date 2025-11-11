import socket
import os

def start_client():
    server_ip = input("Enter server IP address(127.0.0.1): ")
    filename = input("Enter the file name to send: ")

    # Step 1: Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, 5001)

    # Step 2: Send file name first
    client_socket.sendto(filename.encode(), server_address)

    # Step 3: Read file in binary mode and send in chunks
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendto(bytes_read, server_address)
        # Send end of file marker
        client_socket.sendto(b'EOF', server_address)
        print("File sent successfully.")
    else:
        print("File not found!")

    # Step 4: Receive confirmation from server
    msg, _ = client_socket.recvfrom(1024)
    print("Server response:", msg.decode())

    client_socket.close()


if __name__ == "__main__":
    start_client()


#Server

import socket



def start_server():

    # Step 1: Create UDP socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    # Step 2: Bind server to localhost and port 5001

    server_socket.bind(('0.0.0.0', 5001))

    print("UDP Server is up and listening on port 5001...")



    # Step 3: Receive file name from client

    filename, client_addr = server_socket.recvfrom(1024)

    filename = filename.decode()

    print(f"Receiving file: {filename} from {client_addr}")



    # Step 4: Open file to write received data

    with open("received_" + filename, 'wb') as f:

        while True:

            data, addr = server_socket.recvfrom(4096)

            if data == b'EOF':  # End Of File marker

                break

            f.write(data)



    print(f"File '{filename}' received successfully and saved as 'received_{filename}'")



    # Step 5: Send confirmation to client

    server_socket.sendto(b"File received successfully.", client_addr)



    # Close the socket

    server_socket.close()





if __name__ == "__main__":

    start_server()
    
    
    
    
    
    
'''

import socket
import os

import socket — loads Python’s networking module that provides socket objects and constants for network I/O.

import os — loads the OS utilities module; here it’s used to check whether a file exists.


def start_client():

Defines a function named start_client. All client logic lives inside this function.


server_ip = input("Enter server IP address(127.0.0.1): ")
    filename = input("Enter the file name to send: ")

input(...) prompts the user and reads a string from the console.

server_ip will hold the destination IP address (e.g., 127.0.0.1 for local loopback).

filename is the path or name of the file the user wants to send.



# Step 1: Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, 5001)

socket.socket(socket.AF_INET, socket.SOCK_DGRAM) creates a new socket object:

AF_INET — IPv4 address family.

SOCK_DGRAM — datagram socket type → UDP (connectionless, unreliable).


server_address is a tuple (ip, port) describing where to send packets. Port 5001 is chosen arbitrarily in this program.


# Step 2: Send file name first
    client_socket.sendto(filename.encode(), server_address)

filename.encode() converts the filename string to bytes (UTF-8 by default).

sendto(data, address) sends a UDP datagram containing the bytes to server_address.

The program sends the file name first so the server knows what filename to create.


# Step 3: Read file in binary mode and send in chunks
    if os.path.exists(filename):

os.path.exists(filename) checks whether the given file path exists on the client machine.

If the file does not exist, the program goes to the else branch and prints "File not found!".


with open(filename, 'rb') as f:

open(..., 'rb') opens the file for reading in binary mode. Binary mode is necessary to send non-text files correctly (images, executables, etc.).

The with context manager automatically closes the file when the block ends.


while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendto(bytes_read, server_address)

This loop reads the file in chunks of up to 4096 bytes (4 KB):

f.read(4096) returns a bytes object containing up to 4096 bytes, or b'' (empty bytes) when EOF is reached.

if not bytes_read: break — if bytes_read is empty, we've reached end-of-file and exit the loop.

client_socket.sendto(bytes_read, server_address) — sends the chunk to the server as a UDP datagram.


Chunking is used to avoid reading the whole file into memory at once and to send the file in manageable pieces.


# Send end of file marker
        client_socket.sendto(b'EOF', server_address)
        print("File sent successfully.")

After finishing sending file chunks, the client sends a special marker b'EOF' (bytes) to tell the server that no more file data will follow.

Important: using a plain marker like 'EOF' is simple but fragile — if the file itself contains the same bytes sequence as the marker, the server may misinterpret data. For binary-safe protocols you typically use length-prefix framing, sequence numbers, or separate control messages.


print("File sent successfully.") — not a guarantee the server actually saved the file (because UDP is unreliable), but indicates the client finished sending.


else:
        print("File not found!")

If the file path does not exist, inform the user.


# Step 4: Receive confirmation from server
    msg, _ = client_socket.recvfrom(1024)
    print("Server response:", msg.decode())

recvfrom(1024) blocks and waits for a UDP message up to 1024 bytes long. It returns (data, address).

msg receives the bytes from the server.

_ is the server address (ignored here).


msg.decode() decodes the bytes to a string and prints the server’s confirmation message.

Note: If the server’s response never arrives (lost packet, server down), recvfrom will block indefinitely. A production program would typically set a timeout on the socket (client_socket.settimeout(...)) and handle missing responses.


client_socket.close()

Closes the UDP socket to free the local port and resources.


if _name_ == "_main_":
    start_client()

Standard Python idiom:

If this file is executed as the main program, call start_client().

If the file is imported as a module, this block does not run.




---

Server: start_server() file receiver

import socket

Loads the socket module (already imported in the client file; in a separate file it must be imported again).


def start_server():

Defines the function start_server which contains the server logic.


# Step 1: Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Creates a UDP socket (IPv4 + datagram).


# Step 2: Bind server to localhost and port 5001
    server_socket.bind(('0.0.0.0', 5001))
    print("UDP Server is up and listening on port 5001...")

bind(('0.0.0.0', 5001)) attaches the socket to all network interfaces (0.0.0.0) on port 5001.

This makes the server listen for UDP packets addressed to that port on any local IP.


The print shows the server is ready.


# Step 3: Receive file name from client
    filename, client_addr = server_socket.recvfrom(1024)
    filename = filename.decode()
    print(f"Receiving file: {filename} from {client_addr}")

recvfrom(1024) waits for a UDP datagram (up to 1024 bytes) and returns (data, address).

filename holds the raw bytes sent by the client (the filename).

client_addr is a tuple (client_ip, client_port) identifying who sent the packet.


filename.decode() converts the bytes into a Python string.

The server prints which filename it will create and the client address.


# Step 4: Open file to write received data
    with open("received_" + filename, 'wb') as f:

Opens a new file for writing in binary mode with the prefix "received_" added to avoid overwriting local files with same name.

The with context guarantees the file will be closed when the block ends.


while True:
            data, addr = server_socket.recvfrom(4096)
            if data == b'EOF':  # End Of File marker
                break
            f.write(data)

This loop receives file data chunks repeatedly:

recvfrom(4096) reads up to 4096 bytes per UDP datagram.

if data == b'EOF' checks if the datagram equals the end-of-file marker sent by the client. If so, break out of the loop.

f.write(data) writes the received bytes to the output file.


Important UDP caveats:

UDP is message-oriented: each sendto by the client corresponds to one recvfrom call on the server (unless packets are lost or reordered).

UDP is unreliable: packets (chunks) can be lost, duplicated, or received out of order. This simple server assumes none of that happens. For reliable transfer you’d need acknowledgements, checksums, sequence numbers, retransmission logic, or simply use TCP.

The server also assumes that the EOF marker will arrive intact and not be mistaken for real file data.



print(f"File '{filename}' received successfully and saved as 'received_{filename}'")

Logs that the file was saved.


# Step 5: Send confirmation to client
    server_socket.sendto(b"File received successfully.", client_addr)

Sends a one-off confirmation message back to the client_addr (the address that sent the filename earlier).

Since UDP is connectionless, the server explicitly specifies the destination address.


# Close the socket
    server_socket.close()

Closes the server socket and releases the port. After this line, the server stops receiving further packets.


if _name_ == "_main_":
    start_server()

If the file is executed as the main program, start_server() runs.

\
    
What is UDP?

UDP (User Datagram Protocol) is one of the core protocols of the Internet Protocol (IP) suite.
It provides a fast, lightweight way to send data between devices over a network without establishing a connection.

It sends data in small independent chunks called datagrams.

UDP is defined in the Transport Layer (Layer 4) of the OSI model.

It is connectionless and unreliable, but very fast.



---

⚙️ 2. How is UDP different from TCP?

Feature	UDP (User Datagram Protocol)	TCP (Transmission Control Protocol)

Type	Connectionless	Connection-oriented
Reliability	Unreliable (no acknowledgment)	Reliable (ensures delivery)
Error checking	Has checksum but no retransmission	Has checksum, ACKs, retransmissions
Ordering	No guarantee of order	Ensures correct order of data
Speed	Very fast (less overhead)	Slower due to handshaking and checks
Header size	8 bytes	20 bytes (minimum)
Use cases	Live video, voice calls, games	File transfer, web pages, emails


👉 Summary:

TCP ensures accuracy and reliability.

UDP ensures speed and low latency.



---

🔗 3. What is meant by "connectionless service"?

“Connectionless” means no dedicated connection (handshake) is established between sender and receiver before data transmission.

Each packet (datagram) is sent independently, and may take different routes to reach the destination.

The sender doesn’t know if the receiver got the message.


➡️ Example: Sending letters through a postbox — you drop them, but don’t know if they were received unless someone tells you later.


---

⚠️ 4. Is UDP reliable? Why or why not?

❌ No, UDP is not reliable.

Because:

It does not guarantee delivery (packets can be lost).

It does not guarantee order (packets can arrive out of sequence).

It does not check whether the receiver got the data.

It has no retransmission of lost packets.


UDP just sends packets — once sent, it doesn’t care what happens next.


---

🌍 5. Real-life examples of UDP use

UDP is ideal for applications where speed matters more than perfect accuracy.
Some common examples:

Application	Why UDP is used

🎮 Online gaming	Small updates need to be sent very quickly
🎥 Video streaming (YouTube Live, Zoom, Skype)	Real-time delivery more important than perfection
🎧 Voice calls (VoIP)	Delays are worse than minor data loss
📺 IPTV (Internet TV)	Needs low latency
🧭 DNS (Domain Name System)	Simple request-response, small packets



---

💻 6. What functions are used for UDP communication?

In Python (using the socket module), these functions are used:

Function	Purpose

socket.socket(AF_INET, SOCK_DGRAM)	Creates a UDP socket
bind(address)	Binds the socket to IP and port (used by server)
sendto(data, address)	Sends UDP data to given address
recvfrom(buffer_size)	Receives UDP data and sender’s address
close()	Closes the socket



---

📤 7. How do you send and receive files using UDP?

Steps for UDP file transfer:

Client (Sender):

1. Create a UDP socket


2. Send the file name to the server


3. Open the file in binary mode ('rb')


4. Read and send the file in chunks (sendto)


5. Send an EOF marker (like 'EOF') to indicate end of file


6. Wait for confirmation message from the server



Server (Receiver):

1. Create and bind a UDP socket


2. Receive the file name


3. Open a new file to write ('wb')


4. Receive data chunks (recvfrom) until 'EOF' is received


5. Save the received data to a file


6. Send back a confirmation message to the client




---

📂 8. What types of files can be transferred?

Because the file is read and written in binary mode ('rb' and 'wb'),
you can send any type of file, including:

✅ Text files (.txt, .csv)

✅ Images (.jpg, .png)

✅ Audio/video files (.mp3, .mp4)

✅ Documents (.pdf, .docx)

✅ Executable files (.exe)


Essentially any file — but remember: UDP is unreliable, so files can become corrupted if packets are lost.


---

🚫 9. What happens if a packet is lost in UDP?

If a packet (datagram) is lost:

The sender is not notified.

The receiver never receives that part of the file.

The file may be incomplete or corrupted.

UDP does not retransmit lost packets automatically.


To fix this, you would need to implement your own:

Acknowledgment system

Timeout and retransmission

Checksum verification



---

🎧 10. Why is UDP preferred for audio/video transfer?

Because in real-time communication, speed and low delay are more important than perfect accuracy.

If one frame or voice packet is lost, it’s better to skip it than to delay the whole stream.

UDP has no retransmission delay.

It allows continuous, smooth playback — minor data loss is hardly noticeable in sound/video.


✅ Example: In a video call, you prefer the video to continue smoothly even if a few frames are lost — not to pause and wait for retransmission.

'''
