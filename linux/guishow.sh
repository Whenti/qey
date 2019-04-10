#!/bin/bash

new_ids=`xdotool search --class terminator | cut -f 1`
new_id="${new_ids##*$'\n'}"
if [ "$new_id" == "" ] ; then
    terminator &
else
    xdotool windowminimize $new_id
fi