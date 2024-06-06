"""
'temp_humidity.py'
==================================
Example of sending temperature and humidity data to Adafruit IO

Author(s): Brent Rubell

Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity

Dependencies:
    - Adafruit IO Python Client
        (https://github.com/adafruit/io-client-python)
    - Adafruit_CircuitPython_AHTx0
        (https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
"""

# import grovepi modules
import grovepi
from grovepi import *

# import standard python modules.
import time
import math

# import adafruit-blinka modules
import board

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Import AHTx0 library
import adafruit_ahtx0

# Set true to send tempertaure data in degrees fahrenheit ('f')?
USE_DEGREES_F = False

# Time between TempHum reads, in seconds
READ_TIMEOUT = 2

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = <YOUR IO KEY>

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = <YOUR USERNAME>

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Assign a temperature feed, if one exists already
try:
    temperature_feed = aio.feeds('temperature')
except RequestError: # Doesn't exist, create a new feed
    feed_temp = Feed(name="temperature")
    temperature_feed = aio.create_feed(feed_temp)

# Assign a humidity feed, if one exists already
try:
    humidity_feed = aio.feeds('humidity')
except RequestError: # Doesn't exist, create a new feed
    feed_humid = Feed(name="humidity")
    humidity_feed = aio.create_feed(feed_humid)

try: # Create a red led feed
    redled = aio.feeds('redled')
    aio.send(redled.key, '0')
except RequestError:
    redled_feed = Feed(name="redled")
    redled = aio.create_feed(redled_feed)
    aio.send(redled.key, '0')
try: # Create a green led feed
    greenled = aio.feeds('greenled')
    aio.send(greenled.key, '0')
except RequestError:
    greenled_feed = Feed(name="greenled")
    greenled = aio.create_feed(greenled_feed)
    aio.send(greenled.key, '0')
try: # Create a blue led feed
    blueled = aio.feeds('blueled')
    aio.send(blueled.key, '0')
except RequestError:
    blueled_feed = Feed(name="blueled")
    blueled = aio.create_feed(blueled_feed)    
    aio.send(blueled.key, '0')
try: # Create a Pot meter analog feed
    potmeter = aio.feeds('potmeter')
except RequestError:
    potmeter_feed = Feed(name="potmeter")
    potmeter = aio.create_feed(potmeter_feed)    
  
# setup the grovepi sensors

POTMETER = 14		# Pin 14 is A0 Port.
BUTTON = 3	# Connect the Grove Button to digital port D3
TempHum = 4  # Connect the Grove TempHum to digital port 4.
LED_RED = 6		# Connect the Grove red LED to digital port D6
LED_GREEN = 7		# Connect the Grove green LED to digital port D7
LED_BLUE = 8		# Connect the Grove blue LED to digital port D8
pinMode(LED_RED,"OUTPUT")
pinMode(LED_GREEN,"OUTPUT")
pinMode(LED_BLUE,"OUTPUT")
pinMode(BUTTON,"INPUT")
pinMode(POTMETER,"INPUT")
# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.



# Initialize the board's default I2C bus
#i2c = board.I2C()  # uses board.SCL and board.SDA
# Initialize AHT20 using the default address (0x38) and the board's default i2c bus
# sensor = adafruit_ahtx0.AHTx0(i2c)

# Turn off all LED at start
#aio.send(redled.key, '0')
#aio.send(greenled.key, '0')
#aio.send(blueled.key, '0')

while True:
    data = aio.receive(redled.key) #receive data from Adafruit_IO
    if int(data.value) == 1:
        digitalWrite(LED_RED, 1)		# Send value to LED
        print("Red LED ON")
    elif int(data.value) == 0:
        digitalWrite(LED_RED, 0)		# Send value to LED
        print("Red LED OFF")
    data = aio.receive(greenled.key) #receive data from Adafruit_IO
    if int(data.value) == 1:
        digitalWrite(LED_GREEN, 1)		# Send value to LED
        print("Green LED ON")
    elif int(data.value) == 0:
        digitalWrite(LED_GREEN, 0)		# Send value to LED
        print("Green LED OFF")
    data = aio.receive(blueled.key) #receive data from Adafruit_IO
    if int(data.value) == 1:
        digitalWrite(LED_BLUE, 1)		# Send value to LED
        print("Blue LED ON")
    elif int(data.value) == 0:
        digitalWrite(LED_BLUE, 0)		# Send value to LED
        print("Blue LED OFF")
    # Read the button    
    button_state = grovepi.digitalRead(BUTTON)
    if(button_state == 1):
        aio.send(redled.key, '0')
        aio.send(greenled.key, '0')
        aio.send(blueled.key, '0')
    print(button_state)
    # Read the POT Meter
    PotMeter = grovepi.analogRead(POTMETER)
    aio.send(potmeter.key, str(PotMeter))
    try:
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,hum] = grovepi.dht(TempHum,blue)  
        if math.isnan(temp) == False and math.isnan(hum) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, hum))
        else:
            print("nan values")

    except IOError:
        print ("Error")    
    temperature = float(temp)
    humidity = float(hum)
    if USE_DEGREES_F:
        temperature = temperature * 9.0 / 5.0 + 32.0
        print('Temp={0:0.1f}*F'.format(temperature))
    else:
        print('Temp={0:0.1f}*C'.format(temperature))
        print('Humidity={0:0.1f}%'.format(humidity))
    # Format TempHum data as string for sending to Adafruit IO
    temperature = '%.2f'%(temperature)
    humidity = '%.2f'%(humidity)
    # Send humidity and temperature data to Adafruit IO
    aio.send(temperature_feed.key, str(temperature))
    aio.send(humidity_feed.key, str(humidity))

    # Timeout to avoid flooding Adafruit IO
    time.sleep(READ_TIMEOUT)