#!/usr/bin/env python3
import socket
import time
import sys

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}') 
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():

    # set the buffer size
    buffer_size = 4096

    #define address and host of socket connect with clients
    host = socket.gethostname()
    port = 8001

    #define address and host of socket connect with google
    google_host = 'www.google.com'
    google_port = 80

    google_remote_ip = get_remote_ip(google_host)

    try:
        s1 = create_tcp_socket()
        s1.connect((google_remote_ip, google_port))
        print (f'Socket Connected to {host} on ip {google_remote_ip}')
        
        s2 = create_tcp_socket()
        s2.bind((host, port))
        s2.listen(1)

        while True:
            conn, addr = s2.accept()
            print("Connected by", addr)

            #recieve data, wait a bit, then send it back
            payload = conn.recv(buffer_size)
            print("Receive Data")

            # send and receive data from google
            send_data(s1, payload)
            full_data = s1.recv(buffer_size)
            
            # send the result back
            time.sleep(0.5)
            conn.sendall(full_data)
            conn.close()
    
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s1.close()

if __name__ == "__main__":
    main()