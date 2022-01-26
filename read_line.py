import readline
import os

HISTORY_FILENAME = 'completer.hist'


def get_history_items():
    """
    Getting a history element from a list in a file
    :return: list
    """
    return [readline.get_history_item(i)
            for i in range(1, readline.get_current_history_length() + 1)
            ]


class HistoryCompleter(object):

    def __init__(self):
        self.matches = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            history_values = get_history_items()
            if text:
                self.matches = sorted(h
                                      for h in history_values
                                      if h and h.startswith(text))
            else:
                self.matches = []
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def input_ing(text=None):
    """
        custom input
    :param text: optional information
    :return: text from input field
    """
    if os.path.exists(HISTORY_FILENAME):
        readline.read_history_file(HISTORY_FILENAME)
    else:
        readline.write_history_file(HISTORY_FILENAME)
    try:
        while True:
            line = input(text if text else "")
            if line:
                history_values = get_history_items()
                history_values.pop()
                l = sorted(line for h in history_values if h and h.startswith(line))
                if len(l) == 0:
                    readline.append_history_file(1, HISTORY_FILENAME)
                return line
    except EOFError:
        return False


# Регистрация класса 'HistoryCompleter'
readline.set_completer(HistoryCompleter().complete)
readline.set_history_length(10)
# Регистрация клавиши `tab` для автодополнения
readline.parse_and_bind('tab: complete')
