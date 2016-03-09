from datetime import timedelta


class Timer(object):
    timer = timedelta()
    is_editing = False
    is_active = False
    is_alarmed = False
    timer_string_list = ['']
    timer_string = ''
    current_index = 0

    number_keys = {
        'numpad1': '1',
        'numpad2': '2',
        'numpad3': '3',
        'numpad4': '4',
        'numpad5': '5',
        'numpad6': '6',
        'numpad7': '7',
        'numpad8': '8',
        'numpad9': '9',
        'numpad0': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '0': '0',
    }
    separator_keys = ['tab', ':', 'space']
    terminator_keys = ['enter', 'numpadenter']
    reset_keys = ['escape', 'backspace']
    alarm_reset_keys = ['enter', 'numpadenter', 'escape', 'backspace', 'space']
    all_keys = number_keys.keys() + reset_keys + alarm_reset_keys

    def reset(self, *args):
        self.is_editing = False
        self.timer = timedelta()
        self.current_index = 0
        self.is_active = False
        self.is_alarmed = False
        self.timer_string = ''

    def add(self, char):
        self.timer_string += self.number_keys[char]

    def sep(self):
        self.current_index += 1

    def key(self, char):
        if char in self.reset_keys:
            # Reset at any point
            self.reset()

        if char in self.number_keys and not self.is_active and not self.is_editing:
            # Start editing when inactive an numbers are pushed
            self.is_editing = True

        if self.is_editing:
            # Handle edit keys
            if char in self.separator_keys:
                self.sep()
            elif char in self.number_keys:
                self.add(char)
            elif char in self.terminator_keys:
                self.done()

        if self.is_alarmed:
            # Handle alarm reset
            if char in self.alarm_reset_keys:
                self.reset()

    def current_input_value(self):
        if len(self.timer_string) % 2:
            adigits = '0' + self.timer_string
        else:
            adigits = self.timer_string
        digits = []
        for i in range(0, len(adigits) / 2):
            digits.append(''.join(adigits[i * 2: (i + 1) * 2]))
        digits.reverse()
        while len(digits) < 3:
            digits.append('00')
        seconds = 0
        minutes = 0
        hours = 0
        if len(digits) > 0:
            seconds = int(digits[0])
        if len(digits) > 1:
            minutes = int(digits[1])
        if len(digits) > 2:
            hours = int(digits[2])
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def done(self, *args):
        self.is_editing = False
        self.timer = self.current_input_value()
        if self.timer.total_seconds() == 0:
            self.reset()
        else:
            self.is_active = True

    def countdown(self, *args):
        if self.is_active:
            if self.is_alarmed:
                # Alarm triggered, continue counting down
                self.timer += timedelta(seconds=1)
            elif self.timer.total_seconds() == 0:
                # Countdown reached, set alarm
                self.is_alarmed = True
                self.timer += timedelta(seconds=1)
            else:
                # Countdown while there's still time
                self.timer -= timedelta(seconds=1)

    def __str__(self):
        if self.is_editing:
            return str(self.current_input_value())
        elif self.is_active:
            timestring = str(self.timer)
            return "{}{}".format(
                '-' if self.is_alarmed else '',
                timestring,
            )
        else:
            return ''
