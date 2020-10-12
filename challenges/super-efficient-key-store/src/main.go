package main

import (
    "net"
    "log"
    "strings"
    "io/ioutil"//"math/rand"
    "strconv"
    "time"
)

var CAN_SET_FLAG = false//var CAN_SET_FLAG = true
var START_PORT = 12000
var END_PORT = 13000

// func main() {
//     listener, err :=  net.Listen("tcp", ":5000")
//     if err != nil {
//         log.Fatal(err)
//     }

//     for {
//         conn, err := listener.Accept()
//         if err != nil {
//             log.Println(err)
//         }
//         go handleConnection(conn)
//     }
// }

// func handleConnection(conn net.Conn) {
//     defer conn.Close()

//     secret, ln := startUdpServer()
//     if secret == "" || ln == nil {
//         conn.Write([]byte("No room\n"))
//         return
//     }
//     parts := strings.Split(ln.LocalAddr().String(),":")
//     conn.Write([]byte("use this secret: "+secret+"\nuse this UDP Port: "+parts[len(parts)-1]+"\n"))  
//     go runUdpServer(secret, ln)
// }

// var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

// func randStringRunes(n int) string {
//     b := make([]rune, n)
//     for i := range b {
//         b[i] = letterRunes[rand.Intn(len(letterRunes))]
//     }
//     return string(b)
// }

// func startUdpServer() (string,*net.UDPConn) {
//     for port := START_PORT; port <= END_PORT; port++ {
//         listenAddr, err := net.ResolveUDPAddr("udp", ":"+strconv.Itoa(port))
//         for err != nil {
//             log.Fatal(err)
//         }
//         ln, err := net.ListenUDP("udp", listenAddr) 
//         if err == nil {
//             secret := randStringRunes(20)
//             log.Printf("startUdpServer port: %v secret: %v\n", port, secret)
//             return secret,ln
//         }
//     }
//     return "", nil
// }     

// func runUdpServer(secret string, to *net.UDPConn){
//     defer to.Close()
//     buf := make([]byte,256)
//     n,_,err := to.ReadFrom(buf)
//     if err != nil {
//         log.Println(err)
//     }
//     log.Printf("runUdpServer expected secret: %v\n", secret)
//     if strings.TrimSpace(string(buf[:n])) != secret{
//         return
//     }

//    store := make(map[string]string, 1)
// start delete for /dist
func main() {
    flag_port := "12021"
    dat, err := ioutil.ReadFile("flag.txt")
    if err != nil{
        panic(err)
    }
    flag := string(dat)

    for port := START_PORT; port <= END_PORT; port++ {
        if strconv.Itoa(port) == flag_port{
            log.Println("making "+flag_port+" contain the flag")
            go runUdpServer(port, flag)
        } else {
            go runUdpServer(port, "")
        }
    }

    localAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil{
        panic(err)
    }

    remoteAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:"+flag_port)
    if err != nil{
        panic(err)
    }

    uconn, err := net.DialUDP("udp", localAddr, remoteAddr)
    if err != nil{
        panic(err)
    }
    defer uconn.Close()


    uconn.Write([]byte("get flag\n"))
    buf := make([]byte,256)
    n,_,err := uconn.ReadFrom(buf)
    for string(buf[:n]) != flag+"\n"{
        log.Println(string(buf))
        log.Println("The Flag wasn't set yet.")
        time.Sleep(time.Second)
        uconn.Write([]byte("get flag\n"))
        n,_,err = uconn.ReadFrom(buf)
    }
    log.Println("Finished creating the flag seat")
    pause := make(chan string)
    for {
        <- pause
    }
}

func runUdpServer(port int, flag string){
    listenAddr, err := net.ResolveUDPAddr("udp", ":"+strconv.Itoa(port))
    if err != nil {
        log.Fatal(err)
    }
    to, err := net.ListenUDP("udp", listenAddr) 
    if err != nil {
        log.Fatal(err)
    }
    defer to.Close()
    buf := make([]byte,256)

    store := make(map[string]string, 1)
    if flag != "" {
        store["flag"] = flag
    }
// end delete for /dist

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
