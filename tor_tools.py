import stem
import io
import pycurl
import stem.process
from stem.util import term
from stem.control import Controller
from stem import Signal


class PrivacyTools():
    def __int__(self):
        pass

    def set_exits(self):
        """
         Only works for local instances of Tor
         See Ubuntu /etc/tor/torrc for hard config
         sets Tor Exit nodes  locations
         https://stem.torproject.org/tutorials/to_russia_with_love.html
        """
        tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(SOCKS_PORT),
                'ExitNodes': '{ro},{ru}',
            },
            init_msg_handler=print_bootstrap_lines,
        )


    def change_torIP(self):
        """
        Change Tor Identity
        https://stem.torproject.org/faq.html
        """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print('Changed IP!')






















""""
import functools

from stem import StreamStatus
from stem.control import EventType, Controller

def main():
  print("Tracking requests for tor exits. Press 'enter' to end.")
  print("")

  with Controller.from_port() as controller:
    controller.authenticate()

    stream_listener = functools.partial(stream_event, controller)
    controller.add_event_listener(stream_listener, EventType.STREAM)

    input()  # wait for user to press enter


def stream_event(controller, event):
  if event.status == StreamStatus.SUCCEEDED and event.circ_id:
    circ = controller.get_circuit(event.circ_id)

    exit_fingerprint = circ.path[-1][0]
    exit_relay = controller.get_network_status(exit_fingerprint)

    print("Exit relay for our connection to %s" % (event.target))
    print("  address: %s:%i" % (exit_relay.address, exit_relay.or_port))
    print("  fingerprint: %s" % exit_relay.fingerprint)
    print("  nickname: %s" % exit_relay.nickname)
    print("  locale: %s" % controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown'))
    print("")


if __name__ == '__main__':
  main()
"""

















