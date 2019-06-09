#include <LiquidCrystal.h>
LiquidCrystal lcd(7, 8, 9, 10, 11 , 12);


int solenoidPin = 2;
const int ledPin = 13;
const int triggerPin = 5;
const int inputPin = 3;
int toggle = 0;
const int debounceDelay = 20;
float analogArray[120];
float timeArray[120];
//char line1[21];
//char line2[21]; 
char pDisp[5];
char pSet[5];
int clearCounter = 0;
int readIndex = 0;

//values for pressure sensor

int sensorPinPlus = A1;
int pSetPin = A3;
float pSetVal = 0;
int sensorValuePlus = 0;
float flukeReader = 0;
int setPinValue=0;
float vMinus = 0.;
float vPlus = 0.;

float pressureValue = 0;
float timeFloat = 0.;
long t = 0; //time counter
long endTime = 3000000; //time to log pressure
int initialTime = 0; //time of the start of the logging
float v = 0; //diff between vPlus and vMinus
int index = 0; //index for loops
const int maxChars = 20; //limit for serial communication
char strValue[maxChars + 1];
int steps = 0;
float qTime = 0;
int setP =5;
int serialTrigger=0;

// values for serial reading
bool readSet = false;
bool readV = false;
//setup stepper motor
//#include <Wire.h>
//#include <Adafruit_MotorShield.h>
//#include "utility/Adafruit_MS_PWMServoDriver.h"

//Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
//Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);

boolean debounce(int pin)
{
  boolean state;
  boolean previousState;

  previousState = digitalRead(pin);
  for (int counter = 0; counter < debounceDelay; counter++)
  {
    delay(1);
    state = digitalRead(pin);
    if ( state != previousState)
    {
      counter = 0;
      previousState = state;
    }
  }
  return state;
}


//define serial function

void serialEvent()
{
    char ch = Serial.read();
    if (ch == 't')
       {
        serialTrigger=1; Serial.println("triggering");
         }
    else if (ch == 's')
      {
        //strValue[readIndex] = 0;
        readIndex = 0;
        readSet = true;
        //Serial.println("t1");
      }

    else if (ch == 'v')
      {
        //strValue[readIndex] = 0;
        //strValue[0] = 0;
        readIndex = 0;
        readV = true;
                //Serial.print("t2 "); Serial.println(maxChars);
//
      }
     else if (ch != 10 && readIndex < maxChars && readSet) //carriage return
          {
            strValue[readIndex++] = ch;
         //                  Serial.println("t3");

            //Serial.print(index);Serial.print(ch); Serial.print(index);Serial.print(atoi(strValue)); 
          }
     else if (ch != '\n' && readIndex < maxChars && readV) //carriage return
          {
            strValue[readIndex++] = ch;
            //Serial.write("index ");Serial.print(readIndex);Serial.print(' ');Serial.write("current value ");Serial.println(ch); 
          }
     else if (ch=0)
     {
      Serial.println("zero");
     }
     
     else
          {
            strValue[readIndex]=0;
            if (readSet)
            {
              setP = atoi(strValue);
        //      Serial.write(ch);Serial.write("set pressure "); Serial.println(setP);
             readIndex=0;
            //strValue[0]=0;
            readSet=false;
            readV = false;
            }
            else if (readV)
            {
             flukeReader = atof(strValue);

             //Serial.print(ch);Serial.print(' ');Serial.print(readV);Serial.print(" aV: "); Serial.println(flukeReader,5);
            readIndex=0;
            //strValue[0]=0;
            readSet=false;
            readV = false;
            }
         // Serial.println("elsed");
          }
}



void setup()
{
  pinMode(solenoidPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(inputPin, INPUT_PULLUP);
  pinMode(triggerPin, OUTPUT);

  //pressure sensor
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("--------------------");
  Serial.println("TWO CHANNEL DC VOLTMETER");
  Serial.print("Maximum Voltage: ");
  Serial.println("V");
  Serial.println("--------------------");
  Serial.println("");

//  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

//  myMotor->setSpeed(10);  // 10 rpm

  delay(2000);
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.write("Valve:C");
  lcd.setCursor(8,0);
  lcd.write("PS: ");
  lcd.setCursor(0,1);
  lcd.write("PR: ");
  clearCounter=0;



}

void loop()
{
  if (clearCounter == 500)
  {
    lcd.begin(16,2);
    lcd.clear();

    lcd.setCursor(0,0);
    lcd.write("Valve:");
    lcd.setCursor(8,0);
    lcd.write("PS: ");
    lcd.setCursor(0,1);
    lcd.write("PR: ");
    clearCounter=0;
  }
  clearCounter=clearCounter+1;
  //Serial.println(clearCounter);
  //sensorValuePlus= analogRead(sensorPinPlus);
  //setPinValue = analogRead(pSetPin);
  setPinValue = float(setP);
 // Serial.println(setP);
  pSetVal = ((setPinValue) / 1023.) * 5 / .025 * 10.; //units of inches of h20
  pressureValue = ((flukeReader )) / .025 * 10.; //units of inches of h20
  lcd.setCursor(3,1);
  dtostrf(pressureValue,5,2,pDisp);
  lcd.print(pDisp);
  dtostrf(pSetVal,5,2,pSet);
  lcd.setCursor(11,0);
  lcd.print(pSet);
  //Serial.println(toggle);

  //lcd.print(millis()/1000);
  //delay(200);
  //Serial.print(pressureValue);
  //Serial.print('\n');
  
  if (Serial.available())
  {
    serialEvent();
  }
  if (!debounce(inputPin) || serialTrigger == 1)
  {
    serialTrigger = 0; //reset trigger so it doesn't keep firing
    toggle = (toggle + 1) % 2; // switch between 1 and zero every time it is pressed
    Serial.print("TOGGLED "); Serial.println(toggle);

    if (toggle == 1)
    {
      //time quench initiated
      qTime = micros();
      //first, store initial pressure
      for (int counter = 0; counter < 6; counter++)
      {
 
        analogArray[counter] = analogRead(sensorPinPlus)/1000./1023.*5/.025*10;
        timeArray[counter] = micros()-qTime;

      }
      digitalWrite(triggerPin,HIGH);
      digitalWrite(solenoidPin, HIGH); //trigger the trans to trigger the quench
      for (int counter = 6; counter <120; counter++)
      {
        analogArray[counter] = analogRead(sensorPinPlus)/1000./1023.*5/.025*10;
        timeArray[counter] = micros()-qTime;

      }
      
      digitalWrite(ledPin, HIGH);
      lcd.setCursor(6,0);
      lcd.print("O");
      Serial.println("OPEN");
      Serial.println("Begin Read");
      //now print out the results of the pressure logging for anyone to decode
      for (int counter = 0; counter<120; counter++)
      {
        String row = String(timeArray[counter],8)+" , "+String(analogArray[counter],8);
        Serial.println(row);
      }
      Serial.println("End Read");
      //de-arm trigger
      digitalWrite(triggerPin,LOW);
    }

    else if (toggle == 0)
    {
      digitalWrite(solenoidPin, LOW);
      digitalWrite(ledPin, LOW);
      lcd.setCursor(6,0);
      lcd.print("C");
    }
    else
    {
      Serial.print("ERROR");
    }


    // now read the pressure value after 2 seconds, and log for a second
    delay(2000);
    Serial.println("begin logging");





    //end switching part of the program

  }


}
