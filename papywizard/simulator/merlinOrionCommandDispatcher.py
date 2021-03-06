# -*- coding: utf-8 -*-

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

Complete simulation of the Merlin/Orion head protocole.
This simulator can be use to check all low-level messages
between Papywizard and the head.

Implements
==========

- MerlinOrionCommandDispatcherObject
- MerlinOrionCommandDispatcher

@author: Frédéric Mantegazza
@copyright: (C) 2007-2011 Frédéric Mantegazza
@license: CeCILL
"""

__revision__ = "$Id: merlinOrionCommandDispatcher.py 2498 2011-04-17 07:51:23Z fma $"

from PyQt4 import QtCore

from papywizard.common.loggingServices import Logger
from papywizard.common.exception import HardwareError
from papywizard.plugins.simulationPlugins import SimulationAxis

ENCODER_ZERO = 0x800000
ENCODER_FULL_CIRCLE = 0xE62D3
SIDEREAL_RATE = 0x6f9  # "F90600"

merlinOrionCommandDispatcher = None


class MerlinOrionCommandDispatcherObject(QtCore.QObject):
    """ Abstract handler for Merlin/Orion commands set.
    """
    def __init__(self):
        """ Init the abstract handler.
        """
        QtCore.QObject.__init__(self)
        yawAxis = SimulationAxis('yawAxis', "Simulation")
        pitchAxis = SimulationAxis('pitchAxis', "Simulation")
        yawAxis.activate()
        pitchAxis.activate()
        self._axis = {1: yawAxis,
                      2: pitchAxis}
        self._axisCmd = {}
        self._axisDir = {}
        self._axisSpeed = {}
        self._axisPos = {}

    def activate(self):
        """ Activate threads.
        """
        self._axis[1].activate()
        self._axis[2].activate()

    def deactivate(self):
        """ Deactivate threads.
        """
        self._axis[1].deactivate()
        self._axis[2].deactivate()

    def _decodeAxisValue(self, strValue):
        """ Decode value from axis.

        Values (position, speed...) returned by axis are
        32bits-encoded strings, low byte first.

        @param strValue: value returned by axis
        @type strValue: str

        @return: value
        @rtype: int
        """
        value = 0
        for i in xrange(3):
            value += eval("0x%s" % strValue[i*2:i*2+2]) * 2 ** (i * 8)

        return value

    def _encodeAxisValue(self, value):
        """ Encode value for axis.

        Values (position, speed...) to send to axis must be
        32bits-encoded strings, low byte first.

        @param value: value
        @type value: int

        @return: value to send to axis
        @rtype: str
        """
        strHexValue = "000000%s" % hex(value)[2:]
        strValue = strHexValue[-2:] + strHexValue[-4:-2] + strHexValue[-6:-4]

        return strValue.upper()

    def _encoderToAngle(self, codPos):
        """ Convert encoder value to degres.

        @param codPos: encoder position
        @type codPos: int

        @return: position, in °
        @rtype: float
        """
        return (codPos - ENCODER_ZERO) * 360. / ENCODER_FULL_CIRCLE

    def _angleToEncoder(self, pos):
        """ Convert degres to encoder value.

        @param pos: position, in °
        @type pos: float

        @return: encoder position
        @rtype: int
        """
        return int(pos * ENCODER_FULL_CIRCLE / 360. + ENCODER_ZERO)

    def handleCmd(self, cmdStr):
        """ Handle a command.

        @param cmdStr: command to simulate
        @type cmdStr: str

        @return: response
        @rtype: str

        raise HardwareError: wrong command
        """
        Logger().debug("MerlinOrionBaseHandler.handleCmd(): cmdStr=%s" % cmdStr)
        if not cmdStr.startswith(':'):
            raise HardwareError("Invalid command format (%s)" % repr(cmdStr))

        # Split cmdStr
        cmd = cmdStr[1]
        numAxis = int(cmdStr[2])
        if numAxis not in (1, 2):
            raise HardwareError("Invalid axis number (%d)" % numAxis)
        param = cmdStr[3:-1]
        Logger().debug("MerlinOrionBaseHandler.handleCmd(): cmdStr=%s, cmd=%s, numAxis=%d, param=%s" % (repr(cmdStr), cmd, numAxis, param))

        # Compute command response
        response = ""

        # Stop command
        if cmd == 'L':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): stop")
            self._axis[numAxis].stop()
            response = ""

        # Check motor command
        elif cmd == 'F':
            Logger().trace("MerlinOrionBaseHandler.handleCmd(): ???")

        # Get encoder full circle command
        elif cmd == 'a':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): ???")
            response = self._encodeAxisValue(ENCODER_FULL_CIRCLE)

        # Get sidereal rate command
        elif cmd == 'D':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): ???")
            response = self._encodeAxisValue(SIDEREAL_RATE)

        # Get firmeware version command
        elif cmd == 'e':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): ???")
            response = "xxxxxx"

        # Read command
        elif cmd == 'j':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): read")
            pos = self._axis[numAxis].read()
            response = self._encodeAxisValue(self._angleToEncoder(pos))

        # Status command
        elif cmd == 'f':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): status")
            if self._axis[numAxis].isMoving():
                response = "-1-"
            else:
                response = "-0-"

        # Set action command
        elif cmd == 'G':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): set action")
            if param[0] == '0':
                self._axisCmd[numAxis] = 'drive'
            elif param[0] == '3':
                self._axisCmd[numAxis] = 'jog'
                if param[1] == '0':
                    self._axisDir[numAxis] = '+'
                elif param[1] == '1':
                    self._axisDir[numAxis] = '-'
                else:
                    raise HardwareError("Invalid param")
                Logger().debug("MerlinOrionBaseHandler.handleCmd(): axis %d direction=%s" % (numAxis, self._axisDir[numAxis]))
            else:
                raise NotImplementedError

        # Speed command
        elif cmd == 'I':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): speed")
            try:
                speed = self._decodeAxisValue(param)
                Logger().debug("MerlinOrionBaseHandler.handleCmd(): axis %d speed=%d" % (numAxis, speed))
                self._axisSpeed[numAxis] = speed
            except KeyError:
                raise HardwareError("No direction has been set")

        # Position command
        elif cmd == 'S':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): position")
            self._axisPos[numAxis] = self._encoderToAngle(self._decodeAxisValue(param))

        # Run command
        elif cmd == 'J':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): run")
            try:
                if self._axisCmd[numAxis] == 'jog':
                    dir_ = self._axisDir[numAxis]
                    speed = self._axisSpeed[numAxis]
                    self._axis[numAxis].startJog(dir_)
                elif self._axisCmd[numAxis] == 'drive':
                    pos = self._axisPos[numAxis]
                    self._axis[numAxis].drive(pos, wait=False)
            except KeyError:
                raise HardwareError("Missing one axis cmd/direction/speed value")

        # Shutter command
        elif cmd == 'O':
            Logger().debug("MerlinOrionBaseHandler.handleCmd(): shutter")

        # Invalid command
        else:
            raise HardwareError("Invalid command")

        return "=%s\r" % response


# Command dispatcher factory
def MerlinOrionCommandDispatcher(model=None):
    global merlinOrionCommandDispatcher
    if merlinOrionCommandDispatcher is None:
        merlinOrionCommandDispatcher = MerlinOrionCommandDispatcherObject()

    return merlinOrionCommandDispatcher
