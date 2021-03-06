# -*- coding: utf-8 -*-

# pour le bluetooth

""" Panohead remote control.

License
=======

 - B{Papywizard} (U{http://www.papywizard.org}) is Copyright:
  - (C) 2007-2011 Frédéric Mantegazza

This software is governed by the B{CeCILL} license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
U{http://www.cecill.info}.

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

Module purpose
==============

Bluetooth handling

Implements
==========

- BluetoothSocket
- BluetoothError
- discoverDevices

@author: Frédéric Mantegazza
@copyright: (C) 2007-2011 Frédéric Mantegazza
@license: CeCILL
"""

__revision__ = "$Id: bluetoothTransport.py 2498 2011-04-17 07:51:23Z fma $"

import sys

from PyQt4 import QtCore

from papywizard.common.loggingServices import Logger


# MacOS platform
if sys.platform == "darwin":
    import lightblue

    BluetoothSocket = lightblue.socket
    BluetoothError = lightblue.BluetoothError
    RFCOMM = lightblue.RFCOMM

    def discoverDevices():
        devices = []
        foundDevices = lightblue.finddevices(getnames=True)
        for address, name, class_ in foundDevices:
            devices.append((address, name))
        return devices

# Windows platform
elif sys.platform == "win32":
    import bluetooth

    BluetoothSocket = bluetooth.BluetoothSocket
    BluetoothError = bluetooth.BluetoothError
    RFCOMM = bluetooth.RFCOMM

    def discoverDevices():
        return bluetooth.discover_devices(lookup_names=True)

# Linux platform
elif sys.platform == "linux2":
    import bluetooth

    BluetoothSocket = bluetooth.BluetoothSocket
    BluetoothError = bluetooth.BluetoothError
    RFCOMM = bluetooth.RFCOMM

    def discoverDevices():
        return bluetooth.discover_devices(lookup_names=True)

# Others
else:
    raise NotImplementedError("This platform (%s) does not support bluetooth transport" % sys.platform)


class BluetoothTransport(QtCore.QObject):
    """ Bluetooth transport class.
    """
    def __init__(self):
        """ Init object.
        """
        QtCore.QObject.__init__(self)
        
    def discoverDevices(self):
        """ Lookup for available devices.
        
        @return: availabe devices, as address/name pairs
        @rtype: list of tuple
        """
        devices = discoverDevices()
        Logger().debug("BluetoothTransport.discoverDevices(): devices=%s" % devices)
        return devices
