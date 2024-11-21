#define RED_LED_LANE1 2       // Red LED for Lane 1
#define GREEN_LED_LANE1 3     // Green LED for Lane 1
#define RED_LED_LANE2 4       // Red LED for Lane 2
#define GREEN_LED_LANE2 5     // Green LED for Lane 2

#define IR_SENSOR_LANE1 6     // IR Sensor for Lane 1
#define IR_SENSOR_LANE2 7     // IR Sensor for Lane 2

#define GREEN_TIME 5000       // Green light duration in ms (5 seconds)

void setup() {
  pinMode(RED_LED_LANE1, OUTPUT);
  pinMode(GREEN_LED_LANE1, OUTPUT);
  pinMode(RED_LED_LANE2, OUTPUT);
  pinMode(GREEN_LED_LANE2, OUTPUT);

  pinMode(IR_SENSOR_LANE1, INPUT);
  pinMode(IR_SENSOR_LANE2, INPUT);

  // Initially, all signals are red
  digitalWrite(RED_LED_LANE1, HIGH);
  digitalWrite(GREEN_LED_LANE1, LOW);
  digitalWrite(RED_LED_LANE2, HIGH);
  digitalWrite(GREEN_LED_LANE2, LOW);
}

void loop() {
  static bool lane1CycleActive = false;
  static bool lane2CycleActive = false;

  bool vehicleInLane1 = digitalRead(IR_SENSOR_LANE1) == LOW;  // Vehicle detected in Lane 1 if IR sensor reads LOW
  bool vehicleInLane2 = digitalRead(IR_SENSOR_LANE2) == LOW;  // Vehicle detected in Lane 2 if IR sensor reads LOW

  // Trigger traffic light cycle for Lane 1 if a vehicle is detected and no cycle is active
  if (vehicleInLane1 && !lane1CycleActive) {
    lane1CycleActive = true;
    setTrafficLightLane1();
    lane1CycleActive = false; // Reset cycle status after completion
  }

  // Trigger traffic light cycle for Lane 2 if a vehicle is detected and no cycle is active
  if (vehicleInLane2 && !lane2CycleActive) {
    lane2CycleActive = true;
    setTrafficLightLane2();
    lane2CycleActive = false; // Reset cycle status after completion
  }
}

void setTrafficLightLane1() {
  // Set Lane 1 to Green
  digitalWrite(RED_LED_LANE1, LOW);
  digitalWrite(GREEN_LED_LANE1, HIGH);
  delay(GREEN_TIME);          // Keep Lane 1 Green for specified time

  // Switch Lane 1 to Red
  digitalWrite(GREEN_LED_LANE1, LOW);
  digitalWrite(RED_LED_LANE1, HIGH);
}

void setTrafficLightLane2() {
  // Set Lane 2 to Green
  digitalWrite(RED_LED_LANE2, LOW);
  digitalWrite(GREEN_LED_LANE2, HIGH);
  delay(GREEN_TIME);          // Keep Lane 2 Green for specified time

  // Switch Lane 2 to Red
  digitalWrite(GREEN_LED_LANE2, LOW);
  digitalWrite(RED_LED_LANE2, HIGH);
}
