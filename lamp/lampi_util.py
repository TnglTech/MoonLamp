import socket
import fcntl
import struct

DEVICE_ID_FILENAME = '/sys/class/net/eth0/address'


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
    except Exception:
        return ''


def get_device_id():
    try:
        mac_addr = open(DEVICE_ID_FILENAME).read().strip()
        return mac_addr.replace(':', '')
    except Exception:
        return 'UNKNOWN'
