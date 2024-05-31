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

# Time between sensor reads, in seconds
READ_TIMEOUT = 2

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_IO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username).
ADAFRUIT_IO_USERNAME = 'YOUR_USERNAME'

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

try: # if we have a 'digital' feed
    digital = aio.feeds('digital')
except RequestError: # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)
# setup the grovepi sensors

LED = 2		# Connect the Grove LED to digital port D4
pinMode(LED,"OUTPUT")
sensor = 4  # The Sensor goes on digital port 4.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.



# Initialize the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# Initialize AHT20 using the default address (0x38) and the board's default i2c bus
# sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    data = aio.receive(digital.key) #receive data from Adafruit_IO
    print(data.value)
    if int(data.value) == 1:
        print('received <- ON\n')
    elif int(data.value) == 0:
        print('received <- OFF\n')

    # set the LED to the feed value
    #led_value = int(data.value)
    digitalWrite(LED, int(data.value))		# Send value on LED
    try:
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,hum] = grovepi.dht(sensor,blue)  
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
    # Format sensor data as string for sending to Adafruit IO
    temperature = '%.2f'%(temperature)
    humidity = '%.2f'%(humidity)
    # Send humidity and temperature data to Adafruit IO
    aio.send(temperature_feed.key, str(temperature))
    aio.send(humidity_feed.key, str(humidity))

    # Timeout to avoid flooding Adafruit IO
    time.sleep(READ_TIMEOUT)

