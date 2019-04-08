#!/bin/bash

curr_id=`xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2`
curr_class=`xprop -id $curr_id WM_CLASS | cut -f 4 -d " "`

if [ "$curr_class" = "\"Terminator\"" ] ; then
    xdotool windowminimize $curr_id
else 
    new_ids=`xdotool search --class terminator | cut -f 1`
    new_id=${new_ids##*$'\n'}
    if [ -n "$new_id" ] ; then
	xdotool windowactivate $new_id
    else
	terminator &
    fi      
fi
