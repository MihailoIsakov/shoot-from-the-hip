#! /bin/bash
THEANO_FLAGS=mode=FAST_RUN,device=gpu0,floatX=float32 jupyter notebook

