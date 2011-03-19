#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus

bus = dbus.SessionBus()
busObj = dbus.Interface(bus.get_object(dbus.BUS_DAEMON_NAME,
                                       dbus.BUS_DAEMON_PATH),
                        dbus_interface=dbus.BUS_DAEMON_IFACE)
names = busObj.ListNames()
for name in names:
    if name[0] != ':':
        service = bus.get_object(name, "/")
        print dir(service)
        ##intro = service.Introspect(dbus_interface=dbus.INTROSPECTABLE_IFACE)
        #print intro

