# as_server.py
# Authoritative Server Implementation

import socket

# Load DNS records from a file
def load_dns_records(file_path):
    dns_records = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                name, ip, ttl = line.strip().split(",")
                dns_records[name] = (ip, int(ttl))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return dns_records

# Write DNS records to a file
def save_dns_records(file_path, dns_records):
    with open(file_path, "w") as file:
        for name, (ip, ttl) in dns_records.items():
            file.write(f"{name},{ip},{ttl}\n")

# Handle DNS registration requests
def handle_registration(data, dns_records):
    try:
        data = data.decode().strip().split(',')
        hostname, ip, ttl = data[0], data[1], data[2]
        dns_records[hostname] = (ip, int(ttl))
        save_dns_records("dns_records.txt", dns_records)
        return "HTTP/1.1 201 Created\n\n"
    except Exception as e:
        print(f"Registration failed: {str(e)}")
        return f"HTTP/1.1 400 Bad Request\n\n{str(e)}"

# Handle DNS queries
def handle_dns_query(query, dns_records):
    try:
        query_name = query.decode().strip()
        if query_name in dns_records:
            ip, ttl = dns_records[query_name]
            response = f"TYPE=A\nNAME={query_name} VALUE={ip} TTL={ttl}\n"
            return response
        else:
            return f"HTTP/1.1 404 Not Found\n\nDNS entry not found for {query_name}"
    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\n\n{str(e)}"

# Main function to run the Authoritative Server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    dns_records = load_dns_records("dns_records.txt")
    
    print("Authoritative DNS Server is running...")
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        response = None
        
        # Check if it's a registration request or a DNS query
        try:
            data_str = data.decode().strip()
            if data_str.startswith("REGISTER"):
                response = handle_registration(data_str[8:], dns_records)
            elif data_str.startswith("QUERY"):
                response = handle_dns_query(data_str[5:], dns_records)
        except Exception as e:
            response = f"HTTP/1.1 500 Internal Server Error\n\n{str(e)}"
        
        # Send the response back to the client
        if response:
            server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()

