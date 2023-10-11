import requests

# registration request
#url = 'http://192.168.3.198:30002/register'
#jsons = {
#    'hostname': 'www.test4.com',
#    'ip': '172.155.53.125',
#    'as_ip': '192.168.3.198',
#    'as_port': "30001",
#}
#headers = {
#    'Connection': 'close'
#}
#res = requests.put(url=url, json=jsons, headers=headers)
#print(res.text)

# query request
url = 'http://192.168.3.198:30003/fibonacci'
params = {
    "hostname": "www.test4.com",
    "fs_port": "30002",
    "number": "15",
    "as_ip": "192.168.3.198",
    "as_port": "30001"
}
headers = {
    'Connection': 'close'
}
res = requests.get(url=url, params=params, headers=headers)
print(res.text)
