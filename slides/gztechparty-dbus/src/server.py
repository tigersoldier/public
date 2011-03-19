#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
import dbus.service
import glib
from dbus.mainloop.glib import DBusGMainLoop

MPRIS_IFACE = 'org.freedesktop.MediaPlayer'
BUS_NAME = 'org.mpris.demo'

class DemoPlayer(object):
    """ MPRIS service demo
    """
    
    def __init__(self, bus_name):
        self._bus_name = dbus.service.BusName(bus_name, dbus.SessionBus())
        self._root_obj = MprisRoot(self, self._bus_name)
        self._player_obj = MprisPlayer(self, self._bus_name)
        self._current = 0
        self._tracks = [{
                'title': 'Track A',
                'artist': 'Artist A',
                }, {
                'title': 'Track B',
                'artist': 'Artist B',
                }, {
                'title': 'Track C',
                'artist': 'Artist C',
                },
            ]


    def GetMetadata(self, index):
        return self._tracks[index]

    def GetCurrentTrack(self):
        return self._current

    def SetCurrentTrack(self, index):
        self._current = (index + len(self._tracks)) % len(self._tracks)
        self._player_obj.TrackChange(self.GetMetadata(self.GetCurrentTrack()))

    def Prev(self):
        self.SetCurrentTrack(self._current - 1)

    def Next(self):
        self.SetCurrentTrack(self._current + 1)

class MprisRoot(dbus.service.Object):
    """ MPRIS '/' object
    """
    
    def __init__(self, player, bus_name):
        dbus.service.Object.__init__(self,
                                     bus_name=bus_name,
                                     object_path='/')
    @dbus.service.method(dbus_interface=MPRIS_IFACE,
                         in_signature='',
                         out_signature='s')
    def Identity(self):
        return 'MPRIS Demo 0.1'

    
class MprisPlayer(dbus.service.Object):
    """ MPRIS '/Player' object
    """
    
    def __init__(self, player, bus_name):
        self._player = player
        dbus.service.Object.__init__(self,
                                     bus_name=bus_name,
                                     object_path='/Player')

    @dbus.service.method(dbus_interface=MPRIS_IFACE,
                         in_signature='',
                         out_signature='a{sv}')
    def GetMetadata(self):
        return self._player.GetMetadata(self._player.GetCurrentTrack())

    @dbus.service.method(dbus_interface=MPRIS_IFACE,
                         in_signature='',
                         out_signature='')
    def Next(self):
        self._player.Next()

    @dbus.service.method(dbus_interface=MPRIS_IFACE,
                         in_signature='',
                         out_signature='')
    def Prev(self):
        self._player.Prev()

    @dbus.service.signal(dbus_interface=MPRIS_IFACE,
                         signature='a{sv}')
    def TrackChange(self, track):
        pass

if __name__ == '__main__':
    loop = glib.MainLoop()
    dbus_loop = DBusGMainLoop(set_as_default=True)
    player = DemoPlayer(BUS_NAME)
    loop.run()
