package main

import (
	"bytes"
	"fmt"
	"net"
	"os"
)

func main() {
	server, err := net.Listen("tcp", ":33787")
	if err != nil {
		onErr(err)
		return
	}
	fmt.Println("Listening...")
	i := 0
	for {
		conn, err := server.Accept()
		if err != nil {
			onErr(err)
			return
		}
		fmt.Printf("[%d] Incoming connection\n", i)
		go connHandler(conn, i)
		i++
	}
}

func connHandler(c net.Conn, id int) {
	var (
		fname   string
		fbuffer = bytes.Buffer{}
	)

	for {
		packet := make([]byte, 8*1024)
		n, err := c.Read(packet)
		if err != nil {
			onErr(err)
			goto close
		}
		op := packet[0]
		data := packet[1:n]

		switch op {
		case 0:
			fname = string(data)
			fmt.Printf("[%d] Filename: %s\n", id, fname)
		case 0x0F:
			n, _ := fbuffer.Write(data)
			fmt.Printf("[%d] Received %d bytes\n", id, n)
		case 0xFF:
			if len(fname) == 0 || fbuffer.Len() == 0 {
				goto close
			}
			fd, err := os.Create(fname)
			if err != nil {
				onErr(err)
				goto close
			}
			fmt.Printf("[%d] Dumping\n", id)
			fbuffer.WriteTo(fd)
			goto close
		}
	}
close:
	fmt.Printf("[%d] Closing connection\n", id)
	c.Close()
}

func onErr(err error) {
	fmt.Println("\nAn error has occured:")
	fmt.Println("\t" + err.Error())
}
