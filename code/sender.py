#!/usr/bin/env python3

from mma8451 import mma8451
import signal
import sys
from datetime import datetime
import uuid
import numpy as np
import time
import random

from kombu import Connection, Producer, Exchange

piid = 'pi.' + str(uuid.uuid1().node)

print("Starting with id: " + piid)

exch = Exchange('raspi.live', type='direct')

def sigint_handler(signal, frame):
    print('Exiting...')
    MMA8451.close()
    conn.release()
    sys.exit(0)

conn = Connection('amqp://pi:raspberry@192.168.0.105')
conn.connect()
channel = conn.channel()
b_exch = exch(channel)
producer = Producer(channel, exchange=b_exch, routing_key=piid)

def callback(data):
    producer.publish(
        {
            'x': np.average(data[:,0]),
            'y': np.average(data[:,1]),
            'z': np.average(data[:,2]),
        },
        retry=True,
    )


MMA8451 = mma8451.Device()
MMA8451.open()
MMA8451.restart()
MMA8451.configure(bit_depth=14,
                  auto_sleep=False,
                  power_mode="high_resolution",
                  sleep_power_mode="high_resolution",
                  fifo_mode="fill",
                  fifo_watermark=20,
                  low_noise=True)


signal.signal(signal.SIGINT, signal.SIG_IGN)
MMA8451.setup_threaded_fifo_callback(gpio_pin=17,
                                     interrupt_pin=1,
                                     callback=callback,
                                     time_interval=0.05,
                                     convert_to_float=True)

signal.signal(signal.SIGINT, sigint_handler)
print('Finished initialization')
signal.pause()
