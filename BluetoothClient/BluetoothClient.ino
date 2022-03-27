#include <dht_nonblocking.h>
#define dhtSensorType DHT_TYPE_11
#define redLED 4
#define blueLED 5
#define buzzer 6

int incomingByte;
const int baudRate=9600;
const int dhtSensorPin=2;
float Na;
float K;
float Glucose;
float CRP;
float ILBeta;
float temperature;
float humidity;
unsigned long interval=5000;

DHT_nonblocking dht_sensor(dhtSensorPin, dhtSensorType);

static bool checkNa(float *Na)
{
  /*
   * Check whether the Na concentration reading is ready for uploading
   * 
   * By defaut, the Na concentration comes from the ion-selective electrode
   * as a float with default unit: mM
   * 
   * For proof-of-principle purpose, this function for now would generate a 
   * random float value within: 10~160 mM, which is estimated based on the
   * reference papers
   */
   static unsigned long NaTimeStamp=millis();
   if (millis()-NaTimeStamp>interval)
   {
    NaTimeStamp=millis();
    *Na=(float)random(1000, 16001)/100;
    return true;
   }
   return false;
}

static bool checkK(float *K)
{
  /*
   * Check whether the K concentration reading is ready for uploading
   * 
   * By default, the K concentration comes from the ion-selective electrode
   * as a float with default unit: mM
   * 
   * For proof-of-principle purpose, this function for now would return a 
   * random float value within: 1~32 mM, which is estimated based on the
   * reference papers
   */
   static unsigned long KTimeStamp=millis();
   if (millis()-KTimeStamp>interval)
   {
    KTimeStamp=millis();
    *K=(float)random(100, 3201)/100;
    return true;
   }
   return false;
}

static bool checkGlucose(float *Glucose)
{
  /*
   * Check whether the Glucose concentration is ready for uploading
   * 
   * By default, the Glucose concentration from the glucose sensor
   * as a float with default unit: μM
   * 
   * For proof-of-principle purpose, this function for now would return a 
   * random float value within: 0~200 μM, which is estimated based on the
   * reference papers
   */
   static unsigned long GlucoseTimeStamp=millis();
   if (millis()-GlucoseTimeStamp>interval)
   {
    GlucoseTimeStamp=millis();
    *Glucose=(float)random(0, 20001)/100;
    return true;
   }
   return false;
}

static bool checkCRP(float *CRP)
{
  /*
   * Check whether the CRP concentration is ready for uploading
   * 
   * By default, the CRP concentration from the IBD sensor
   * as a float with default unit: ng/mL
   * 
   * For proof-of-principle purpose, this function for now would return a 
   * random float value within: 0~10 ng/mL, which is estimated based on the
   * reference papers
   */
   static unsigned long CRPTimeStamp=millis();
   if (millis()-CRPTimeStamp>interval)
   {
    CRPTimeStamp=millis();
    *CRP=(float)random(0, 1001)/100;
    return true;
   }
   return false;
}

static bool checkILBeta(float *ILBeta)
{
  /*
   * Return the IL-Beta concentration from the IBD sensor as a float
   * with default unit: pg/mL
   * 
   * For proof-of-principle purpose, this function for now would return a 
   * random float value within: 0.2~200 pg/mL, which is estimated based on the
   * reference papers
   */
   static unsigned long ILBetaTimeStamp=millis();
   if (millis()-ILBetaTimeStamp>interval)
   {
    ILBetaTimeStamp=millis();
    *ILBeta=(float)random(20, 20001)/100;
    return true;
   }
   return false;
}

static bool checkTemperature(float *temperature, float *humidity)
{
  /*
   * Check whether the temperature reading is ready for uploading
   */
   static unsigned long temperatureTimeStamp=millis();
   if (millis()-temperatureTimeStamp>interval)
   {
    if (dht_sensor.measure(temperature, humidity)==true)
    {
      temperatureTimeStamp=millis();
      return true;
    }
   }
   return false;
}

void uploadNa(float *Na)
{
  /*
   * Upload the Na concentration only if the sensor is ready
   */
   if (checkNa(Na)==true)
   {Serial.println("Na,"+String(*Na));}
}

void uploadK(float *K)
{
  /*
   * Upload the K concentration only if the sensor is ready
   */
   if (checkK(K)==true)
   {Serial.println("K,"+String(*K));}
}

void uploadGlucose(float *Glucose)
{
  /*
   * Upload the Glucose concentration only if the sensor is ready
   */
   if (checkGlucose(Glucose)==true)
   {Serial.println("Glucose,"+String(*Glucose));}
}

void uploadCRP(float *CRP)
{
  /*
   * Upload the CRP concentration only if the sensor is ready
   */
   if (checkCRP(CRP)==true)
   {Serial.println("CRP,"+String(*CRP));}
}

void uploadILBeta(float *ILBeta)
{
  /*
   * Upload the ILBeta concentration only if the sensor is ready
   */
   if (checkILBeta(ILBeta)==true)
   {Serial.println("ILBeta,"+String(*ILBeta));}
}

void uploadTemperature(float *temperature, float *humidity)
{
  /*
   * Upload the temperature reading only if the sensor is ready
   */
   if (checkTemperature(temperature, humidity)==true)
   {Serial.println("Temperature,"+String(*temperature));}
}

void alarm()
{
  /*
   * Fire alarm if received the command from the PC
   * 
   * The alarm simulates the ambulance alarm:
   * (1) Red/Blue LED will blink for 5s
   * (2) The buzzer will beep at different frequency for 5s
   * (3) The alarm automatically stops after 5s
   */
   digitalWrite(redLED, LOW);
   digitalWrite(blueLED, LOW);
   
   for (int i=0;i<5;i++)
   {
    tone(buzzer, 660, 500);
    digitalWrite(redLED, HIGH);
    digitalWrite(blueLED, LOW);
    delay(500);
    
    tone(buzzer, 494, 500);
    digitalWrite(redLED, LOW);
    digitalWrite(blueLED, HIGH);
    delay(500);
   }  

   digitalWrite(redLED, LOW);
   digitalWrite(blueLED, LOW);
}

void setup() {
  Serial.begin(baudRate);
  pinMode(redLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  digitalWrite(redLED, LOW);
  digitalWrite(blueLED, LOW);
}

void loop()
{
  /*
   * Within a full loop:
   * (1) Upload the Na concentration
   * (2) Upload the K concentration
   * (3) Upload the Glucose concentration
   * (4) Upload the CRP concentration
   * (5) Upload the ILBeta concentration
   * (6) Upload the Temperature reading
   * (7) Fire alarm if received command from PC
   */
  uploadNa(&Na);
  uploadK(&K);
  uploadGlucose(&Glucose);
  uploadCRP(&CRP);
  uploadILBeta(&ILBeta);
  uploadTemperature(&temperature, &humidity);
  if (Serial.available() > 0)
  {
    incomingByte = Serial.read();
    if (incomingByte == 'H') { alarm();}
  }
  delay(1000);
}
