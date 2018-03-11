from mma8451 import accel
import datetime
import time

MMA8451 = accel.Accel()
MMA8451.init()

if MMA8451.whoAmI() != accel.deviceName:
    print("Error! Device not recognized! (" + str(accel.deviceName) + ")")
    sys.exit()

while True:  # forever loop
    print ("\nCurrent Date-Time: " + str(datetime.datetime.now()))
    axes = MMA8451.getAxisValue()
    MMA8451.debugShowAxisAcceleration(axes['x'], axes['y'], axes['z'])

    time.sleep(0.5)
