import socket
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor


COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

def scan_host(ip, ports=COMMON_PORTS):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)  # Set timeout for each port check
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return ip, open_ports

def scan_network(network):
    results = []

    try:
        ip_net = ip_network(network, strict=False)
        ip_list = [str(ip) for ip in ip_net.hosts()]
    except ValueError:
        try:
            ip = socket.gethostbyname(network)
            ip_list = [ip]
        except socket.gaierror:
            return []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_host, ip) for ip in ip_list]
        for future in futures:
            ip, open_ports = future.result()
            if open_ports:
                results.append((ip, open_ports))
    return results

