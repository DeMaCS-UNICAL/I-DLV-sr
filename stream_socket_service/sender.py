#!/usr/bin/env python3

import sys
import socket
import time
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#PORT = 9000        # Port to listen on (non-privileged ports are > 1023)
print("period ",float(sys.argv[1]), " events to send ",int(sys.argv[2]), "log file ", str(sys.argv[3]), "port ",int(sys.argv[4]))
max_events=int(sys.argv[2])
PORT =int(sys.argv[4])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    try:
        with conn:
            print('Connected by', addr)
        
            file1 = open(str(sys.argv[3]), 'r') 
            n_events=0
            while True: 
            # Get next line from file 
                line = file1.readline() 
            
            # if line is empty 
            # end of file is reached 
                if not line or n_events>=max_events: 
                    break
                conn.sendall(line.encode())
                #print('sent', line)
                n_events+=1
                time.sleep(float(sys.argv[1]))
            file1.close() 
    except:
        s.close()
    s.close()
     
       
