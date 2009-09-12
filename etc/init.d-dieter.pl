#!/bin/bash

PID_FILE=/var/run/dieter.pl.pid
PORT=10000
PROJECT_ROOT=/var/www/dieter

case $1 in
    start)
        cd  $PROJECT_ROOT
        exec sudo -u django python2.5 manage.py runfcgi host=127.0.0.1 port=$PORT pidfile=$PID_FILE daemonize=false maxrequests=100 maxchildren=10 &
        ;;
    stop)
        kill `cat $PID_FILE` ;;
    restart)
        kill `cat $PID_FILE`
        cd  $PROJECT_ROOT
        exec sudo -u django python2.5 manage.py runfcgi host=127.0.0.1 port=$PORT pidfile=$PID_FILE daemonize=false maxrequests=100 maxchildren=10 &
        ;;
    *)
        echo "usage: dieter-django {start|stop}" ;;
esac
exit 0
