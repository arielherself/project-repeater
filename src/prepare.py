import asyncio
import GPIO
from misc import getch

VL_BASE = 60
VR_BASE = 59
RATIO = 0.4
STARTUP_DELTA = 0.1
STARTUP_TIME = 2

async def main():
    try:
        recorder = GPIO.Recorder('actions.pkl', verbosed=True)
        while 1:
            p = getch()
            if p == 'g':
                for _ in range(STARTUP_TIME):
                    await recorder.set_speed_and_dump(VL_BASE, VR_BASE * (1.0 + STARTUP_DELTA))
                await recorder.set_speed_and_dump(VL_BASE, VR_BASE)
            elif p == 'w':
                await recorder.set_speed_and_dump(VL_BASE, VR_BASE)
            elif p == 's':
                await recorder.set_speed_and_dump(0, 0)
            elif p == 'a':
                await recorder.set_speed_and_dump(max(recorder.lspeed-RATIO*VL_BASE, 0.0), recorder.rspeed)
            elif p == 'd':
                await recorder.set_speed_and_dump(recorder.lspeed, max(recorder.rspeed-RATIO*VR_BASE, 0.0))
            elif p == 'q':
                await recorder.finish_and_dump()
                break
            elif p == 'x':
                await recorder.finish()
                break
    except:
        print('Unexpected interrupt.')
        await recorder.finish()
            
if __name__ == '__main__':
    asyncio.run(main())