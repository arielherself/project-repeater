import asyncio
import GPIO
from misc import getch

VL_BASE = 30
VR_BASE = 27
RATIO = 0.1

async def main():
    recorder = GPIO.Recorder('actions.pkl', verbosed=True)
    while 1:
        p = getch()
        if p == 'w':
            await recorder.set_speed_and_dump(VL_BASE, VR_BASE)
        elif p == 's':
            await recorder.set_speed_and_dump(0, 0)
        elif p == 'a':
            await recorder.set_speed_and_dump(recorder.lspeed-RATIO*VL_BASE, recorder.rspeed)
        elif p == 'd':
            await recorder.set_speed_and_dump(recorder.lspeed, recorder.rspeed-RATIO*VR_BASE)
        elif p == 'q':
            await recorder.finish()
            break
            
if __name__ == '__main__':
    asyncio.run(main())