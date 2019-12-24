#!/usr/bin/python
import smbus
import time
import pdb

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0 on rPi), 1 = /dev/i2c-1 (port I2C1 on rPi)

DEVICE_ADDRESS = 0x08   #7 bit I2C address
CHANNEL_NR = 32         #number of channels on the ADC, 24 or 32

def photoresistor_read(sensor_number):
    return int(read_ANA(DEVICE_ADDRESS, sensor_number))

def get_all_photoresistor_values(sensor_channels = [i for i in range(5,28)]):
    all_sensors_dict = {}
    #print("Channels:\n" + str(sensor_channels))
    #pdb.set_trace()
    for ch in sensor_channels:
        all_sensors_dict[int(ch)] = int(photoresistor_read(ch))
    return all_sensors_dict


def read_ANA(slave_module, channel_nr):
        try:
            #print("About to read channel: " + str(channel_nr))
            bus.write_i2c_block_data(slave_module, 0x13, [channel_nr, 0x69])
            time.sleep(0.005)
            data = bus.read_i2c_block_data(slave_module, 0)
            time.sleep(0.005)
            if(data[0] == 0x13 and data[3] == 0x69):
                formated_data = data[1] << 8 | data[2]
                if(formated_data <= 0x0FFF):
                    return "%4d" % formated_data
                else:
                    return 0
            else:
                return 0
        except OSError:
            print("Lost connection to the remote I/O ADC.")
            return 0
