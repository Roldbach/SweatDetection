int state;

String controlLED(String state)
{
  /*
   * Control the built-in led light according to the input
   * from Python script via bluetooth
   * 
   * This function is only used for testing
   */
  if (state=="0")
  {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED: OFF");
    return state;
  }
  else
  {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("LED: ON");
    delay(1000);
    return "0";
  }
}

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  // If showing light, connect successfully
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()>0)
  {
    state=Serial.read();
  }
  

}
