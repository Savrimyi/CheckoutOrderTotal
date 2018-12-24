#!/bin/sh

python3.7 RunCheckoutAPI.py run  &

python3.7 RunCheckoutAPI.py test

pkill RunCheckoutAPI.py
