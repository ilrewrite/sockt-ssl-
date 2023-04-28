import socket
import ssl
import os

class server_ssl:
    def build_listen(self):
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # 加载服务器所用证书和私钥
        context.load_cert_chain('cert/server.crt', 'cert/server_rsa_private.pem.unsecure')
        server_path='server_files/'
        # 监听端口
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('localhost', 8000))
            sock.listen(5)
            # 将socket打包成SSL socket，其主要工作是完成密钥协商
            with context.wrap_socket(sock, server_side=True) as ssock:
                client_socket, addr = ssock.accept()
                msg = client_socket.recv(1024).decode("utf-8")
                print(f"receive msg from client {addr}：{msg}")
                msg = f"yes , you have client_socketect with server.\n".encode("utf-8")
                client_socket.send(msg)
                while True:
                    file_name = client_socket.recv(1024).decode('utf-8')
                    if not os.path.isfile(server_path+file_name):
                        client_socket.send('not found file'.encode("utf-8"))
                        continue
                    with open(server_path+file_name, 'rb') as file:
                        client_socket.send(f'{os.stat(server_path+file_name).st_size}'.encode('utf-8'))
                        while True:
                            data=file.read(1024)
                            try:
                                client_socket.send(data)
                            except ssl.SSLEOFError:
                                pass
                            if not data:
                                print("transmit complete")
                                break
                client_socket.close()

if __name__ == "__main__":
    server = server_ssl()
    server.build_listen()