#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject

service = "org.mpris.demo"
#service = "org.mpris.audacious"
interface = "org.freedesktop.MediaPlayer"
object_path = "/Player"
loop = gobject.MainLoop()

def track_change_cb(track, sender=None):
    print "Track changed: %s" % track['title']
    print "Sender is: %s" % sender

if __name__ == '__main__':
    mainloop = DBusGMainLoop()
    session = dbus.SessionBus(mainloop=mainloop)
    try:
        proxy = session.get_object(service, object_path);
    except dbus.DBusException:
        print "Can not connect to service"
        exit(1)
    iface = dbus.Interface(proxy, dbus_interface=interface)
    iface.connect_to_signal("TrackChange",
                            track_change_cb,
                            sender_keyword="sender")
    loop.run()
