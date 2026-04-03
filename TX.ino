const int ledSwitch = 4; // D4
const int fanSwitch = 2; // Switch for fan
const int buzzerSwitch = 3; // Switch for buzzer

bool fanState = false;
bool buzzerState = false;

void setup() {
  pinMode(ledSwitch, OUTPUT);
  pinMode(fanSwitch, INPUT_PULLUP);
  pinMode(buzzerSwitch, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  static bool lastFanSwitch = HIGH;
  static bool lastBuzzerSwitch = HIGH;

  bool currentFan = digitalRead(fanSwitch);
  bool currentBuzzer = digitalRead(buzzerSwitch);

  // Fan toggle
  if (currentFan == LOW && lastFanSwitch == HIGH) { // switch just pressed
    fanState = !fanState;   // toggle state
    sendCommand(fanState ? 1 : 0, "Fan");
  }
  lastFanSwitch = currentFan;

  // Buzzer toggle
  if (currentBuzzer == LOW && lastBuzzerSwitch == HIGH) {
    buzzerState = !buzzerState;
    sendCommand(buzzerState ? 2 : 0, "Buzzer");
  }
  lastBuzzerSwitch = currentBuzzer;

  delay(50); // debounce
}

void sendCommand(int cmd, String name){
  if (cmd == 0) return; // no need to send off command if you want simple toggle
  if (cmd == 1){
    digitalWrite(ledSwitch, HIGH);
    delay(200);
    digitalWrite(ledSwitch, LOW);
    Serial.println(name + " ON");
  } else if (cmd == 2){
    for(int i=0;i<2;i++){ // double pulse for buzzer
      digitalWrite(ledSwitch, HIGH);
      delay(200);
      digitalWrite(ledSwitch, LOW);
      delay(100);
    }
    Serial.println(name + " ON");
  }
}