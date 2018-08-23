#!/bin/bash
### BEGIN INIT INFO
# Provides:          blabla
# Required-Start:    $syslog
# Required-Stop:     $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: It runs the relay server
# Description: It runs the relay server
#
### END INIT INFO

while true
do
   python light.py
done