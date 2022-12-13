#!/bin/bash

./bin/dlv2-float --mode=idlv $1 $2 | ./bin/clingo --mode=clasp
