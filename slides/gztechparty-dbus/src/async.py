#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import glib

service = "org.mpris.audacious"
interface = "org.freedesktop.MediaPlayer"
object_path = "/Player"
loop = glib.MainLoop()

def reply_cb(metadata):
    print "Got Metadata"
    for k, v in metadata.items():
        print "%s: %s" % (k, v)
    loop.quit()

def error_cb(e):
    print "Async call failed"
    loop.quit()

if __name__ == '__main__':
    mainloop = DBusGMainLoop()
    bus = dbus.SessionBus(mainloop=mainloop)
    try:
        proxy = bus.get_object(service, object_path);
    except dbus.DBusException:
        print "Can not connect to service"
        exit(1)
    iface = dbus.Interface(proxy, dbus_interface=interface)
    iface.GetMetadata(reply_handler=reply_cb,
                      error_handler=error_cb)
    loop.run()
