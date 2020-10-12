package main

import (
    "net"
    "log"
    "strings"
    "math/rand"
    "strconv"
)

var CAN_SET_FLAG = true
var START_PORT = 12000
var END_PORT = 13000

func main() {
    listener, err :=  net.Listen("tcp", ":5000")
    if err != nil {
        log.Fatal(err)
    }

    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Println(err)
        }
        go handleConnection(conn)
    }
}

func handleConnection(conn net.Conn) {
    defer conn.Close()

    secret, ln := startUdpServer()
    if secret == "" || ln == nil {
        conn.Write([]byte("No room\n"))
        return
    }
    parts := strings.Split(ln.LocalAddr().String(),":")
    conn.Write([]byte("use this secret: "+secret+"\nuse this UDP Port: "+parts[len(parts)-1]+"\n"))  
    go runUdpServer(secret, ln)
}

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func randStringRunes(n int) string {
    b := make([]rune, n)
    for i := range b {
        b[i] = letterRunes[rand.Intn(len(letterRunes))]
    }
    return string(b)
}

func startUdpServer() (string,*net.UDPConn) {
    for port := START_PORT; port <= END_PORT; port++ {
        listenAddr, err := net.ResolveUDPAddr("udp", ":"+strconv.Itoa(port))
        for err != nil {
            log.Fatal(err)
        }
        ln, err := net.ListenUDP("udp", listenAddr) 
        if err == nil {
            secret := randStringRunes(20)
            log.Printf("startUdpServer port: %v secret: %v\n", port, secret)
            return secret,ln
        }
    }
    return "", nil
}     

func runUdpServer(secret string, to *net.UDPConn){
    defer to.Close()
    buf := make([]byte,256)
    n,_,err := to.ReadFrom(buf)
    if err != nil {
        log.Println(err)
    }
    log.Printf("runUdpServer expected secret: %v\n", secret)
    if strings.TrimSpace(string(buf[:n])) != secret{
        return
    }

    store := make(map[string]string, 1)
    for {
        n,addr,err := to.ReadFrom(buf)
        if err != nil {
            log.Fatal(err)
        }
        value := strings.Fields(string(buf[:n]))
        if len(value) == 2 && value[0] == "get"{
            to.WriteTo([]byte(store[value[1]]+"\n"),addr)  
        }
        if len(value) == 1 && value[0] == "exit"{
            to.WriteTo([]byte("la di da, oh sorry, did you say something\n"),addr)
        }
        if len(value) == 3 && value[0] == "set"{
            if value[1] == "flag" && !CAN_SET_FLAG {
                to.WriteTo([]byte("not done\n"),addr) 
            } else if len(store) > 10 {
                to.WriteTo([]byte("I'm full\n"),addr)
            } else {
                store[value[1]]=value[2]
                to.WriteTo([]byte("done\n"),addr)   
                if value[1] == "flag" {
                    CAN_SET_FLAG = false
                }
            }
        }
        if len(value) == 1 && value[0] == "help"{
            to.WriteTo([]byte("get\nexit\nset\nhelp\n"),addr)   
        }
        if len(value) == 1 && value[0] == "list"{
            keys := ""
            for k := range store {
                keys += k+"\n"
            }
            to.WriteTo([]byte(keys),addr)   
        }
    }
}
