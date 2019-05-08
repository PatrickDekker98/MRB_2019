#https://github.com/tino/pyFirmata


from pyfirmata import Arduino
import time

from PID import PID

#create a Arduino board
board = Arduino('COM2')

#create PID
pid = PID(10,10,10)


#pwm control
pin3 = board.get_pin('d:3:p')
error = 0

while True:
    #error = get error
    gas = pid.Calc(error)
    if gas <= 256 and gas >= 0:
        pin3.write(gas/255)
    elif gas < 0:
        pin3.write(0)
    elif gas > 256:
        pin3.write(1)
    time.sleep(0.1)





