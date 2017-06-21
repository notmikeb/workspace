#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32pipe, win32file
import msvcrt
import sys
import struct
import time
import math
import subprocess
import os

msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)

#open Wireshark, configure pipe interface and start capture (not mandatory, you can also do this manually)
wireshark_cmd=['', r'-i\\.\pipe\wireshark','-k']
if len(sys.argv) > 1:
    wireshark_cmd[0] = sys.argv[1]
else:
    wireshark_cmd[0]	 = r"C:\Program Files\Wireshark\Wireshark.exe"
    print("Caution! no assign he wireshark.exe location !")

proc=subprocess.Popen(wireshark_cmd)

#create the named pipe \\.\pipe\wireshark
pipe = win32pipe.CreateNamedPipe(
    r'\\.\pipe\wireshark',
    win32pipe.PIPE_ACCESS_OUTBOUND,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    300,
    None)

win32pipe.ConnectNamedPipe(pipe, None)

filename = r'btsnoop_hci.cap'
with open(filename, 'rb') as f:
    f.read(16)
    #sys.stdin.read(16) # read snoop log header
    pcap_header = struct.pack("<{}{}{}{}{}{}".format(
        "I",    # magic number
        "HH",   # major/minor version number
        "i",    # thiszone
        "I",    # sigfigs
        "I",    # snaplen
        "I",    # network: data link type
        ),
            0xa1b2c3d4, # magin number
            2, 4,       # major/minor version number
            0,          # thiszone (UTC)
            0,          # sigfigs
            65535,      # snaplen
            201,        # LINKTYPE_BLUETOOTH_HCI_H4_WITH_PHDR
            )

    win32file.WriteFile(pipe, pcap_header)
    myin = f
    
    while True:
        peekdata = myin.read(4)
        if peekdata:
            pass
        else:
            break
         
        print ("open okay")
        ori_len = struct.unpack(">I", peekdata)[0] # Original Length
        inc_len = struct.unpack(">I", myin.read(4))[0] # Include Length
        flag = struct.unpack(">I", myin.read(4))[0] # Packet Flags
        print ("flag {}".format(flag))
        drops = myin.read(4) # Cumulative Drops
        timestamp = myin.read(8) # Timestamp Microseconds
        print "inc_len {}".format(inc_len)
        packet = myin.read(inc_len)
        ts_usec, ts_sec = math.modf(time.time())
        ts_sec = int(ts_sec)
        ts_usec = int(ts_usec * 10**6)
        print ts_sec, ts_usec
        packet_type = ord(packet[0])
        direction = flag & 0x01
        h4_packet = struct.pack("!I{}s".format(inc_len),
                direction,
                packet
                )

        buf = struct.pack("<{}{}{}{}{}".format(
            "I",                            # timestamp seconds
            "I",                            # timestamp microseconds
            "I",                            # include length
            "I",                            # actual length
            "{}s".format(len(h4_packet)),   # packet data
            ),
                ts_sec,
                ts_usec,
                len(h4_packet),
                ori_len + 4, # remove packet type add h4 header
                h4_packet
                )

        win32file.WriteFile(pipe, buf)