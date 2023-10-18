import smbus
import time

# Set the address of the light sensor to communicate with
BH1750_I2C_ADDR = 0x23

# Create a connection to the I2C bus (the way the Raspberry Pi talks to devices)
bus = smbus.SMBus(1)

# Function to get the amount of light from the sensor
def read_light_level():
    # Ask the light sensor for data in continuous mode
    data = bus.read_i2c_block_data(BH1750_I2C_ADDR, 0x20)
    
    # Use a formula to calculate the light level in lux
    light_level = (data[1] + (256 * data[0])) / 1.2
    
    return light_level

# Function to describe how bright the light is
def categorize_light(light_level):
    if light_level < 10:
        return "It's too dark"
    elif 10 <= light_level < 50:
        return "It's dark"
    elif 50 <= light_level < 200:
        return "It's somewhat bright"
    elif 200 <= light_level < 500:
        return "It's bright"
    else:
        return "It's too bright"

try:
    # Keep checking the light level
    while True:
        light_level = read_light_level()  # Get the current light level
        category = categorize_light(light_level)  # Describe how bright the light is
        
        # Show the light level and its description
        print(f"Light Level: {light_level} lux - {category}")
        
        # Wait for 1 second before checking again
        time.sleep(1)

except KeyboardInterrupt:
    # If you press Ctrl+C, stop the program nicely
    pass

finally:
    # Close the connection to the light sensor to free up resources
    bus.close()