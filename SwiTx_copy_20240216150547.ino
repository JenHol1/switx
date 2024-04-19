/*
  SwiTx Arduino Code
  Version 2



  */
int inByte ='0';
const int MuteA = 14;
const int MuteB = 15;
const int PlexA1 = 16;
const int PlexB1 = 18;

void setup() {
  
  pinMode(MuteA, OUTPUT);     // 4066 Quad Bilateral Switch
  digitalWrite(MuteA, HIGH);   // Switch Signal State

  pinMode(MuteB, OUTPUT);     // 4066 Quad Bilateral Switch
  digitalWrite(MuteB, HIGH);   // Switch Signal State

  pinMode(PlexA1, OUTPUT);     // 4067 Analog Multiplexer
  digitalWrite(PlexA1, LOW);   // Plexer Signal State 0
  
  pinMode(PlexB1, OUTPUT);     // 4067 Analog Multiplexer
  digitalWrite(PlexB1, LOW);   // Plexer Signal State 0


  Serial.begin(9600);      // Serial Port
  Serial.println("<Serial Test>");     //Serial Port Test Text
  
}

void loop() {
  
  if (Serial.available() > 0) {
    inByte = (Serial.read()); // Read byte from serial port

    // Toggle the Device state 
    if (inByte == '1') { //Switches to B
      digitalWrite(MuteA, LOW);  // Turn the MuteA ON
      digitalWrite(MuteB, LOW);  // Turn the MuteB ON

      delay(100);                // Delay 

      digitalWrite(PlexA1, HIGH);  // Turn the PlexA1 ON 1
      digitalWrite(PlexB1, HIGH);  // Turn the PlexB1 ON 1 (Switched to Channel B)

      delay(100);                // Delay

      digitalWrite(MuteA, HIGH);  // Turn the MuteA OFF
      digitalWrite(MuteB, HIGH);  // Turn the MuteB OFF
      
      Serial.println("Switched to B");

    } else if (inByte == '0') { //Switches to A
      digitalWrite(MuteA, LOW);  // Turn the MuteA ON
      digitalWrite(MuteB, LOW);  // Turn the MuteB ON

      delay(100);                // Delay

      digitalWrite(PlexA1, LOW);  // Turn the PlexA1 ON 0
      digitalWrite(PlexB1, LOW);  // Turn the PlexB1 ON 0 (Switched to Channel A)

      delay(100);                // Delay

      digitalWrite(MuteA, HIGH);  // Turn the MuteA OFF
      digitalWrite(MuteB, HIGH);  // Turn the MuteB OFF

      Serial.println("Switched to A");
      
    } else {
      Serial.println("Invalid character received. Send '1' to turn Switch Output, '0' to turn Keep Current Output.");
    }
  }
}



