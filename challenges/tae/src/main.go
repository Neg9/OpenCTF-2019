package main

import (
  "fmt"
  "net"
  "os"
  "bufio"
  "math/rand"
  "strings"
  "encoding/hex"
  "io/ioutil"
)

const (
  CONN_HOST = "0.0.0.0"
  CONN_PORT = "5000"
  CONN_TYPE = "tcp"
)

var FLAG = "flag{1t_wuz_ma!d_up_:clap:}"

func main() {
  // Listen for incoming connections.
  l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
  if err != nil {
    fmt.Println("Error listening:", err.Error())
    os.Exit(1)
  }
  // Close the listener when the application closes.
  defer l.Close()
  fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
  for {
    // Listen for an incoming connection.
    conn, err := l.Accept()
    if err != nil {
      fmt.Println("Error accepting: ", err.Error())
      os.Exit(1)
    }
    // Handle connections in a new goroutine.
    go handleRequest(conn)
  }
}

// got tired of writing this so much
func write(message string, conn net.Conn){
  conn.Write([]byte(message+"\n"))
}


// starting vocab
func initialPhrases() (map[string][]string,[]string) {
  content, err := ioutil.ReadFile("/taetae.txt")
  if err != nil {
    panic(err)
  }

  parts := strings.Split(string(content), "\n")
  responses := map[string][]string{}
  phrases := make([]string, len(parts)*100)

  previous := ""
  for i,line := range parts{
    line = strings.TrimSpace(line)
    for j:=0;j<100;j++{
      phrases[i*100+j] = line
    }
    responses[previous]=phrases[i*100:(i+1)*100]
    previous = strings.ToLower(line)
  }
  responses[strings.ToLower(parts[len(parts)-1])] = responses[""]
  return responses, phrases
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
  //properly handling handles
  defer conn.Close()

  // load vocab for session

  // make the unique secret as a hex
  responses, phrases := initialPhrases()
  bytes := make([]byte, 20)
  rand.Read(bytes)
  key := hex.EncodeToString(bytes)

  // start the conversation, this isn't in the vocab because it contains the key
  write("If you can make me say "+key+" then I will tell you the flag.", conn)

  // however they start a converstaion is probably a fair response to hi
  lastsaid := ""
  for {

    // get what they said
    message, err := bufio.NewReader(conn).ReadString('\n')
    if err != nil {
      fmt.Println(err)
      return
    }

    // add it to potential responses
    message = strings.TrimSpace(message)
    responses[lastsaid] = append(responses[lastsaid], message)

    // prevent the key from accidentally being said as a random response
    // not realistic, but the limited vocabulary requires this to make the challenge work
    if !strings.Contains(message, key){
      phrases = append(phrases, message)
    }

    // pick a response if their message has known responses or pick a random response
    choices, known := responses[strings.ToLower(message)]
    response := ""
    if known {
      response = choices[rand.Intn(len(choices))]
    } else {
      response = phrases[rand.Intn(len(phrases))]
    }
    write(response, conn)

    // check for win condition
    if strings.Contains(response, key){
      write("Woops, you got me. ;)", conn)
      write(FLAG, conn)
    }

    // ensure that hi and HI are both responded to equally.
    lastsaid = strings.ToLower(response)
  }
}
