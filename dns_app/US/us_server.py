# -*- coding: utf-8 -*-
import socket
import requests
from flask import Flask, request

app = Flask(__name__)



def query_dns(hostname,as_ip,as_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        query_message = f'FIBONACCI\nTYPE=A\nHOSTNAME={hostname}\n'
        s.sendto(query_message.encode('utf-8'), (as_ip, as_port))
        data, addr = s.recvfrom(1024)
        response = data.decode('utf-8')
        return response


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not (hostname and fs_port and number and as_ip and as_port):
        return "Bad Request", 400

    try:
        number = int(number)
        fs_port = int(fs_port)
        as_port = int(as_port)
    except ValueError:
        return "Bad Request", 400

    # Query DNS for FS IP
    fs_ip_data = query_dns(hostname,as_ip,as_port)

    if fs_ip_data[:4] == 'Type':
        # Send Fibonacci request to FS service
        return fs_ip_data, 201
    else:
        return fs_ip_data, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
