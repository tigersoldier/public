#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
import sys
service = "org.mpris.audacious"
interface = "org.freedesktop.MediaPlayer"
object_path = "/Player"

def call0(iface, cmd, *args):
    method = {
        "play": "Play",
        "pause": "Pause",
        "next": "Next",
        "prev": "Prev",
        "stop": "Stop",
        }
    func = getattr(iface, method[cmd])
    func()

def seek(iface, cmd, *args):
    pass

handlers = {
    "play": call0,
    "pause": call0,
    "next": call0,
    "prev": call0,
    "stop": call0,
    "seek": seek,
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s <cmd> [args]" % sys.argv[0]
        exit(1)
    if not sys.argv[1] in handlers:
        print "Bad command ``%s''" % sys.argv[1]
        exit(1)

    session = dbus.SessionBus()
    try:
        proxy = session.get_object(service, object_path);
    except dbus.DBusException:
        print "Can not connect to service"
        exit(1)
    iface = dbus.Interface(proxy, dbus_interface=interface)
    handlers[sys.argv[1]](iface, *sys.argv[1:])
