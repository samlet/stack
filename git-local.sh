#!/bin/bash
# git archive --format=tar --prefix=stack/ HEAD | gzip >/pi/archive/sagas-stack-0.1.tar.gz

rm /pi/archive/sagas/sagas-stack*
git archive --prefix=stack/ -o /pi/archive/sagas/sagas-stack-0.1.tar.gz HEAD
echo 'done.'
ls -alh /pi/archive/sagas/sagas-stack*


