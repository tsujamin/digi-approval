#!/bin/sh
cd `dirname $0`/../..
scl enable python27 "bash --rcfile src/dev/$1"
