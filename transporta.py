#!/usr/bin/python3
import sys
import time
import termcolor as tc
import socket
import threading
import argparse
import os
import tqdm




class __host__():
    def __init__(self, ip, port, byte_size,cmd,user):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip , port)
        self.CONN_NO = []
        self.CMD = cmd
        self.USER = user

        if byte_size == b'MAX':
            self.BYTE_SIZE = 100000000
        elif  byte_size == b'MIN':
            self.BYTE_SIZE = 100000
        elif byte_size == b'DEF':
            self.BYTE_SIZE = 1000
        self.conn = None


    def start_connection(self):
        try:
            with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as server:
                print(f'[+] binding {self.IP} to port {self.PORT}')
                server.bind(self.ADDR)
                print(f'[+] listening to port {self.PORT}')
                server.listen()
                print('[+] connection established!.')
                self.connected = True
                while self.connected:
                    conn , addr =  server.accept()
                    self.conn = conn
                    self.CONN_NO.append(addr)


                    thread =  threading.Thread(target=self.handle_connection , args=(conn,addr))
                    thread.start()
                thread._stop()
                conn.close()
        except KeyboardInterrupt:
            self.exit()
        except socket.gaierror:
            self.server_error()
        except OverflowError:
            self.server_error()
            self.exit()
        except OSError:
            self.server_error()
    def handle_connection(self, conn, addr):
        try:
            tc.cprint(f'[*] {addr} connected', 'green')
            tc.cprint(f'[*] {len(self.CONN_NO)} process handled', 'yellow')
            self.__recv__(conn,addr)
            # self.__send__(conn,addr)
        except KeyboardInterrupt:
            self.exit()



    def __recv__(self, conn, addr):
            __data__ = conn.recv(self.BYTE_SIZE)
            self.reply_bytes(conn, addr, __data__)
            self.reply_buffer(conn, addr , __data__)
    def reply_buffer(self, conn , addr, __data__):
        check_transport = b',' in  __data__ and b'/' in __data__ and b'<DRAG>' not in __data__
        check_drag = b'<DRAG>' in __data__
        if check_transport:
            INFO = __data__.decode().split(',')
            local_file_dest = INFO[0]
            remote_file_dest = INFO[1]
            TRANSPORT = transport(conn, local_file_dest, remote_file_dest)
            TRANSPORT.send()
        elif check_drag:
            INFO = __data__.decode().split(',')
            INFO.remove('<DRAG>')

            remote_file_name = INFO[0].strip()
            remote_file_name = remote_file_name.split('/')

            remote_file_dest = INFO[1] + '/' + remote_file_name[-1]
            local_file_dest = INFO[0]
            file_size = INFO[2]
            DRAG = drag(conn, remote_file_dest, local_file_dest, file_size)
            DRAG.recv()
        else:
            pass
    def reply_bytes(self,conn,addr, __data__):
        check_transport = b',' in  __data__ and b'/' in __data__
        if __data__ == b'exit':
            tc.cprint(f'[!] {addr} diconnected!.')
            self.CONN_NO.remove(addr)
            tc.cprint(f'{ len(self.CONN_NO)} is active process')
            self.conn.send(b'byee')
        elif __data__ == b'hello':
            conn.send(b'I am up on port ' + bytes(str(self.PORT) , 'utf-8'))
        elif __data__ == b'':
            conn.send(b'recv!')
        else:
            if check_transport:
                pass
            else:
                tc.cprint(f'[+] {addr} says {__data__}' , 'green')
                conn.send(b'recv!')


    # def __send__(self, conn , addr, cmd):
    #     if cmd == 'send':
    #         self.conn.send(b'recv!')
    #     else:
    #         pass

    def exit(self):
        tc.cprint('[!] exit.!', 'red')
        sys.exit()
    def server_error(self):
        tc.cprint('[!] unable to create server!')
        sys.exit()
    def close_connection(self):
        try:
            self.conn.shutdown(socket.SHUT_WR)
            self.conn.close()
        except AttributeError:
            self.exit()
        except Exception:
            self.exit()



global host
host = __host__


class __client__():
    def __init__(self, ip, port, cmd,value, USER):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip , port)
        self.CONN_NO = []
        self.BYTE_SIZE_MAX = 100000000
        self.BYTE_SIZE_MIN = 100000
        self.BYTE_SIZE_DEF = 1000
        self.CMD = cmd
        self.VALUE = value
        self.USER = USER

    def start_connection(self):
        try:
            with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as server:
                print(f'[+] connecting to {self.IP} on port {self.PORT}')
                print('[+] connected!.')
                self.connected = True
                self.conn = server
                server.connect(self.ADDR)
                self.handle_connection(self.conn)
                # thread = threading.Thread(target=self.handle_connection , args=(self.conn , ))
                # thread.start()
                # thread._stop()
        except KeyboardInterrupt:
            self.conn.send(b'exit')
            self.exit()
        except socket.gaierror:
            self.server_error()
        except ConnectionRefusedError:
            tc.cprint(f'[!] {self.IP} is down on port {self.PORT}!' , 'red')
            sys.exit()
        except Exception:
            tc.cprint(f'[!] unable to reach to {self.IP}')
            sys.exit()
    def handle_connection(self, conn):
        if self.CMD == 'send':
            self.__send__(self.conn, self.VALUE)
            self.send_transport_info(self.VALUE)
        elif self.CMD == 'drag':
            self.send_drag_info(self.VALUE)
        elif self.CMD == 'transport' or self.CMD == 'recv':
            self.send_transport_info(self.VALUE)
            #self.__recv__()




    def handle_active_conn_count(self):
        self.CONN_NO = host.__host__(self.IP, self.PORT).CONN_NO

    def __recv__(self, conn , __data__):

            try:
                print(f'[+] {__data__}')
                tc.cprint(f'[+] {len(__data__)} byte(s) is recv!.', 'yellow')
                print('[#] done!')
                self.conn.close()
                self.exit()
            except OSError:
                self.exit()

    def __send__(self, conn, __data__):
        data_len = len(__data__)
        try:
            tc.cprint(f'[+] sending bytes..', 'green' )
            self.conn.send(__data__)
            tc.cprint(f'[+] {data_len} bytes(s) sent.', 'yellow')
            __data__ = self.conn.recv(self.BYTE_SIZE_MAX)
            self.__recv__(self.conn , __data__)

        except KeyboardInterrupt:
            self.conn.send(b'exit')
            self.conn.close()
            self.exit()
    def send_transport_info(self, INFO):
        try:
            tc.cprint('[+] sending resources info...', 'green')
            self.conn.send(INFO)
            tc.cprint('[+] info is sent!...' , 'yellow')
            print('[#] done sending info!')
            tc.cprint('[+] waiting for reply...', 'yellow')
            incoming_bytes = self.conn.recv(self.BYTE_SIZE_MAX)
            tc.cprint('[+] feedback is recv...', 'green')
            check =  b'<TRANSPORT>' in incoming_bytes
            if check:
                __data__ = incoming_bytes.split(b"<TRANSPORT>")
                file_size = int(__data__[0].decode())
            else:
                self.close_connection()
            FILE = INFO.decode().split(',')
            file_dest_dir = FILE[0].strip()
            check_backw_splash = '\\' in FILE[1]
            check_forw_splash = '/' in FILE[1]
            if check_backw_splash:
                file_name = FILE[1].split('\\')
                file_name = file_name[-1]
                file_name = file_dest_dir + '/' + file_name
            elif check_forw_splash:
                file_name = FILE[1].split('/')
                file_name = file_name[-1]
                file_name = file_dest_dir + '/' + file_name
            else :
                file_name = file_name = FILE[1].split('/')
                file_name = file_name[-1]
                file_name = file_dest_dir + '/' + file_name
            
                

            progress = tqdm.tqdm(range(file_size) ,  f'[+] transporting data into {file_name.strip()}...' , unit='B' , unit_scale=True)
            with open(file_name.strip(), 'wb') as f:
                for _ in progress:
                    incoming_bytes = self.conn.recv(self.BYTE_SIZE_MAX)
                    if not incoming_bytes:
                        break
                    f.write(incoming_bytes)
                    progress.update(file_size)
            tc.cprint(f'[+] {file_name} is successfully transported', 'yellow')
            self.close_connection()
        except FileNotFoundError as msg:
            tc.cprint(f'[!] error allocating resources:' +  msg)
            self.exit()
        except Exception as msg:
            print(msg)
            self.exit()
    def send_drag_info(self, INFO):
        try:
            tc.cprint('[+] sending resources info...', 'green')
            FILE = INFO.decode().split(',')
            file_size = os.path.getsize(FILE[0].strip())
            file_name = FILE[0].strip()

            self.conn.send(INFO + b',' + str(file_size).encode()  + ',<DRAG>'.encode())
            # incoming_bytes = self.conn.recv(self.BYTE_SIZE_MAX)
            # print(incoming_bytes)
            progress = tqdm.tqdm(range(file_size) ,  f'[+] dragging {file_name}...' , unit='B' , unit_scale=True)
            with open(file_name.strip(), 'rb') as f:
                for _ in progress:
                    outgoing_bytes = f.read(file_size)
                    if not outgoing_bytes:
                        break
                    self.conn.sendall(outgoing_bytes)
                    progress.update(file_size)
            tc.cprint(f'[+] {file_name} is successfully dragged to remote dest {FILE[1]}', 'yellow')
            self.close_connection()
        except FileNotFoundError:
            tc.cprint(f'[!] error allocating resources')
            self.exit()
        except Exception:
            self.exit()

    def exit(self):
        tc.cprint('[!] exit.!', 'red')
        sys.exit()
    def server_error(self):
        tc.cprint('[!] unable to create server!')
        sys.exit()
    def close_connection(self):
        try:
            self.conn.shutdown(socket.SHUT_WR)
            self.conn.close()
            self.exit()
        except AttributeError:
            self.exit()
        except Exception:
            self.exit()

global client
client = __client__


class __drag__():
    def __init__(self,conn,remote_file_dest , local_file_dest, file_size):
        self.conn = conn
        self.REMOTE_FILE_DEST = remote_file_dest.strip()
        self.LOCAL_FILE_DEST = local_file_dest.strip()
        self.FILE_SIZE = int(file_size)
    def recv(self):
        try:
            progress = tqdm.tqdm(range(self.FILE_SIZE), f'[+] dragging {self.REMOTE_FILE_DEST}...' , unit='B', unit_scale=True)
            with open(self.REMOTE_FILE_DEST, 'wb') as _file_:
                for _ in progress:
                    _bytes_ = self.conn.recv(self.FILE_SIZE)
                    if not _bytes_:
                        break
                    _file_.write(_bytes_)
                    progress.update(self.FILE_SIZE)
                self.conn.close()
                print('[#] done!.')
        except FileNotFoundError:
            self.allocation_resources_error()
        except Exception:
           self.error_encountered()

    def allocation_resources_error(self):
        tc.cprint(f'[!] unable to allocate data resources!')
        self.exit()
    def error_encountered(self):
        tc.cprint('[!] draga is unable to trasport data!')
        self.exit()
    def exit(self):
        print('[#] done!.')
        sys.exit()


global drag 
drag = __drag__




class __transport__():
    def __init__(self,conn, local_file_dest , remote_file_dest ):
        self.conn = conn
        self.LOCAL_FILE_DEST = local_file_dest.strip()
        self.REMOTE_FILE_DEST = remote_file_dest.strip()
    def send(self):
        try:

            file_name = self.REMOTE_FILE_DEST.split('/')
            file_name = file_name[-1]
            file_size = os.path.getsize(self.REMOTE_FILE_DEST)
            self.conn.send(str(file_size).encode() + b'<TRANSPORT>')


            progress = tqdm.tqdm(range(file_size), f'[+] transporting {file_name}...' , unit='B', unit_scale=True)
            with open(self.REMOTE_FILE_DEST, 'rb') as _file_:
                for _ in progress:
                    _bytes_ = _file_.read()
                    if not _bytes_:
                        break
                    self.conn.sendall(_bytes_)
                    progress.update(file_size)
                self.conn.close()
                print('[#] done!.')


        except FileNotFoundError:
            self.allocation_resources_error()
        except Exception:
           self.error_encountered()

    def allocation_resources_error(self):
        tc.cprint(f'[!] unable to allocate data resources!')
        self.exit()
    def error_encountered(self):
        tc.cprint('[!] transporta is unable to transport data!')
        self.exit()
    def exit(self):
        print('[#] done!.')
        sys.exit()


global transport 
transport = __transport__
class transporta():   
    def arg_parser(self):    
        parser = argparse.ArgumentParser(description='transporta.')
        parser.add_argument('-H', '--host' ,action='store_true',   help='start transporta as host.')
        parser.add_argument('-C', '--client',action='store_true',   help='start transporta as client.')
        parser.add_argument('-s', '--send' , action='store_true', help='send bytes or buffer.')
        parser.add_argument('-st', '--set' , action='store_true', help='set byte size to be send or recv per time stamp for host.')
        parser.add_argument('-t', '--transport', action='store_true', help='transport buffer/bytes from a remote machine to your machine.')
        parser.add_argument('-d', '--drag', action='store_true', help='drag bytes/buffer from your machine to a remote  machine.')

        parser.add_argument('ip', type=str  , help='ip.')
        parser.add_argument('port', type=int  , help='port.')
        parser.add_argument('byte', type=str , help='bytes to send/ bytes sent can be use to config communication protocol.')
       
        args = parser.parse_args()

        

        self.HOST =  args.host
        self.CLIENT = args.client
        self.IP = args.ip
        self.PORT = args.port
        self.SEND = args.send
        self.SEND_BYTE = args.byte.encode()
        self.TRANSPORT = args.transport
        self.DRAG = args.drag
        self.SET = args.set
        self.handle_args()
        
    def handle_args(self):
        if self.HOST:
            if self.TRANSPORT:
                print('[!] host can not use --transport on intializing use --host-transport instead.')
                sys.exit()
            
            if self.SEND_BYTE == b'MIN' or self.SEND_BYTE == b'MAX' or self.SEND_BYTE == b'DEF':
                if self.SET:
                    self.handle_host(self.SEND_BYTE, 'send', 'host')
                elif self.TRANSPORT:
                    self.handle_host(self.SEND_BYTE, 'transport', 'host')
            else:
                print('[!] invalid byte config it can either be:\nMAX(100 000 000)\nMIN(100 000)\nDEF(1000)')
                sys.exit()

        elif self.CLIENT:
            if self.SEND_BYTE != b'MIN' or self.SEND_BYTE != b'MAX' or self.SEND_BYTE != b'DEF':
                if self.SEND:
                    self.send_bytes(self.SEND_BYTE , 'client')
                elif self.TRANSPORT:
                  self.handle_transport(self.SEND_BYTE, 'client')
                elif self.DRAG:
                    self.handle_drag(self.SEND_BYTE, 'client')
                
    def handle_host(self, byte_size,CMD,USER):
        __HOST__ = host(self.IP, self.PORT, byte_size, CMD, USER)
        __HOST__.start_connection()
    def handle_client(self, CMD , VALUE, USER):
        __client__ = client(self.IP, self.PORT, CMD, VALUE, USER)
        __client__.start_connection()

    def send_bytes(self, value, USER):
        self.handle_client('send', value,USER)
    def handle_transport(self, byte_value, USER):
        self.handle_client('transport', byte_value , USER)
    def handle_drag(self, byte_value, USER):
        self.handle_client('drag', byte_value , USER)



TRANSPORTA = transporta()
TRANSPORTA.arg_parser()