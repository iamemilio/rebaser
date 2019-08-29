#!/bin/bash

oc create configmap script --from-file=rebaser.py=rebaser.py

