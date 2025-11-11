import ipaddress
import math

def calculate_subnet_mask(ip_address, num_subnets):
    # Convert IP address to an IPv4Network object
    ip_network = ipaddress.IPv4Network(ip_address, strict=False)

    # Get the base subnet mask in CIDR notation
    base_mask = ip_network.prefixlen

    # Calculate the new subnet mask
    bits_to_borrow = math.ceil(math.log2(num_subnets))
    new_mask = base_mask + bits_to_borrow

    # Calculate subnet mask in dotted decimal format
    subnet_mask = ipaddress.IPv4Network(f'0.0.0.0/{new_mask}').netmask

    # Hosts per subnet
    num_hosts_per_subnet = 2 ** (32 - new_mask) - 2

    return new_mask, subnet_mask, num_hosts_per_subnet


def main():
    print("Subnetting Demonstration Program")

    # Input IP and subnets
    ip_address = input("Enter the IP address with CIDR (e.g., 192.168.1.0/24): ")
    num_subnets = int(input("Enter the number of subnets required: "))

    # Process subnet mask
    new_mask, subnet_mask, num_hosts_per_subnet = calculate_subnet_mask(ip_address, num_subnets)

    # Output
    print("\nCalculated Subnet Mask Information:")
    print(f"Original IP Address and CIDR: {ip_address}")
    print(f"New Subnet Mask (CIDR Notation): /{new_mask}")
    print(f"New Subnet Mask (Dotted Decimal Notation): {subnet_mask}")
    print(f"Number of Hosts per Subnet: {num_hosts_per_subnet}")


if __name__ == "__main__":
    main()







'''

import ipaddress
import math

Imports two Python modules:
ipaddress — helps work with IPv4/IPv6 addresses and networks.
math — gives math functions (we use ceil and log2).


def calculate_subnet_mask(ip_address, num_subnets):
Defines a function named calculate_subnet_mask that takes:
ip_address — a string like '192.168.1.0/24'.
num_subnets — an integer: how many subnets you need.

ip_network = ipaddress.IPv4Network(ip_address, strict=False)
Converts the input string into an IPv4Network object.
strict=False means it will accept addresses where host bits might be set 
(e.g., 192.168.1.5/24) and treat it as the network 192.168.1.0/24.

base_mask = ip_network.prefixlen
prefixlen extracts the original CIDR mask (the /24 part becomes 24) and stores 
it in base_mask.

bits_to_borrow = math.ceil(math.log2(num_subnets))
Figures out how many bits of the host portion you must "borrow" to create num_subnets.
math.log2(num_subnets) gives the base-2 logarithm; ceil(...) rounds up because you need
 a whole number of bits.
Example: if num_subnets = 3, log2(3) ≈ 1.585 → ceil → 2 bits needed (because 1 bit only 
gives 2 subnets; 2 bits give 4).



new_mask = base_mask + bits_to_borrow

The new subnet mask (in CIDR) is the original mask plus the borrowed bits.

Example: base /24 + borrow 2 → new /26.



subnet_mask = ipaddress.IPv4Network(f'0.0.0.0/{new_mask}').netmask

Creates a dummy network 0.0.0.0/new_mask just to get the dotted decimal form of the mask (e.g., 255.255.255.192), by using .netmask.


num_hosts_per_subnet = 2 ** (32 - new_mask) - 2

Calculates usable hosts per subnet:

32 - new_mask = number of host bits.

2 ** host_bits = total addresses in that subnet.

- 2 subtracts network address and broadcast address (traditional rule for usable hosts).

Note: for /31 and /32 special cases this formula needs care (see notes below).



return new_mask, subnet_mask, num_hosts_per_subnet

Returns the new CIDR mask (integer), the dotted decimal mask, and the number of usable hosts per subnet.


def main():
    print("Subnetting Demonstration Program")

main() function — entry point. Prints a title.


ip_address = input("Enter the IP address with CIDR (e.g., 192.168.1.0/24): ")
    num_subnets = int(input("Enter the number of subnets required: "))

Reads user input:

ip_address like 192.168.1.0/24.

num_subnets as an integer.



new_mask, subnet_mask, num_hosts_per_subnet = calculate_subnet_mask(ip_address, num_subnets)

Calls the function we explained and stores the results.


print("\nCalculated Subnet Mask Information:")
    print(f"Original IP Address and CIDR: {ip_address}")
    print(f"New Subnet Mask (CIDR Notation): /{new_mask}")
    print(f"New Subnet Mask (Dotted Decimal Notation): {subnet_mask}")
    print(f"Number of Hosts per Subnet: {num_hosts_per_subnet}")

Prints the results in a readable format.


if _name_ == "_main_":
    main()

Standard Python idiom: if you run this file directly, call main().


A couple of practical notes about the code

If num_subnets <= 1, log2 gives 0 or negative; borrowing 0 bits makes sense for 1 subnet — but code should ideally handle num_subnets==0 (invalid) explicitly.

If new_mask becomes > 30 you may get num_hosts_per_subnet ≤ 0 — for /31 and /32 addresses, the usual "usable hosts = 2^host_bits - 2" rule doesn’t apply the same way (see below).

If the user requests more subnets than available (borrowing more bits than host bits), new_mask could exceed 32 → invalid. The code doesn’t currently check for that.



---

Answers to your questions

What is subnetting?

Subnetting is splitting a larger IP network into smaller, separate networks (subnets). Each subnet acts like its own network with its own range of IP addresses.

Why do we need subnetting?

Efficient IP use: Avoid wasting addresses by matching network size to actual needs.

Improved performance: Smaller broadcast domains reduce unnecessary traffic.

Security & organization: Separate departments or services into isolated networks.

Simpler routing: Aggregate or control routes better inside an organization.


What is a subnet mask?

A subnet mask marks which bits of an IP address are the network part and which are the host part. In dotted decimal it looks like 255.255.255.0. In CIDR notation it’s /24. Bits set to 1 belong to the network, bits set to 0 belong to hosts.

How is subnet mask calculated?

1. Start with the network’s original mask (e.g., /24 for many Class C networks).


2. Decide how many subnets (N) you need.


3. Compute bits to borrow: bits = ceil(log2(N)).


4. New mask = original_mask + bits.


5. Convert new mask to dotted decimal if needed (e.g., /26 → 255.255.255.192).



Example: Start /24, need 4 subnets → log2(4)=2 → new mask = 24+2 = /26.

How many hosts are available per subnet for a given mask?

Use:
usable_hosts = 2^(32 - mask) - 2

mask is the CIDR number (e.g., 26).

The -2 removes the network and broadcast addresses (not usable by hosts).

Example: /26 → host bits = 6 → 2^6 - 2 = 64 - 2 = 62 usable hosts.

Special cases:
/31 (2 addresses) is used sometimes for point-to-point links — both addresses can be
 used (RFC 3021) — so the -2 rule is not applied.
/32 is a single host (only one IP) — used for a single device route.

What is CIDR notation?

CIDR = Classless Inter-Domain Routing. CIDR notation expresses the network 
prefix length after a slash: 192.168.1.0/24. The /24 means the first 24 bits are 
network bits (mask = 255.255.255.0).

Give an example of a subnet mask for a Class C network.

Typical Class C default: /24 → dotted decimal 255.255.255.0.

If you subdivide it into 4 subnets: new mask /26 → 255.255.255.192.


What is the range of private IP addresses?

Private (RFC 1918) IPv4 ranges are:

10.0.0.0 — 10.255.255.255 (10.0.0.0/8)

172.16.0.0 — 172.31.255.255 (172.16.0.0/12)

192.168.0.0 — 192.168.255.255 (192.168.0.0/16)


These addresses are not routable on the public internet and are used inside private networks.
What is the difference between network ID and host ID?

Network ID (network address): The part of the IP address that identifies the subnet. 
All hosts in the same subnet share the same network ID bits. The network address itself 
(all host bits = 0) identifies the subnet and is not assignable to hosts.

Host ID (host address): The remaining bits that identify a specific device within
 that subnet. Host bits vary between devices in the same subnet.

Example: IP 192.168.1.50/24:

Network ID = 192.168.1.0 (network portion /24)

Host ID = 0.0.0.50 (the last 8 bits in this mask)

What command or program do you use to find the subnet mask?

Common commands and tools:

Windows

ipconfig — shows IP, subnet mask, gateway (e.g., ipconfig /all).

Cross-platform / utilities

ipcalc — calculates subnets, masks, ranges (ipcalc 192.168.1.0/24).

networkctl, GUI network managers, or OS network settings.


Online

Many online subnet calculators (type ipcalc or “subnet calculator”) — useful for quick calculations.
---

Quick example with numbers (illustration)
If you run the program and input:
IP: 192.168.1.0/24
Number of subnets: 4
Calculations:
bits_to_borrow = ceil(log2(4)) = 2
new_mask = 24 + 2 = 26 → /26
subnet mask dotted = 255.255.255.192
hosts per subnet = 2^(32 - 26) - 2 = 2^6 - 2 = 64 - 2 = 62

So you get four subnets:
192.168.1.0/26 (addresses .0–.63, hosts .1–.62)
192.168.1.64/26 (addresses .64–.127, hosts .65–.126)
192.168.1.128/26 (addresses .128–.191, hosts .129–.190)
192.168.1.192/26 (addresses .192–.255, hosts .193–.254)
'''