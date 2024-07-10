import socket
from scapy.all import DNS, DNSRR
import requests


def get_ad_domains():
    download_url = 'https://hosts.anudeep.me/mirror/adservers.txt'
    ad_domains = []
    for line in requests.get(download_url).text.splitlines():
        if line[0] == '#':
            continue
        ad_domains.append(line.split()[1].strip())
    return sorted(ad_domains)


def binary_search(list, x):
    s = 0
    d = len(list) - 1
    while s <= d:
        m = (s+d)//2
        if list[m] == x or list[m] == x[:-1]: #:-1 pentru ca am vazut ca domeniile care dau request au un '.' la final
            return True
        if x < list[m]:
            d = m - 1
        else:
            s = m + 1
    return False

#Sursa: https://github.com/senisioi/computer-networks/tree/2023/capitolul6#scapy_dns
def main():
    ad_domains = get_ad_domains()
    simple_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    simple_udp.bind(('0.0.0.0', 53))
    while True:
        request, adresa_sursa = simple_udp.recvfrom(65535)

        packet = DNS(request)
        dns = packet.getlayer(DNS)
        
        if dns is not None and dns.opcode == 0: 
            print("Received DNS query from:", adresa_sursa)
            print(packet.summary())

            domain = dns.qd.qname.decode().strip()
            print("Domain:"+domain)

            if binary_search(ad_domains, domain):
                
                print('BLOCKED!!! ' + domain)
                with open('blocked_domains.txt', 'a') as f:
                    f.write(domain+'\n')
                    f.flush()
                dns_answer = DNSRR(
                    rrname=dns.qd.qname,  
                    ttl=330, 
                    type="A",
                    rclass="IN",
                    rdata='0.0.0.0'
                )

                dns_response = DNS(
                    id=packet[DNS].id,  # DNS replies must have the same ID as requests
                    qr=1,  # 1 for response, 0 for query
                    aa=0,  # Authoritative Answer
                    rcode=0,  # 0, nicio eroare
                    qd=packet.qd,  # request-ul original
                    an=dns_answer  # obiectul de reply
                )

                print("Sending DNS response:")
                print(dns_response.summary())

                simple_udp.sendto(bytes(dns_response), adresa_sursa)
            else:

                print("Allowing DNS query:", domain[:-1])

    simple_udp.close()


main()
