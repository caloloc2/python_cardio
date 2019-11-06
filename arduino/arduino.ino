int encendido = 1;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    int data = Serial.read();
    Serial.println(data);
    if (data==97){
      digitalWrite(13, encendido);
      encendido = abs(encendido -1);
    }
  }
}
