#!/usr/bin/env python3
import sys
import struct
import os
import socket


try:
    host = sys.argv[1]
    files = sys.argv[2:]
    port = 5000
except:
    sys.exit("Usage: sockfile.py <ip> <files>")


try:
    s = socket.socket()
    s.connect((host, port))
    s.send(struct.pack('!I', len(files)))

    for file in files:
        f = open(file, 'rb')

        print('Sending', f.name)
        i = 0
        size = os.path.getsize(file)
        l = struct.pack('!Q', size)
        s.send(l)

        if s.recv(1) == b'\x00':
            raise Exception()

        while l:
            l = f.read(1024 * 256)
            s.send(l)
            percentage = min(round((i / (size / (1024 * 256))) * 100, 2), 100)
            print('\r' * 16, 'Sending...', percentage, '%   ', end='')
            i += 1
        f.close()
        print("\nFile sent successfully.")
    s.close()
except FileNotFoundError:
    sys.exit(file + " does not exist.")
except Exception:
    sys.exit("Send cancelled by remote.")
finally:
    try:
        f.close()
        s.close()
    except:
        pass
