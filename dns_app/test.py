import requests

# 注册请求
url = 'http://192.168.3.200:9090/register'
jsons = {
    'hostname': 'www.test3.com',
    'ip': '172.155.53.125',
    'as_ip': '192.168.3.200',
    'as_port': "53533",
}
headers = {
    'Connection': 'close'
}
res = requests.put(url=url, json=jsons, headers=headers)
print(res.text)

# 查询请求
#url = 'http://192.168.3.200:8080/fibonacci'
#params = {
#    "hostname": "www.test2.com",
#    "fs_port": "9090",
#    "number": "15",
#    "as_ip": "192.168.3.200",
#    "as_port": "53533"
#}
#headers = {
#    'Connection': 'close'
#}
#res = requests.get(url=url, params=params, headers=headers)
#print(res.text)
