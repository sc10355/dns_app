# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import socket

import json

app = Flask(__name__)


def register_with_as(hostname, ip, as_ip, as_port):
    data = f'REGISTER\nHOSTNAME={hostname}\nIP={ip}'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data.encode('utf-8'), (as_ip, as_port))
        data, addr = s.recvfrom(1024)
        message = data.decode('utf-8')
        return message


@app.route('/register', methods=['PUT'])
def register():
    data = json.loads(request.data.decode('utf-8'))
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')
    try:
        as_port = int(as_port)
    except ValueError:
        return "Bad Request", 400
    message = register_with_as(hostname, ip, as_ip, as_port)
    return message, 201


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    number = int(request.args.get('number'))
    response = requests.get(f'http://{hostname}/fibonacci?number={number}')
    return response.text, response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
