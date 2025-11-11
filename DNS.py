
import socket

def dns_lookup():
    choice = input("Enter '1' for URL to IP address or '2' for IP address to URL: ")

    if choice == '1':
        # URL to IP Address
        url = input("Enter the URL (e.g., www.example.com): ")
        try:
            ip_address = socket.gethostbyname(url)
            print(f"The IP address for {url} is: {ip_address}")
        except socket.gaierror:
            print("Could not resolve the URL. Please check the URL and try again.")

    elif choice == '2':
        # IP Address to URL
        ip_address = input("Enter the IP address (e.g., 192.0.2.1): ")
        try:
            url = socket.gethostbyaddr(ip_address)
            print(f"The URL for {ip_address} is: {url[0]}")
        except socket.herror:
            print("Could not resolve the IP address. Please check the IP and try again.")

    else:
        print("Invalid choice. Please enter '1' or '2'.")


if __name__ == "__main__":
    dns_lookup()
























'''

mport socket

Imports Python’s built-in socket module.

socket provides low-level networking interfaces and some DNS helper functions used here (gethostbyname, gethostbyaddr).

After this line you can call socket.some_function().



---

def dns_lookup():

Defines a function named dns_lookup.

No parameters; it reads from input() inside.

The function body (all indented lines that follow) will run when dns_lookup() is called.



---

choice = input("Enter '1' for URL to IP address or '2' for IP address to URL: ")

Shows the prompt string to the user and waits for keyboard input.

input() returns a str. Example returns: "1" or "2" (including possible whitespace if the user types it).

The returned string is stored in the variable choice.

Note: input() is blocking (the program waits here until user types and presses Enter).



---

if choice == '1':

Compares choice to the string '1'.

If the user entered exactly '1' (no extra spaces), the following indented block executes (URL → IP path).



---

# URL to IP Address
        url = input("Enter the URL (e.g., www.example.com): ")

Comment for human readers.

Prompts the user to enter a URL/hostname like www.example.com or example.com.

The entered string is stored in variable url.

Important: This expects a hostname (domain). It will not accept a full URL with scheme/path (e.g., https://example.com/path) — socket.gethostbyname expects a plain host name.



---

try:
            ip_address = socket.gethostbyname(url)
            print(f"The IP address for {url} is: {ip_address}")

try: begins an exception handling block.

socket.gethostbyname(url):

Performs a DNS lookup for url.

Returns a single IPv4 address as a string, e.g. "93.184.216.34".

Limitation: returns only IPv4. It does not return IPv6 addresses. For IPv6 or multiple addresses you would use socket.getaddrinfo.

This call may perform network I/O and will block until the DNS response arrives or an error/time-out occurs.


The result is stored in ip_address.

print(...) prints a friendly message with the resolved IP.

If the hostname cannot be resolved, socket.gethostbyname raises socket.gaierror (address-related error).



---

except socket.gaierror:
            print("Could not resolve the URL. Please check the URL and try again.")

Catches socket.gaierror raised by gethostbyname if DNS resolution fails (unknown host, network error, etc.).

Prints an error message explaining resolution failed.

Note: This catches only gaierror. Other exceptions (e.g., keyboard interrupt) are not caught here.



---

elif choice == '2':

If choice was not '1' but exactly '2', this elif branch runs (IP → URL path).



---

# IP Address to URL
        ip_address = input("Enter the IP address (e.g., 192.0.2.1): ")

Comment for human readers.

Prompts user to enter an IP address as a string (e.g. "8.8.8.8").

The input string is stored in ip_address.

Note: The program does not validate format here — an invalid string will simply cause gethostbyaddr to raise an exception.



---

try:
            url = socket.gethostbyaddr(ip_address)
            print(f"The URL for {ip_address} is: {url[0]}")

socket.gethostbyaddr(ip_address):

Performs a reverse DNS lookup (PTR lookup) for the given IP.

Returns a tuple: (hostname, aliaslist, ipaddrlist).

hostname is the primary host name (string).

aliaslist is a list of alternative names (possibly empty).

ipaddrlist is a list of IP addresses for that host (usually contains the original IP).


Example return: ("dns.google", [], ["8.8.8.8"]).


The code stores the full tuple in url (variable named url but actually a tuple).

print(f"The URL for {ip_address} is: {url[0]}") prints only the primary hostname (url[0]).

If the reverse lookup fails, socket.gethostbyaddr raises socket.herror.



---

except socket.herror:
            print("Could not resolve the IP address. Please check the IP and try again.")

Catches socket.herror raised when reverse lookup fails (no PTR record, network problem, invalid IP string).

Prints a friendly failure message.



---

else:
        print("Invalid choice. Please enter '1' or '2'.")

If choice was neither '1' nor '2', reaches this else branch.

Prints an instruction telling the user to use '1' or '2'.



---

if _name_ == "_main_":
    dns_lookup()

if _name_ == "_main_": is a common Python idiom:

When the script is run directly (python script.py), Python sets _name_ to "_main_", so the condition is true.

When the file is imported as a module in another script, _name_ will be the module name, not "_main_", so this block will not run.


dns_lookup() calls the function defined earlier — starting the interactive prompt and DNS lookups.



What is DNS?

DNS (Domain Name System) is a system that translates human-readable domain names (like www.google.com) into machine-readable IP addresses (like 142.250.190.78).
It acts like the phonebook of the Internet, mapping names to numbers.


---

2. What is the purpose of DNS?

The main purpose of DNS is to make it easier for users to access websites without remembering long numerical IP addresses.
✅ Simplifies browsing: You type a name, not a number.
✅ Automates resolution: Converts the name to IP automatically.
✅ Manages network traffic: Helps locate services and hosts efficiently.


---

3. What is the difference between URL and IP address?

Aspect	URL (Uniform Resource Locator)	IP Address

Definition	Human-readable address used to access websites	Numerical label assigned to a device on the network
Example	https://www.example.com/page.html	93.184.216.34
Purpose	Identifies a web resource and its location	Identifies the specific host or server
Readability	Easy for humans	Easy for computers



---

4. What is Forward Lookup?

Forward DNS lookup is the process of converting a domain name → IP address.
🧠 Example:
www.google.com → 142.250.190.78

This is what happens when you type a website name into your browser.


---

5. What is Reverse Lookup?

Reverse DNS lookup converts an IP address → domain name.
🧠 Example:
142.250.190.78 → www.google.com

Used mainly for email verification, logging, and network troubleshooting.


---

6. Which function is used in programming for DNS resolution?

In Python or C (using socket programming), the common functions are:

Language	Function	Purpose

Python	socket.gethostbyname('hostname')	Forward lookup
Python	socket.gethostbyaddr('IP_address')	Reverse lookup
C	gethostbyname()	Forward lookup
C	gethostbyaddr()	Reverse lookup



---

7. What command is used to check DNS in Windows/Linux?

System	Command	Description

Windows	nslookup <domain>	Shows IP for a domain or reverse lookup
Windows	ipconfig /displaydns	Shows local DNS cache
Linux	dig <domain>	Detailed DNS query info
Linux	host <domain>	Simple DNS lookup
Linux	nslookup <domain>	Same as Windows, also works here



---

8. What is the structure of a DNS query?

A DNS query (request sent to the DNS server) has three main parts:

Part	Description

Header	Contains query type, ID, and flags
Question Section	Contains the domain name and record type requested
Answer/Authority/Additional Sections	Contain the actual resolved data (like IP), authority information, and extra details



---

9. What are the DNS record types?

Record Type	Meaning	Example

A	Maps domain name → IPv4 address	example.com → 93.184.216.34
AAAA	Maps domain name → IPv6 address	example.com → 2606:2800:220:1:248:1893:25c8:1946
MX	Mail Exchange record (email routing)	mail.example.com
CNAME	Canonical Name (alias for another domain)	www → example.com
NS	Nameserver record (points to DNS server for domain)	ns1.example.com
PTR	Pointer record (for reverse DNS lookup)	93.184.216.34 → example.com
TXT	Text record (used for verification, SPF, etc.)	v=spf1 include:_spf.google.com ~all



---

10. What happens if DNS server is not reachable?

If the DNS server is down or unreachable:

The system cannot resolve domain names to IP addresses.

You can’t access websites using names (but can still access using IPs).

Browser shows errors like:

“DNS server not responding”

“This site can’t be reached”
'''