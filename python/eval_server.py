from threading import Thread
from subprocess import run

class ConnectionThr(Thread):
    def __init__(self, conn):
        print("New connection")
        super(ConnectionThr, self).__init__()
        self.conn = conn
        self.alive = True
        
    def run(self):
        while self.alive:
            data = self.conn.recv(8192)
            print("Got data")
            if data[0] == 0:
                print("Closing")
                self.alive = False
            else:
                try:
                    open("__src.py")
                except FileNotFoundError:
                    mode = "xb"
                else:
                    mode = "wb"
                with open("__src.py", mode) as f:
                    f.write(data)
                res = run(["python", "__src.py"], capture_output=True)
                self.conn.send(res.stdout)
        self.conn.close()
        
if __name__ == '__main__':
    from socket import create_server
    
    def handle_conn(c):
        ConnectionThr(c).start()
        
    server = create_server(('localhost', 33797))
    while True:
        c, _ = server.accept()
        handle_conn(c)