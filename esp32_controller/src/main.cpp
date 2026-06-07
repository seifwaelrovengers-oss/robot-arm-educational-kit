#include <WiFi.h>
#include <AccelStepper.h>
#include <ESP32Servo.h>

void updateServos();
// WiFi Access Point
const char* ssid = "RobotArm";
const char* password = "12345678";

WiFiServer server(80);

// Stepper pins
#define STEP1 18
#define DIR1 19
#define STEP2 21
#define DIR2 22

// Servo pins
#define SERVO1_PIN 13
#define SERVO2_PIN 14
#define SERVO3_PIN 27
#define SERVO4_PIN 25
#define SERVO5_PIN 26

// Stepper objects
AccelStepper stepper1(
  AccelStepper::DRIVER,
  STEP1,
  DIR1
);

AccelStepper stepper2(
  AccelStepper::DRIVER,
  STEP2,
  DIR2
);

// Servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// Steps per degree
float STEPS_PER_DEGREE_1 = 20.0;
float STEPS_PER_DEGREE_2 = 20.0;

// Stepper targets
long target1 = 0;
long target2 = 0;

// Servo targets
float servo1_target = 90;
float servo2_target = 90;
float servo3_target = 90;
float servo4_target = 90;
float servo5_target = 90;

// Servo current positions
float servo1_current = 90;
float servo2_current = 90;
float servo3_current = 90;
float servo4_current = 90;
float servo5_current = 90;

// Servo smooth speed
const int SERVO_STEP = 2;

void setup() {

  Serial.begin(115200);

  // WiFi AP
  WiFi.mode(WIFI_AP);

  WiFi.softAP(
    ssid,
    password
  );

  // Reduce WiFi latency
  WiFi.setSleep(false);

  IPAddress IP =
    WiFi.softAPIP();

  Serial.print("ESP32 IP: ");
  Serial.println(IP);

  // Start server
  server.begin();

  // Stepper setup
  stepper1.setMaxSpeed(2500);
  stepper1.setAcceleration(1500);

  stepper2.setMaxSpeed(2500);
  stepper2.setAcceleration(1500);

  // Attach servos
  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  servo3.attach(SERVO3_PIN);
  servo4.attach(SERVO4_PIN);
  servo5.attach(SERVO5_PIN);

  // Initial positions
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
  servo5.write(90);

  Serial.println("Robot Controller Started");
}

void loop() {

  // Smooth stepper motion
  stepper1.run();
  stepper2.run();

  // Smooth servo motion
  updateServos();

  // Wait for client
  WiFiClient client =
    server.available();

  if (client) {

    client.setTimeout(5);

    // Receive data
    String data =
      client.readStringUntil('\n');

    Serial.println(data);

    float angles[7];

    int index = 0;

    char buffer[100];

    // Convert String to char array
    data.toCharArray(
      buffer,
      100
    );

    // Split data
    char *token =
      strtok(buffer, ",");

    while (
      token != NULL &&
      index < 7
    ) {

      angles[index] =
        atof(token);

      token =
        strtok(NULL, ",");

      index++;
    }

    // Servo limits only, steppers can rotate freely
    // Base rotation
    angles[0] =
      constrain(
        angles[0],
        -135,
        135
      );

    // Shoulder
    angles[1] =
      constrain(
        angles[1],
        0,
        180
      );

    // Elbow
    angles[2] =
      constrain(
        angles[2],
        -80,
        90
      );

    // Wrist
    angles[3] =
      constrain(
        angles[3],
        -90,
        90
      );

    // Roll stepper
    angles[4] =
      constrain(
        angles[4],
        -180,
        180
      );

    // Yaw
    angles[5] =
      constrain(
        angles[5],
        0,
        180
      );

    // Gripper
    angles[6] =
      constrain(
        angles[6],
        0,
        180
      );

  // Set stepper targets
    target1 =
      angles[0] *
      STEPS_PER_DEGREE_1;

    target2 =
      angles[4] *
      STEPS_PER_DEGREE_2;

    stepper1.moveTo(target1);
    stepper2.moveTo(target2);
    
    // SERVOS
    servo1_target = angles[1]; // shoulder
    servo2_target = angles[2]; // elbow
    servo3_target = angles[3]; // wrist
    servo4_target = angles[5]; // yaw
    servo5_target = angles[6]; // gripper

    client.stop();
  }
}

void updateServos() {

  // Servo 1
  if (servo1_current < servo1_target)
    servo1_current += SERVO_STEP;

  else if (
    servo1_current >
    servo1_target
  )
    servo1_current -= SERVO_STEP;

  if (
    abs(
      servo1_current -
      servo1_target
    ) < SERVO_STEP
  )
    servo1_current =
      servo1_target;

  // Servo 2
  if (servo2_current < servo2_target)
    servo2_current += SERVO_STEP;

  else if (
    servo2_current >
    servo2_target
  )
    servo2_current -= SERVO_STEP;

  if (
    abs(
      servo2_current -
      servo2_target
    ) < SERVO_STEP
  )
    servo2_current =
      servo2_target;

  // Servo 3
  if (servo3_current < servo3_target)
    servo3_current += SERVO_STEP;

  else if (
    servo3_current >
    servo3_target
  )
    servo3_current -= SERVO_STEP;

  if (
    abs(
      servo3_current -
      servo3_target
    ) < SERVO_STEP
  )
    servo3_current =
      servo3_target;

  // Servo 4
  if (servo4_current < servo4_target)
    servo4_current += SERVO_STEP;

  else if (
    servo4_current >
    servo4_target
  )
    servo4_current -= SERVO_STEP;

  if (
    abs(
      servo4_current -
      servo4_target
    ) < SERVO_STEP
  )
    servo4_current =
      servo4_target;
  // Servo 5
  if (servo5_current < servo5_target)
    servo5_current += SERVO_STEP;

  else if (
    servo5_current >
    servo5_target
  )
    servo5_current -= SERVO_STEP;
    
  if (
      abs(
        servo5_current -
        servo5_target
      ) < SERVO_STEP
    )
      servo5_current =
        servo5_target;
  
  // Write servos
  servo1.write(servo1_current);
  servo2.write(servo2_current);
  servo3.write(servo3_current);
  servo4.write(servo4_current);
  servo5.write(servo5_current);
}