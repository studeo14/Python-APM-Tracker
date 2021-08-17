
import asyncio
from asyncio import events
import datetime
import sys
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

start_time = datetime.datetime.now()
total_events = 0
last_minute = []
events_last_second = 0
running_avg = 0

def on_press(key):
    # print(f'Key pressed: {key}')
    global events_last_second
    events_last_second += 1

def on_click(x, y, button, pressed):
    if not  pressed:
        # print(f'Mouse button clicked: {button}')
        global events_last_second
        events_last_second += 1

async def apm_tracker():
    while True:
        await asyncio.sleep(1)
        cur = datetime.datetime.now()
        global total_events, events_last_second, last_minute
        if len(last_minute) < 60:
            last_minute.append(events_last_second)
        else:
            last_minute = last_minute[1:] + [events_last_second]
        events_last_minute = sum(last_minute)
        total_events += events_last_second
        sys.stdout.write("\033[K")
        min = (cur - start_time).total_seconds()/60
        avg = (total_events/min)
        instant_apm = events_last_second*60
        print(f'total events: {int(avg)}, {events_last_minute}, {instant_apm}', end='\r')
        events_last_second = 0

if __name__ == '__main__':
    try:
        kbl = KeyboardListener(on_release=on_press)
        mbl = MouseListener(on_click=on_click)
        kbl.start()
        mbl.start()
        asyncio.run(apm_tracker())
        kbl.join()
        mbl.join()
    except KeyboardInterrupt:
        print('\nFinishing!')
        cur = datetime.datetime.now()
        min = (cur - start_time).total_seconds()/60
        avg = (total_events/min)
        print(f'AVG APM: {avg}')