import socket
import ssl

class client_ssl:
    def send_hello(self,):
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # 加载信任根证书
        context.load_verify_locations('cert/ca.crt')
        client_path='client_files/'
        # 与服务端建立socket连接
        with socket.create_connection(('localhost', 8000)) as sock:
            # 将socket打包成SSL socket，其主要工作是完成密钥协商
            with context.wrap_socket(sock, server_hostname='SERVER') as ssock:
                # 向服务端发送信息
                msg = "do i connect with server ?".encode("utf-8")
                ssock.send(msg)
                # 接收服务端返回的信息
                msg = ssock.recv(1024).decode("utf-8")
                print(f"receive msg from server : {msg}")
                while True:
                    file_name=input('please input file that you want to get:')
                    ssock.send(file_name.encode("utf-8"))
                    file_size=ssock.recv(1024).decode("utf-8")
                    if file_size=='not found file':
                        print('file is not exist!')
                        continue
                    file_size=int(file_size)
                    recv_size=0
                    with open(client_path+file_name,'wb') as file:
                        while recv_size<file_size:
                            if file_size - recv_size > 1024:
                                data = ssock.recv(1024)
                                recv_size += 1024
                            else:
                                data=ssock.recv(file_size-recv_size)
                                recv_size = file_size
                            file.write(data)
                ssock.close()

if __name__ == "__main__":
    client = client_ssl()
    client.send_hello()