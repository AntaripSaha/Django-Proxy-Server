import requests
import json
import os
import subprocess
import re
from django.http import HttpResponse
from django.shortcuts import render


def active_ips(request):

    url = 'https://proxylist.geonode.com/api/proxy-list?limit=30&page=1&sort_by=lastChecked&sort_type=desc'
    response = requests.get(url)
    data_str = response.content
    data_dict = json.loads(data_str)
    sorted_data = sorted(data_dict["data"], key=lambda x: x["latency"])
    ip_ports = [(d["ip"], d["port"]) for d in sorted_data]
    print('active ips searching')
    # Write the IP addresses and ports to a text file
    with open("data.txt", "w") as f:
        for ip, port in ip_ports:
            f.write(f"{ip}:{port}\n")

    # Pass the list of IP addresses and ports to the template
    context = {"ip_ports": ip_ports}
    # Open the data file and read all IP addresses and ports
    with open("data.txt", "r") as f:
        ip_ports = [line.strip() for line in f.readlines()]

    # Ping each IP and write the ones without any lost packets to a new file
    with open("available_ips.txt", "w") as f:
        for ip_port in ip_ports:
            ip, port = ip_port.split(":")
            # Use the appropriate command for your OS to ping the IP address
            # In this example, we're using the Windows ping command
            response = os.system(f"ping -n 1 {ip}")
            if response == 0:
                f.write(f"{ip}:{port}\n")

    return HttpResponse("Finished pinging IPs and wrote available IPs to file.")
    # return render(request, "available_ips.html", context)


def ping_ips(request):
    # Open the data file and read all IP addresses and ports
    with open("data.txt", "r") as f:
        ip_ports = [line.strip() for line in f.readlines()]

    # Ping each IP and write the ones without any lost packets to a new file
    with open("available_ips.txt", "w") as f:
        for ip_port in ip_ports:
            ip, port = ip_port.split(":")
            # Use the appropriate command for your OS to ping the IP address
            # In this example, we're using the Windows ping command
            response = os.system(f"ping -n 1 {ip}")
            if response == 0:
                f.write(f"{ip}:{port}\n")

    return HttpResponse("Finished pinging IPs and wrote available IPs to file.")


def available_ips(request):
    # Open the available IPs file and read all IP addresses and ports
    with open("available_ips.txt", "r") as f:
        ips = [line.strip() for line in f.readlines()]

    context = {'ips': ips}
    return render(request, 'available_ips.html', context)


# def set_proxy(request, ip_port):
#     # Set the proxy to the selected IP address and port
#     os.environ["http_proxy"] = f"http://{ip_port}"
#     os.environ["https_proxy"] = f"http://{ip_port}"
#
#     # Check if the proxy has been set correctly
#     result = subprocess.run(['curl', '-s', 'https://ipinfo.io/ip'], stdout=subprocess.PIPE)
#     current_ip = result.stdout.decode('utf-8').strip()
#     if current_ip == ip_port.split(":")[0]:
#         return HttpResponse(f"Proxy set to {ip_port}")
#     else:
#         return HttpResponse("Error setting proxy")


def set_proxy(request, ip_port):
    # Set the proxy to the selected IP address and port
    os.environ["http_proxy"] = f"http://{ip_port}"
    os.environ["https_proxy"] = f"http://{ip_port}"

    # Debug print statements
    print(f"Selected IP address and port: {ip_port}")
    print(f"http_proxy: {os.environ.get('http_proxy')}")
    print(f"https_proxy: {os.environ.get('https_proxy')}")

    # Check if the environment variables are set correctly
    if os.environ.get("http_proxy") == f"http://{ip_port}" and os.environ.get("https_proxy") == f"http://{ip_port}":
        proxies = {"http": f"http://{ip_port}", "https": f"http://{ip_port}"}
        response = requests.get('https://api.myip.com', proxies=proxies)
        return HttpResponse(f"Your Current IP is: {response.text.strip()}")
    else:
        return HttpResponse("Error setting proxy")
