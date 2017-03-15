from signal import *
import atexit
import helpers
import resources
import sys
import temperature_sensor
import time

import part1
import part2
import part3
import part4

# Type in your Raspberry Pi's name, description, and location here
name = "Example Raspberry Pi Name (dont use me!)"
description = "This is my Raspberry Pi!"
position_x = -1
position_y = -1

# (Set up some helpers to clean up when we finish running):
permit_cleanup = True
atexit.register(lambda: helpers.perform_part5_cleanup(name, permit_cleanup))
for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM, SIGHUP):
    signal(sig, lambda x, y: helpers.perform_part5_cleanup(name, permit_cleanup))

if __name__ == "__main__":
    # First, we need to create a PI Point:
    pipoint_response = part1.create_pipoint(
        name,
        resources.base_url,
        resources.dataserver_web_id)

    # (We check that the PI Point was successfully created before continuing):
    if pipoint_response.text != "":
        permit_cleanup = False
    print(pipoint_response.text)

    # (We need the PI Point WebId later, so we get it now):
    pipoint_web_id = helpers.get_web_id(pipoint_response)

    # Second, we need to create an AF Element:
    element_response = part2.create_af_element(
        name,
        description,
        resources.base_url,
        resources.parent_af_element_web_id)
    
    # (Here, we retrieve the WebIds for the X and Y coordinate attributes):
    coordinate_web_ids = helpers.get_coordinate_locations(element_response)

    # Third, we update the X and Y coordinates to match our location:
    part3.update_af_attribute(
        position_x,
        resources.base_url,
        coordinate_web_ids.x_web_id)
    part3.update_af_attribute(
        position_y,
        resources.base_url,
        coordinate_web_ids.y_web_id)

    # (Here, we retrieve the WebId for the Temperature attribute):
    value_web_id = helpers.get_attribute_web_id_by_name(
        "Temperature",
        resources.base_url,
        helpers.get_web_id(element_response))

    # Finally, we read the temperature from the temperature sensor, and POST
    # the value to the PI Point:
    sensor = temperature_sensor.TemperatureSensor()
    while True:
        current_temperature = sensor.read_temp()
        print("Sending:  " + str(current_temperature))
        part4.post_pi_value(
            current_temperature,
            pipoint_web_id,
            resources.base_url)
        print("Received: " + str(helpers.get_attribute_field(
            value_web_id,
            lambda x: x["Value"])))
        time.sleep(5)

    
    
