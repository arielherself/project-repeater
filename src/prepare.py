import asyncio
import GPIO
from misc import getch

async def main():
    recorder = GPIO.Recorder('actions.pkl', verbosed=True)
    while 1:
        p = getch()
        if p == 'w':
            await recorder.set_speed_and_dump(100, 100)
        elif p == 's':
            await recorder.set_speed_and_dump(0, 0)
            await recorder.finish()
        elif p == 'a':
            await recorder.set_speed_and_dump(recorder.lspeed-10, recorder.rspeed)
        elif p == 'd':
            await recorder.set_speed_and_dump(recorder.lspeed, recorder.rspeed-10)
            
if __name__ == '__main__':
    asyncio.run(main())