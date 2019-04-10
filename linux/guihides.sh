#!/bin/bash

new_ids=`xdotool search --class terminator | cut -f 1`
new_id="${new_ids##*$'\n'}"

xdotool windowminimize $new_id
