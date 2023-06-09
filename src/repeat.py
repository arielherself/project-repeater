from sys import argv
import asyncio
from time import sleep
import pickle
import GPIO
from misc import time_diff

async def main():
    with open(argv[1], 'rb') as f:
        actions = pickle.load(f)

    dl = time_diff([a[0] for a in actions])
    f_actions = []
    for i in range(len(actions)):
        f_actions.append([dl[i], actions[i][1], actions[i][2]])

    recorder = GPIO.Recorder('actions_reflection.pkl', verbosed=True)
    try:
        for i in range(int(argv[2])):
            for time, lspeed, rspeed in f_actions:
                sleep(time)
                await recorder.set_speed(lspeed, rspeed)
    except:
        pass
    await recorder.finish()

if __name__ == '__main__':
    asyncio.run(main())
