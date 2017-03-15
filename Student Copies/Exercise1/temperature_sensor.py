import glob
import os
import re

class TemperatureSensor:
    'Represents an attached DS18B20 temperature sensor.'
    def read_file(self, file):
        """
        Reads the contents of the specified file.

        Args:
            self: A reference to the temperature sensor performing the read operation.
            file: The path of the file to read.

        Returns:
            The contents of the specified file, or None if an error occurs.
        """
        content = None
        try:
            file_handle = open(file,'r')
            content = file_handle.read()
            file_handle.close()
        except Exception as e:
            print('Failed to open file: ' + str(e))
        return content

    def get_sensor_file(self):
        """
        Finds the path to the first attached DS18B20 temperature sensor.

        Args:
            self: A reference to the temperature sensor performing the operation.

        Returns:
            The file representing the temperature sensor's response when queried.
        """
        attached_temperature_sensors = glob.glob('/sys/bus/w1/devices/28-*')
        if len(attached_temperature_sensors) == 0:
            raise FileNotFoundError('No attached temperature sensors found.')
    
        return attached_temperature_sensors[0] + '/w1_slave'

    def read_temp(self):
        """
        Parses the sensor file for a temperature. Assumes the file is formatted as a DS18B20 response.

        Args:
            self: The temperature sensor to read the value of.

        Returns:
            The temperature from the file in Fahrenheit, or 0 if an error occurs.
        """
        temp_f = 0.0
        try:
            lines = self.read_file(self.sensor_file)
            while not re.search(r'YES', lines):
                time.sleep(0.2)
                lines = self.read_file(self.sensor_file)
            temp_string = re.search('t=([-]?\d+)', lines).group(1)
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
        except Exception as e:
            print('Failed to read temperature sensor value: ' + str(e))
            print('Check that your temperature sensor is plugged in correctly.')
        return temp_f

    def __init__(self):
        """
        Initializes a new DS18B20 temperature sensor object.

        Args:
            self: A reference to the temperature sensor object to be created.
        """
        self.sensor_file=self.get_sensor_file()

if __name__ == "__main__":
    sensor = TemperatureSensor()
    while True:
        print(sensor.read_temp())
