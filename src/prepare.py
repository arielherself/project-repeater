import asyncio
import GPIO
from misc import getch

VL_BASE = 30
VR_BASE = 27
RATIO = 0.1

async def main():
    try:
        recorder = GPIO.Recorder('actions.pkl', verbosed=True)
        while 1:
            p = getch()
            if p == 'w':
                await recorder.set_speed_and_dump(VL_BASE, VR_BASE)
            elif p == 's':
                await recorder.set_speed_and_dump(0, 0)
            elif p == 'a':
                await recorder.set_speed_and_dump(max(recorder.lspeed-RATIO*VL_BASE, 0.0), recorder.rspeed)
            elif p == 'd':
                await recorder.set_speed_and_dump(recorder.lspeed, max(recorder.rspeed-RATIO*VR_BASE, 0.0))
            elif p == 'q':
                await recorder.finish()
                break
    except:
        print('Unexpected interrupt.')
        await recorder.finish()
            
if __name__ == '__main__':
    asyncio.run(main())