import socket

def get_private_ip():
    # Get the private IP address
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    return private_ip

def write_ip_to_file(ip_address):
    with open('../components/get_ip/get_ip.js', 'w') as file:
        file.write(f'const ip_address = "{ip_address}";')


if __name__ == "__main__":
    ip_address = get_private_ip()
    write_ip_to_file(ip_address)
    print(f"Private IP address {ip_address} written to private_ip.txt")