//construct 3 servo objects
int fan_pin = 5;
int sound_pin = 8;



int fan_speed =100;
int sound_tone =0;

// constructing the string object that will contain the data received from a PC
String data;

void setup() {
  //attaching digital pins to servo objects
  pinMode(fan_pin, OUTPUT);
  pinMode(sound_pin, OUTPUT);
  //setting serial baudrate to 115200
  Serial.begin(115200); 
}

//this function gets the servo data from the serial input
//Also the Y input will be converted to 1 positive and 1 negative value to acomplish one servo going up and the other going down.
void get_servo_info(){
  if(Serial.available()){
    data = Serial.readStringUntil('\n');
    if (data.startsWith("S")){
       sound_tone = data.substring(1).toInt();
    }
    else if (data.startsWith("F")){
       fan_speed = data.substring(1).toInt();
    }
  }
}

// this function sets the new position to the servo's
void update_servo_position(){
  analogWrite(fan_pin, fan_speed);
}

void update_sound(int sound_tone){
    tone(sound_pin, sound_tone*25, 500 );
    delay(10);
}

void loop() {
  get_servo_info();
  update_servo_position();
  update_sound(sound_tone);
}
