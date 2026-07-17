# GPIO used PD8, PD17

import gpiod
import sys

#
default_state=1

chip=gpiod.Chip('gpiochip0')

linesKey = chip.get_lines([104])
linesLed = chip.get_lines([113])

linesKey.request(consumer='foobar', type=gpiod.LINE_REQ_EV_BOTH_EDGES)
linesLed.request(consumer='foobar', type=gpiod.LINE_REQ_DIR_OUT, default_vals=[default_state])

while True:
    ev_lines = linesKey.event_wait(sec=1)
    if ev_lines:
            for line in ev_lines:
                            event = line.event_read()
                            #print_event(event)
                            if event.type == gpiod.LineEvent.RISING_EDGE:
                                evstr = ' RISING EDGE'
                                linesLed.set_values([not(default_state)])
                            elif event.type == gpiod.LineEvent.FALLING_EDGE:
                                evstr = 'FALLING EDGE'
                                linesLed.set_values([default_state])
                            else:
                                raise TypeError('Invalid event type')
                            print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                                               event.source.offset(),
                                                                               event.sec, event.nsec))
                                            