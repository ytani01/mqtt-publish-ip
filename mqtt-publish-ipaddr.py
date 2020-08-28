#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Publish IP address via MQTT(beebotte)
"""
__author__ = 'Yoichi Tanibayashi'
__data__   = '2020'

from Mqtt import BeebottePublisher as BBT
from IpAddr import IpAddr
import os
import time
from MyLogger import get_logger
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


MYNAME  = 'mqtt-publish-ipaddr'
VERSION = '0.00'


class MqttPublishIpaddrApp:
    RES_HOSTNAME = 'hostname'
    RES_IP = 'ipaddr'
    RES_MAC = 'macaddr'
    RES_COMMENT = 'comment'

    _log = get_logger(__name__, False)

    def __init__(self, channel, token, comment, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s, token=%s, comment=%s',
                        channel, token, comment)

        self._channel = channel
        self._token = token
        self._comment = comment

        self._hostname = os.uname()[1]
        self._ipaddr = ''
        self._macaddr = ''

        self._topic_hostname = self._channel + '/' + self.RES_HOSTNAME
        self._topic_ipaddr = self._channel + '/' + self.RES_IP
        self._topic_macaddr = self._channel + '/' + self.RES_MAC
        self._topic_comment = self._channel + '/' + self.RES_COMMENT

        self._obj_ipaddr = IpAddr()
        self._obj_bbt = BBT(self._token)

    def main(self):
        self._log.debug('')

        '''
        get IP address and MAC address
        '''
        addrs = None
        while ( addrs is None ):
            addrs = self._obj_ipaddr.get_ip_mac()
            self._log.debug('addrs=%s', addrs)
            if addrs is None:
                time.sleep(2)

        self._ipaddr = addrs['ip']
        self._macaddr = addrs['mac']
        msg = '%s  %s  %s  %s' % (
            self._hostname, self._ipaddr, self._macaddr, self._comment)
        print(msg)

        '''
        publish data
        '''
        self._obj_bbt.start()
        self._obj_bbt.send_data(self._hostname, self._topic_hostname)
        self._obj_bbt.send_data(self._ipaddr, self._topic_ipaddr)
        self._obj_bbt.send_data(self._macaddr, self._topic_macaddr)
        self._obj_bbt.send_data(self._comment, self._topic_comment)
        time.sleep(1)
        self._obj_bbt.end()


@click.command(context_settings=CONTEXT_SETTINGS, help='''
Publish IP address via MQTT(beebotte) -- Ver. %s

  'CHANNEL':Channel Name, 'TOKEN':Channel Token
''' % (VERSION))
@click.argument('channel')
@click.argument('token')
@click.option('--comment', '-c', 'comment', type=str, default='',
              help='comment text')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(channel, token, comment, debug):
    _log = get_logger(__name__, debug)
    _log.debug('channel=%s, token=%s, comment=%s',
               channel, token, comment)

    app = MqttPublishIpaddrApp(channel, token, comment, debug=debug)
    try:
        app.main()
    finally:
        _log.debug('end')


if __name__ == "__main__":
    main()

# for emacs
#  Local Variables:
#  Coding: utf-8-unix
#  End:
