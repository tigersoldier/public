#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
service = "org.mpris.audacious"
interface = "org.freedesktop.MediaPlayer"
object_path = "/Player"

if __name__ == '__main__':
    bus = dbus.SessionBus()
    try:
        proxy = bus.get_object(service, object_path);
    except dbus.DBusException:
        print "Can not connect to service"
        exit(1)
    iface = dbus.Interface(proxy, dbus_interface=interface)
    metadata = iface.GetMetadata()
    for k, v in metadata.items():
        print "%s: %s" % (k, v)
