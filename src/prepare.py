import asyncio
import GPIO
from misc import getch

async def main():
    try:
        recorder = GPIO.Recorder('actions.pkl', verbosed=True)
        while 1:
            p = getch()
            if p == 'w':
                await recorder.set_speed_and_dump(100, 100)
            elif p == 's':
                await recorder.set_speed_and_dump(0, 0)
                await recorder.finish()
                break
            elif p == 'a':
                await recorder.set_speed_and_dump(recorder.lspeed-10, recorder.rspeed)
            elif p == 'd':
                await recorder.set_speed_and_dump(recorder.lspeed, recorder.rspeed-10)
    except KeyboardInterrupt:
        print("Unexpected termination. Did you mean 'd' to stop?")
        await recorder.finish()
            
if __name__ == '__main__':
    asyncio.run(main())