#! /bin/bash

rsync -P -av -e ssh m31-01:/home/kouseki.miyo/kagra-gif/airEnvironmentMonitor/measurementA/*.gwf ./
