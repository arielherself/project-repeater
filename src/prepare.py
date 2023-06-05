import asyncio
import GPIO
from misc import getch

V_BASE = 30
RATIO = 0.1

async def main():
    recorder = GPIO.Recorder('actions.pkl', verbosed=True)
    while 1:
        p = getch()
        if p == 'w':
            await recorder.set_speed_and_dump(V_BASE, V_BASE)
        elif p == 's':
            await recorder.set_speed_and_dump(0, 0)
        elif p == 'd':
            await recorder.set_speed_and_dump(recorder.lspeed-RATIO*V_BASE, recorder.rspeed)
        elif p == 'a':
            await recorder.set_speed_and_dump(recorder.lspeed, recorder.rspeed-RATIO*V_BASE)
        elif p == 'q':
            await recorder.finish()
            break
            
if __name__ == '__main__':
    asyncio.run(main())