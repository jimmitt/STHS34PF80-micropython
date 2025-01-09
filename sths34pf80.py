import machine
import time

class STHS34PF80:
    WHO_AM_I_REG = 0x0F
    WHO_AM_I_VAL = 0xD3
    CTRL1_REG = 0x20
    STATUS_REG = 0x23
    TOBJECT_L_REG = 0x26
    TOBJECT_H_REG = 0x27
    TAMBIENT_L_REG = 0x28
    TAMBIENT_H_REG = 0x29

    def __init__(self, i2c, address=0x5A):
        """
        Initialize the STHS34PF80 sensor.

        :param i2c: The I2C bus instance.
        :param address: The I2C address of the sensor (default: 0x5A).
        """
        self.i2c = i2c
        self.address = address

        # Verify connection
        if not self._check_device():
            raise OSError("STHS34PF80 not found on I2C bus.")

        # Initialize the sensor
        self._initialize_sensor()

    def _check_device(self):
        """
        Check if the device is present on the I2C bus.
        """
        try:
            who_am_i = self._read_register(self.WHO_AM_I_REG)
            return who_am_i[0] == self.WHO_AM_I_VAL
        except OSError:
            return False

    def _initialize_sensor(self):
        """
        Initialize the sensor with default settings.
        """
        # Set Output Data Rate (ODR) to 1 Hz (CTRL1_REG: ODR[3:0] = 0011)
        self._write_register(self.CTRL1_REG, 0x03)

    def _write_register(self, register, value):
        """
        Write a byte to a specific register.

        :param register: The register address.
        :param value: The value to write.
        """
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    def _read_register(self, register, length=1):
        """
        Read data from a specific register.

        :param register: The register address.
        :param length: Number of bytes to read (default: 1).
        :return: The data read from the register.
        """
        return self.i2c.readfrom_mem(self.address, register, length)

    def get_presence_status(self):
        """
        Get the human presence detection status.

        :return: True if presence is detected, False otherwise.
        """
        status = self._read_register(self.STATUS_REG)
        # Assuming presence detection is indicated by bit 0 in STATUS_REG
        return bool(status[0] & 0x01)

    def get_object_temperature(self):
        """
        Get the object temperature reading.

        :return: Temperature in Celsius.
        """
        temp_l = self._read_register(self.TOBJECT_L_REG)[0]
        temp_h = self._read_register(self.TOBJECT_H_REG)[0]
        temp_raw = (temp_h << 8) | temp_l
        # Convert raw value to Celsius (example conversion)
        return temp_raw * 0.01

    def get_ambient_temperature(self):
        """
        Get the ambient temperature reading.

        :return: Temperature in Celsius.
        """
        temp_l = self._read_register(self.TAMBIENT_L_REG)[0]
        temp_h = self._read_register(self.TAMBIENT_H_REG)[0]
        temp_raw = (temp_h << 8) | temp_l
        # Convert raw value to Celsius (example conversion)
        return temp_raw * 0.01

# Example usage:
# from machine import I2C, Pin
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# sensor = STHS34PF80(i2c)
# print(sensor.get_presence_status())
# print(sensor.get_object_temperature())
# print(sensor.get_ambient_temperature())
