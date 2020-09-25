import asyncio
import datetime
import logging

from events import EventKind


STARTUP_TIME = datetime.datetime.now()
FIVE_SECONDS = datetime.timedelta(seconds=5)
TWENTY_SECONDS = datetime.timedelta(seconds=20)

FAKE_EVENTS = [
    {
        'name': 'Show alert',
        'kind': EventKind.ALERT,
        'start': STARTUP_TIME - TWENTY_SECONDS,
    },
    {
        'name': 'Get calm',
        'kind': EventKind.CALM,
        'start': STARTUP_TIME + FIVE_SECONDS,
    },
    {
        'name': 'Do reminder',
        'kind': EventKind.REMIND,
        'start': STARTUP_TIME + TWENTY_SECONDS,
    },
    {
        'name': 'Nothing',
        'kind': EventKind.NOTHING,
        'start': datetime.datetime.max,
    },
]

class EventProvider:
    def get_next_event(self):
        now = datetime.datetime.now()
        last_event = { 'start': datetime.datetime.min }
        for event in FAKE_EVENTS:
            if last_event['start'] < now < event['start']:
                self.last_next_event = event
                return event
            
            last_event = event

        raise NotImplementedError('fallen off the edge of time')

    def get_current_event(self):
        now = datetime.datetime.now()
        last_event = { 'start': datetime.datetime.min }
        for event in FAKE_EVENTS:
            if last_event['start'] < now < event['start']:
                if 'name' in last_event:
                    return last_event
                raise NotImplementedError('before the beginning of time')
            
            last_event = event

        raise NotImplementedError('not even sure how we got here')        


class Schedule:
    def __init__(self):
        self.event_provider = EventProvider()
        self.task = asyncio.create_task(self._get_current_event())
        self.debounce = asyncio.create_task(self._debounce(0))

    async def _get_current_event(self):
        logging.debug('::: _get_current_event :::')
        current_event = self.event_provider.get_current_event()
        logging.debug(f'returning event {current_event["name"]}')
        return current_event
    
    async def _debounce(self, debounce_for=1):
        logging.debug(f'debouncing for {debounce_for}')
        await asyncio.sleep(debounce_for)

    async def _get_next_event(self):
        logging.debug('::: _get_next_event :::')
        next_event = self.event_provider.get_next_event()
        logging.debug(f'the next event will be {next_event["name"]}')
        time_til_event = next_event['start'] - datetime.datetime.now()
        logging.debug(f'sleeping {time_til_event.seconds} seconds')
        await asyncio.sleep(time_til_event.seconds)
        logging.debug(f'returning event {next_event["name"]}')
        return next_event

    def get_next_event(self):
        if self.task.done() and self.debounce.done():
            result = self.task.result()
            self.debounce = asyncio.create_task(self._debounce())
            self.task = asyncio.create_task(self._get_next_event())
            return result
