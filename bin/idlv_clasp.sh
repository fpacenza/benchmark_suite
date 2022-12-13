#!/bin/bash

./bin/dlv2 --mode=idlv $1 $2 | ./bin/clingo --mode=clasp
