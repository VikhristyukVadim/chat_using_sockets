import argparse
from client_socket import Client


def argument_parser():
    """Initialising of arg parser"""
    parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )
    """Creating parser arguments"""
    # Server parser----------------------------------------------------------------------------------------------------
    parser.add_argument('--ip', help="ip address", required=True)
    parser.add_argument('--port', help="connection port", required=True)
    parser.add_argument('-r', help="user registration mode", action="store_true")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    client = Client(argument_parser, argument_parser())
    client.logining()
