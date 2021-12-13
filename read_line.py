import atexit
import os
import readline
#
if __name__ == '__main__':
    history_file = os.path.join(os.path.expanduser("~"), "._history")

    try:
        readline.read_history_file(history_file)
        h_len = readline.get_current_history_length()
    except FileNotFoundError:
        open(history_file, 'wb').close()
        h_len = 0


    def save(prev_h_len, hist_file):
        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - prev_h_len, hist_file)


    atexit.register(save, h_len, history_file)

# import readline

    # addrs = ['angela@domain.com', 'michael@domain.com', 'david@test.com']
    #
    # def completer(text, state):
    #     options = [x for x in addrs if x.startswith(text)]
    #     try:
    #         return options[state]
    #     except IndexError:
    #         return None
    #
    # readline.set_completer(completer)
    # readline.parse_and_bind("tab: complete")
    #
    # while 1:
    #     a = input("> ")
    #     print ("You entered", a)

# from __future__ import print_function
