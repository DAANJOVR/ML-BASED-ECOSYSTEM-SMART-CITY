#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

// Definitions
#define DHTPIN 2               // DHT11 data pin
#define DHTTYPE DHT11          // DHT11 sensor type
#define MQ6_PIN A0             // MQ6 sensor analog pin
#define BUZZER_PIN 3           // Active buzzer pin
#define OLED_RESET -1          // OLED reset pin (not used here)
#define AIR_QUALITY_THRESHOLD 400  // Air quality threshold for alert

// Initialize DHT and OLED
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(OLED_RESET);

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW); // Ensure buzzer is off

    Serial.begin(9600);
    dht.begin();

    // Initialize the OLED display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Use 0x3C for OLED address
        Serial.println(F("SSD1306 allocation failed"));
        for (;;); // Freeze if OLED initialization fails
    }
    display.display();
    delay(2000); // Pause for 2 seconds
    display.clearDisplay();
}

void loop() {
    int airQuality = analogRead(MQ6_PIN);     // Read MQ6 sensor data
    float temperature = dht.readTemperature(); // Read temperature from DHT11
    float humidity = dht.readHumidity();       // Read humidity from DHT11

    // Check if DHT sensor readings are valid
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }

    // Display air quality, temperature, and humidity on OLED
    displayData(airQuality, temperature, humidity);

    // Trigger siren if air quality exceeds threshold
    if (airQuality > AIR_QUALITY_THRESHOLD) {
        triggerSiren();  // Trigger alarm if air quality is poor
    } else {
        digitalWrite(BUZZER_PIN, LOW); // Ensure buzzer is off
    }

    delay(2000); // Delay for 2 seconds before next reading
}

// Function to display air quality, temperature, and humidity on the OLED
void displayData(int airQuality, float temperature, float humidity) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
  
    // Display air quality
    display.setCursor(0, 0);
    display.print("Air Quality: ");
    display.println(airQuality);
  
    // Display temperature
    display.setCursor(0, 10);
    display.print("Temp: ");
    display.print(temperature);
    display.println(" C");

    // Display humidity
    display.setCursor(0, 20);
    display.print("Humidity: ");
    display.print(humidity);
    display.println(" %");

    // Display an alert if air quality is poor
    if (airQuality > AIR_QUALITY_THRESHOLD) {
        display.setTextSize(2);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(0, 35);
        display.println("ALERT!");
    }

    display.display(); // Show the readings on the display
}

// Function to trigger a siren with the buzzer in a 1-0-1 pattern
void triggerSiren() {
    for (int i = 0; i < 3; i++) { // 3 beeps
        digitalWrite(BUZZER_PIN, HIGH);
        delay(200); // Buzzer ON for 200 ms
        digitalWrite(BUZZER_PIN, LOW);
        delay(200); // Buzzer OFF for 200 ms
    }
}
