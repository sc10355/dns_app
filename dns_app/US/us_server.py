# us_server.py
# User Server Implementation
from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# Handle Fibonacci requests from users
@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = int(request.args.get('number'))
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))
    
    # Validate parameters
    if not hostname or not fs_port or not as_ip or not as_port:
        return "HTTP/1.1 400 Bad Request\n\nMissing parameters"
    
    # Resolve hostname to IP address using Authoritative Server (AS)
    dns_query = f"TYPE=A\nNAME={hostname}"
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        dns_socket.sendto(dns_query.encode(), (as_ip, as_port))
        fs_ip, _ = dns_socket.recvfrom(1024)
    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\n\n{str(e)}"
    finally:
        dns_socket.close()

    # Query Fibonacci Server (FS) for Fibonacci number
    fs_response = None
    try:
        fs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fs_socket.connect((fs_ip, int(fs_port)))
        fs_socket.send(f'/fibonacci?number={number}'.encode())
        fs_response = fs_socket.recv(1024)
    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\n\n{str(e)}"
    finally:
        fs_socket.close()

    return fs_response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

