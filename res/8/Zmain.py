from init import *
import image

def RangeConfig(var, start = 0, stop = 100):
    if var < start:
        return start
    if var > stop:
        return stop
    return var

speed = 100

try:
    pwma.ChangeDutyCycle(0)
    pwmb.ChangeDutyCycle(0)
    running = not input("Press Enter to start")
    print("Start")

    while True:
        config = 0.15 * image.CalcConfig()
        lspeed = speed + config
        rspeed = speed - config
        pwma.ChangeDutyCycle(RangeConfig(lspeed))
        pwmb.ChangeDutyCycle(RangeConfig(rspeed))
except KeyboardInterrupt:
    pass
finally:
    pwma.ChangeDutyCycle(0)
    pwmb.ChangeDutyCycle(0)
    pwma.stop()
    pwmb.stop()
    GPIO.cleanup()
