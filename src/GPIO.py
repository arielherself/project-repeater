import RPi.GPIO as GPIO
import time
from threading import Lock
import pickle

def require_working_lock(func):
    async def wrapper(*args, **kwargs):
        self = args[0]
        with self._working_lock:
            return await func(*args, **kwargs)
    return wrapper

class Recorder:
    def __init__(self, filename, verbosed=False):
        EA, I2, I1, EB, I4, I3 = (
            13, 19, 26, 16, 20, 21)
        FREQUENCY = 50
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.output([EA, I2, EB, I3], GPIO.LOW)
        GPIO.output([I1, I4], GPIO.HIGH)

        self._pwma = GPIO.PWM(EB, FREQUENCY)
        self._pwmb = GPIO.PWM(EA, FREQUENCY)
        self._pwma.start(0)
        self._pwmb.start(0)
        self._lspeed = 0
        self._rspeed = 0
        self._working_lock = Lock()

        self._actions = []
        self.filename = filename
        self.verbosed = verbosed

        if verbosed:
            print('Ready.')

    @require_working_lock
    async def finish(self):
        self._pwma.stop()
        self._pwmb.stop()
        GPIO.cleanup()
        with open(self.filename, 'wb') as f:
            pickle.dump(self._actions, f)
        if self.verbosed:
            print('Finished dumping.')

    @property
    def lspeed(self):
        return self._lspeed
    
    @property
    def rspeed(self):
        return self._rspeed

    @require_working_lock
    async def set_speed(self, lspeed, rspeed):
        self._pwma.ChangeDutyCycle(lspeed)
        self._pwmb.ChangeDutyCycle(rspeed)
        self._lspeed, self._rspeed = lspeed, rspeed
        if self.verbosed:
            print(f'lspeed: {lspeed}, rspeed: {rspeed}')

    @require_working_lock
    async def set_speed_and_dump(self, lspeed, rspeed):
        self._actions.append([time.time(), lspeed, rspeed])
        self._pwma.ChangeDutyCycle(lspeed)
        self._pwmb.ChangeDutyCycle(rspeed)
        self._lspeed, self._rspeed = lspeed, rspeed
        if self.verbosed:
            print(f'lspeed: {lspeed}, rspeed: {rspeed}')
    
