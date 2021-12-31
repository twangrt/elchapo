void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // open the serial port at 9600 bps:  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("1.52 1.04 1.07\n");         // prints a tab
  delay(50);
}
