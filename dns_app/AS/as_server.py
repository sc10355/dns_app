# -*- coding: utf-8 -*-
import socket
import json
import re

AS_IP = '0.0.0.0'
AS_PORT = 53533

dns_records = {}


def save_to_file():
    with open("dns_records.json", "w") as file:
        json.dump(dns_records, file)


def load_from_file():
    try:
        with open("dns_records.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# 校验IP合法性
def ip_range(ip):
    ip_list = ip.split('.')
    for num in ip_list:
        if int(num) < 0 or int(num) > 255:
            return False
    return True


# 校验输入合法性
def is_valid_ip(ip, hostname):
    hostname_format = re.match(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', hostname)
    check_hostname = True if hostname_format else False

    ip_format = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', ip)
    check_ip_format = True if ip_format else False

    if check_hostname and check_ip_format:
        check_ip_range = ip_range(ip)
        if check_ip_range:
            return True
        else:
            return False
    else:
        return False

dns_records = load_from_file()


def register(hostname, ip):
    dns_records[hostname] = {"ip": ip, "ttl": 10}
    save_to_file()
    print(f'Registration successful for {hostname}.')


def handle_dns_query(hostname):
    if hostname in dns_records:
        response_message = f'TYPE=A, NAME={hostname}, VALUE={dns_records[hostname]["ip"]}, TTL={dns_records[hostname]["ttl"]}'
        print(f'DNS response sent for {hostname}.')
        return response_message
    else:
        return "Not Found"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((AS_IP, AS_PORT))
        print(f"AS server listening on {AS_IP}:{AS_PORT}")
        while True:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8')
            message_parts = message.split('\n')
            deal_type = message_parts[0]
            if deal_type == 'REGISTER':
                if len(message_parts) >= 3:
                    _, hostname, ip = message_parts[:3]

                    # 处理注册请求
                    if "HOSTNAME=" in hostname and "IP=" in ip:
                        hostname = hostname[9:]
                        ip = ip[3:]
                        check_ip = is_valid_ip(ip, hostname)
                        if not check_ip:
                            response = "IP or HostName exception"
                        else:
                            # 处理注册逻辑
                            register(hostname, ip)
                            response = "Registration successful"
                    else:
                        response = "Params Format exception"
                else:
                    response = "Params Num exception"
            elif deal_type == 'FIBONACCI':
                if len(message_parts) >= 3:
                    _, type_, hostname = message_parts[:3]
                    if "TYPE=" in type_ and "HOSTNAME=" in hostname:
                        hostname = hostname[9:]
                        # 处理注册逻辑
                        search_data = dns_records.get(hostname)
                        if not search_data:
                            response = 'IP not fund'
                        else:
                            response = f'Type=A\nNAME={hostname}\nVALUE={search_data["ip"]}\nTTL={search_data["ttl"]}'
                    else:
                        response = "Params Format exception"
                else:
                    response = "Params Num exception"
            else:
                response = "Params Header exception"
            print(response)
            s.sendto(response.encode('utf-8'), addr)


if __name__ == "__main__":
    main()
