# fs_server.py
# Fibonacci Server Implementation

from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# Dictionary to store registered Fibonacci servers
fibonacci_servers = {}

# Register Fibonacci Server with Authoritative Server
@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    print("Received registration request:", data)  
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')
    print("print 参数",hostname,ip,as_ip,as_port)

    if hostname and ip and as_ip and as_port:
        # Register Fibonacci server locally
        fibonacci_servers[hostname] = {
            'ip': ip,
            'as_ip': as_ip,
            'as_port': as_port
        }
        print(fibonacci_servers)

        # Communicate with Authoritative Server (AS) to register
        registration_message = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10"
        as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        as_address = (as_ip, as_port)
        try:
            as_socket.sendto(registration_message.encode(), as_address)
            response, _ = as_socket.recvfrom(1024)
            if response.decode() == "Registration successful":
                return "HTTP/1.1 201 Created\n\n"
            else:
                return "HTTP/1.1 500 Internal Server Error\n\nFailed to register with Authoritative Server"
        except Exception as e:
            return f"HTTP/1.1 500 Internal Server Error\n\n{str(e)}"
        finally:
            as_socket.close()

    else:
        return "HTTP/1.1 400 Bad Request\n\nMissing registration parameters"


# Calculate Fibonacci number for a given sequence number
def calculate_fibonacci(n):
    if n <= 0:
        return "Invalid input"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(3, n+1):
            a, b = b, a + b
        return b

# Handle Fibonacci requests
@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    number = int(request.args.get('number'))

    if hostname in fibonacci_servers:
        fibonacci_number = calculate_fibonacci(number)
        return jsonify({'hostname': hostname, 'fibonacci_number': fibonacci_number})
    else:
        return "HTTP/1.1 404 Not Found\n\nFibonacci server not registered for the provided hostname"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)

