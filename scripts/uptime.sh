#!/bin/bash
awk '{printf "%.0f\n", $1+1}' /proc/uptime
