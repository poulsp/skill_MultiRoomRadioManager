#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

cd $DIR/../

#Find process id pid and kill
#PID=`ps ax|grep  "node.*bin/www"|grep -v "grep"|awk '{print $1}'`
#echo $"$PID"
#kill -2 $(ps ax|grep  "node.*bin/www"|grep -v "grep"|awk '{print $1}') > /dev/null 2>&1

