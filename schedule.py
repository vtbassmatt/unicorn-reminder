import asyncio
import datetime
import logging

from events import EventKind


SCHEDULE = {
    'Off in the morning': {
        'at': datetime.time(0, 0, 0),
        'kind': EventKind.NOTHING,
        'on': [0, 1, 2, 3, 4, 5, 6],  # every day
    },
    'Good morning': {
        'at': datetime.time(7, 0, 0),
        'kind': EventKind.CALM,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Homeroom soon': {
        'at': datetime.time(8, 26, 0),
        'kind': EventKind.ALERT,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Homeroom reminder': {
        'at': datetime.time(8, 30, 0),
        'kind': EventKind.REMIND,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Calm before math': {
        'at': datetime.time(8, 35, 0),
        'kind': EventKind.CALM,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Math soon': {
        'at': datetime.time(8, 56, 0),
        'kind': EventKind.ALERT,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Math reminder': {
        'at': datetime.time(9, 0, 0),
        'kind': EventKind.REMIND,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Calm after math': {
        'at': datetime.time(9, 5, 0),
        'kind': EventKind.CALM,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'ELA soon': {
        'at': datetime.time(10, 56, 0),
        'kind': EventKind.ALERT,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'ELA reminder': {
        'at': datetime.time(11, 0, 0),
        'kind': EventKind.REMIND,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Calm after ELA': {
        'at': datetime.time(11, 5, 0),
        'kind': EventKind.CALM,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
    'Social studies soon': {
        'at': datetime.time(12, 56, 0),
        'kind': EventKind.ALERT,
        'on': [0, 2, 4],  # MWF
    },
    'Social studies reminder': {
        'at': datetime.time(13, 0, 0),
        'kind': EventKind.REMIND,
        'on': [0, 2, 4],  # MWF
    },
    'Calm after social studies': {
        'at': datetime.time(13, 5, 0),
        'kind': EventKind.CALM,
        'on': [0, 2, 4],  # MWF
    },
    'Off rest of day': {
        'at': datetime.time(17, 0, 0),
        'kind': EventKind.NOTHING,
        'on': [0, 1, 2, 3, 4],  # M-F
    },
}

class EventProvider:
    def get_next_event(self):
        event = None

        # start at now/today
        now = datetime.datetime.now()
        day_of_week = initial_dow = now.weekday()

        while not event and day_of_week < initial_dow + 7:
            event = self._get_next_event_on(day_of_week % 7, now)

            # future iterations of the loop will use next day / midnight
            day_of_week += 1
            now = datetime.datetime.combine(
                now.date() + datetime.timedelta(days=1),
                datetime.time(0, 0, 0)
            )

        if not event:
            raise RuntimeError('could not find an event to return')

        return event
    
    def _get_next_event_on(self, day_of_week, check_time):
        last_event = { 'start': datetime.datetime.min }

        for name, sched_event in SCHEDULE.items():
            if day_of_week in sched_event['on']:
                event = {
                    'name': name,
                    'kind': sched_event['kind'],
                    'start': datetime.datetime.combine(check_time.date(), sched_event['at'])
                }
                
                if last_event['start'] <= check_time <= event['start']:
                    self.last_next_event = event
                    return event
                
                last_event = event

    def get_current_event(self):
        now = datetime.datetime.now()
        day_of_week = now.weekday()
        last_event = { 'start': datetime.datetime.min }
        for name, sched_event in SCHEDULE.items():
            if day_of_week in sched_event['on']:
                event = {
                    'name': name,
                    'kind': sched_event['kind'],
                    'start': datetime.datetime.combine(now.date(), sched_event['at'])
                }

                if last_event['start'] <= now <= event['start']:
                    if 'name' in last_event:
                        return last_event

                    # TODO: handle wrapping to yesterday (or just return nothing?)
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
