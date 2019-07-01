import time
import cv2
import serial


def send_fan(value, serial_com):
    """
    @brief sends data using serial communication to the arduino with X prefix.
    @param value An integer containing the new x value.
    @param serial_com The serial communication you wan to send to.
    """
    data = "F " + str(int(value)) + "\n"
    send_serial(data, serial_com)


def send_sound(value, serial):
    """
    @brief sends data using serial communication to the arduino with Y prefix.
    @param value An integer containing the new y value.
    @param serial_com The serial communication you wan to send to.
    """
    data = "S " + str(int(value))  + "\n"
    send_serial(data, arduino)


def send_serial(data, serial_com):
    """
    @brief Ecodes the data using ascii and sends it to the serial_com.
    @param data The data you want to send to the serial_com.
    @param serial_com The serial device you want to send the data to.
    """

    data = data.encode("ascii")
    serial_com.write(data)





