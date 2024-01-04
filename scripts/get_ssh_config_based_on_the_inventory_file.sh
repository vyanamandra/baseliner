#!/bin/sh 
cat inventory/hosts | grep ansible_host= | cut -f 1,2,5 -d ' ' | while read l; 
do 
  n=$(echo $l | awk '{print $1}'); 
  i=$(echo $l | cut -f 2 -d '=' | cut -f 1 -d ' '); 
  k=$(echo $l | cut -f 3 -d '='); 
  echo "Host $n\n  Hostname $i\n  User ubuntu\n  Port 22\n  IdentityFile ${k}\n\n"; 
done
