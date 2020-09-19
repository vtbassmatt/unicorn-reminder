import asyncio
from asyncio.locks import Event
import datetime
from enum import Enum


class EventKind(Enum):
    NOTHING = 0
    ALERT = 1
    REMIND = 2
    CALM = 3


SCHEDULE = [
    # 0 - Monday
    [
        {
            'name': 'Do nothing',
            'until': datetime.time(8, 0, 0),
            'kind': EventKind.NOTHING,
        },
        {
            'name': 'Show an alert',
            'until': datetime.time(11, 50, 0),
            'kind': EventKind.ALERT,
        },
        {
            'name': 'Show a reminder',
            'until': datetime.time(12, 0, 0),
            'kind': EventKind.REMIND,
        },
        {
            'name': 'Calm',
            'until': datetime.time(17, 0, 0),
            'kind': EventKind.CALM,
        },
        {
            'name': 'Do nothing',
            'until': datetime.time.max,
            'kind': EventKind.NOTHING,
        },
    ],
    # [
    #     {
    #         'name': 'Homeroom',
    #         'until': datetime.time(8, 30, 0),
    #     },
    #     {
    #         'name': 'Math',
    #         'until': datetime.time(9, 0, 0),
    #     },
    #     {
    #         'name': 'ELA',
    #         'until': datetime.time(11, 0, 0),
    #     },
    #     {
    #         'name': 'Social Studies',
    #         'until': datetime.time(13, 0, 0),
    #     },
    # ],
    # 1 - Tuesday
    [
        {
            'name': 'Homeroom',
            'until': datetime.time(8, 30, 0),
        },
        {
            'name': 'Math',
            'until': datetime.time(9, 0, 0),
        },
        {
            'name': 'ELA',
            'until': datetime.time(11, 0, 0),
        },
    ],
    # 2 - Wednesday
    [
        {
            'name': 'Homeroom',
            'until': datetime.time(8, 30, 0),
        },
        {
            'name': 'Math',
            'until': datetime.time(9, 0, 0),
        },
        {
            'name': 'ELA',
            'until': datetime.time(11, 0, 0),
        },
        {
            'name': 'Social Studies',
            'until': datetime.time(13, 0, 0),
        },
    ],
    # 3 - Thursday
    [
        {
            'name': 'Homeroom',
            'until': datetime.time(8, 30, 0),
        },
        {
            'name': 'Math',
            'until': datetime.time(9, 0, 0),
        },
        {
            'name': 'ELA',
            'until': datetime.time(11, 0, 0),
        },
    ],
    # 4 - Friday
    [
        {
            'name': 'Homeroom',
            'until': datetime.time(8, 30, 0),
        },
        {
            'name': 'Math',
            'until': datetime.time(9, 0, 0),
        },
        {
            'name': 'ELA',
            'until': datetime.time(11, 0, 0),
        },
        {
            'name': 'Social Studies',
            'until': datetime.time(13, 0, 0),
        },
    ],
    # 5 - Saturday
    [
        {
            'name': 'Do nothing',
            'until': datetime.time(14, 0, 0),
            'kind': EventKind.NOTHING,
        },
        {
            'name': 'Show an alert',
            'until': datetime.time(15, 0, 0),
            'kind': EventKind.ALERT,
        },
        {
            'name': 'Show a reminder',
            'until': datetime.time(16, 0, 0),
            'kind': EventKind.REMIND,
        },
        {
            'name': 'Calm',
            'until': datetime.time(17, 0, 0),
            'kind': EventKind.CALM,
        },
        {
            'name': 'Do nothing',
            'until': datetime.time.max,
            'kind': EventKind.NOTHING,
        },
    ],
    # 6 - Sunday
    [
        {
            'name': 'Coffee',
            'until': datetime.time(7, 30, 0),
        },
    ],
]

def get_today_schedule():
    weekday = datetime.datetime.now().weekday()
    return SCHEDULE[weekday]


class Schedule:
    def __init__(self):
        self.task = asyncio.create_task(self._get_next_event(0))
        self.events = []
        self.event_frequency = 30
    
    async def _get_next_event(self, time_to_wait):
        await asyncio.sleep(time_to_wait)

        schedule = get_today_schedule()

        now = datetime.datetime.now().time()
        for event in schedule:
            # assumes the events come in sorted by time
            if now < event['until']:
                return event
        
        return {
            'name': '',
            'until': datetime.time.max,
            'kind': EventKind.NOTHING,
        }

    def has_event(self):
        return len(self.events) > 0
    
    def get_next_event(self):
        return self.events.pop()
    
    def update(self, current):
        if self.task.done():
            self.events.append(self.task.result())
            self.task = asyncio.create_task(self._get_next_event(self.event_frequency))
