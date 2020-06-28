import socket
import threading
import io

class ConnectionThr(threading.Thread):
    def __init__(self, conn):
        super(ConnectionThr, self).__init__()
        self.conn = conn
        self.stream = io.BytesIO()
        self.filename = ""
        self.alive = True
        print("New connection thread")

    def packet(self, op, data):
        print(f"received packet: op={op} data={data}")
        if op == 0x00:
            self.filename = data.decode("utf-8")
            self.stream.seek(0)
            self.stream.flush()
        elif op == 0xFF:
            self.stream.seek(0)
            try:
                open(self.filename)
            except FileNotFoundError:
                with open(self.filename, "xb") as f:
                    f.write(self.stream.read())
            else:
                with open(self.filename, "wb") as f:
                    f.write(self.stream.read())
            self.stream.close()
            self.conn.close()
            self.alive = False
        elif op == 0x0F:
            self.stream.write(data)
        
    def run(self):
        print("is running")
        while self.alive:
            data = self.conn.recv(2048)
            self.packet(data[0], data[1:])
        print("finished")
            
if __name__ == '__main__':
    sock = socket.create_server(("localhost", 33787))
    while True:
        c, i = sock.accept()
        ConnectionThr(c).start()