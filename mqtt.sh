#!/bin/bash
mosquitto_pub -L mqtt://test.mosquitto.org:1883/wtfipfs -m "$*"
