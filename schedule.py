import asyncio
import datetime
import json
import logging

from events import EventKind


class EventProvider:
    def __init__(self):
        with open('schedule.json') as f:
            self.schedule = json.load(f)
        
        # rewrite schedule data
        for event_name, payload in self.schedule.items():
            at = payload['at'].split(':')
            real_time = datetime.time(int(at[0]), int(at[1]), int(at[2]))
            self.schedule[event_name]['at'] = real_time

            kind = EventKind[payload['kind']]
            self.schedule[event_name]['kind'] = kind

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
            raise RuntimeError('could not find a future event to return')

        return event
    
    def _get_next_event_on(self, day_of_week, check_time):
        last_event = { 'start': datetime.datetime.min }

        for name, sched_event in self.schedule.items():
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
        for name, sched_event in self.schedule.items():
            if day_of_week in sched_event['on']:
                event = {
                    'name': name,
                    'kind': sched_event['kind'],
                    'start': datetime.datetime.combine(now.date(), sched_event['at']),
                }

                if last_event['start'] <= now <= event['start']:
                    if 'name' in last_event:
                        return last_event

                    # if we haven't reached the first event of the day,
                    # return a big nothing-burger
                    return {
                        'name': 'Have not reached first event of the day',
                        'kind': EventKind.NOTHING,
                        'start': datetime.datetime.combine(now.date(), datetime.time(0, 0, 0)),
                    }
                
                last_event = event

        raise RuntimeError('could not find a current event to return')


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
