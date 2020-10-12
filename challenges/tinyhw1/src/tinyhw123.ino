/*
 OpenCTF 2019 -tinyhw123
 Author: meta 

 ATTiny85 on internal 8 MHz clock
 Burn Bootloader whenever you change clock speed
 */
 
#include <SoftwareSerial.h> 

#define RX 3
#define TX 4
#define LED 2
#define GAP 200
#define GAP3 600
#define BUFLEN 21
#define BAUD 19200
#define CMPDELTA 80
#define INDELAY 30

SoftwareSerial Serial(RX, TX); 
char flag[] = "DPCTPYFYPRZTCI^CDPCE";
char buf[BUFLEN+1];
int level = 0;


char conv(int c){
  // obfuscation so that flag is not in firmware strings
  return (char)(c^49);
}


void setup() {
  pinMode(RX, INPUT);
  pinMode(TX, OUTPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(BAUD);
  // decode flag
  for (int i=0; i<sizeof(flag)-1; i++){
    flag[i] = conv(flag[i]);
  }
}


void dit(){
  digitalWrite(LED, HIGH);                                               
  delay(GAP);                                                
  digitalWrite(LED, LOW);                                            
  delay(GAP);  
}


void dah(){
  digitalWrite(LED, HIGH);
  delay(GAP3);
  digitalWrite(LED, LOW);                                                              
  delay(GAP);  
}


void morsecode(){
  // codify message to save space for dynamic memory
  // local and global vars are limited to 512 bytes on ATTiny85
  // -. ...-- ...- ...-- .-. ..--.- ... . -. -.. ..--.- .- ..--.- -... ----- -.-- ..--.- --...
  // --- ..--.- -.. ----- ..--.- .- ..--.- .-- ----- -- .- -. ..... ..--.- .--- --- -...
  dah(); dit(); delay(GAP3);
  dit(); dit(); dit(); dah(); dah(); delay(GAP3);
  dit(); dit(); dit(); dah(); delay(GAP3);
  dit(); dit(); dit(); dah(); dah(); delay(GAP3);
  dit(); dah(); dit(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dit(); dit(); dit(); delay(GAP3);
  dit(); delay(GAP3);
  dah(); dit(); delay(GAP3);
  dah(); dit(); dit(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dit(); dah(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dah(); dit(); dit(); dit(); delay(GAP3);
  dah(); dah(); dah(); dah(); dah(); delay(GAP3);
  dah(); dit(); dah(); dah(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dah(); dah(); dit(); dit(); dit(); delay(GAP3);
  dah(); dah(); dah(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dah(); dit(); dit(); delay(GAP3);
  dah(); dah(); dah(); dah(); dah(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dit(); dah(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dit(); dah(); dah(); delay(GAP3);
  dah(); dah(); dah(); dah(); dah(); delay(GAP3);
  dah(); dah(); delay(GAP3);
  dit(); dah(); delay(GAP3);
  dah(); dit(); delay(GAP3);
  dit(); dit(); dit(); dit(); dit(); delay(GAP3);
  dit(); dit(); dah(); dah(); dit(); dah(); delay(GAP3);
  dit(); dah(); dah(); dah(); delay(GAP3);
  dah(); dah(); dah(); delay(GAP3);
  dah(); dit(); dit(); dit(); delay(GAP3);
  delay(2000);
}
                                                                     

bool checkflag(){
  int j = 0;
  for (j=0; j<BUFLEN-1; j++){
    if (buf[j] != flag[j]){
      break;
    }
    else {
      delay(CMPDELTA);
    }
  }
  if (j==BUFLEN-1){
    return true;
  }
  return false;
}


void level2(){
  int i = 0;
  int c = -1;
  memset(buf, '\0', sizeof(buf));
  Serial.print("flag: ");
    
  // readline
  while (i < BUFLEN) {
    if (Serial.available() > 0) {
      c = Serial.read();
      if (c != -1) {
        buf[i] = (char)c;
        if ((buf[i] == '\n') || (buf[i] == '\r')) {
          break;
        }
        // echo
        Serial.print(buf[i]);
        i++;
      }
    }
    // this makes the serial conn more reliable; fewer timeouts
    // 30ms delay works well on 19200 baud on 8 Mhz
    delay(INDELAY);
  }
  
  if (checkflag()) {
    level = 3;
    Serial.println("  <---- Woot! That's the flag :)");
  } else {
    Serial.println("");
  }
}


void flush_stream(){
  int c;
  Serial.flush();
  for (int i=0; i<500; i++) {
    if (Serial.available() > 0) {
      c = Serial.read();
    }
  }
}


void loop() {

  if (level == 1) {
    Serial.println("This is your wakeup call from the Nintendo generation!");
    Serial.println("Level 1 flag: tHe_bEau7y_0f_7h3_BAUD");
    Serial.println("Welcome to level 2!");
    level = 2;
  }
  else if (level == 2) {
    level2();
  }

  else if (level == 3) {
    Serial.println("Well done angelheaded hipster; the stary dynamo awaits.");
    Serial.println("Welcome to level 3!");
    while (true) {
      morsecode();
      delay(4000);
    }
  }
  else {
    Serial.println("OpenCTF 2019");
    delay(1000);
    if (Serial.available()) {
      level = 1;
      flush_stream();
    }
  }
}
