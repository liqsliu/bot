#!/bin/bash
(
cd ~/bot || exit 1
echo "wait ..."
# sleep 5
vgp
tgp
Tgp
bash init.sh || break

pkill -x mt
pkill -x toxbot
kill $(ps uax|grep gm_stream | grep -v grep | awk '{print $2}')

while true
do
python3 -m bot && {
  echo 'ok. stop ...'
  break
} || r=$?
echo "res: $r"
date
vgp && tgp
Tgpp
bash init.sh || break
(cd ~/ToxBot && make )|| exit 1

pkill -x mt
pkill -x toxbot
if [[ "$r" -eq 1 ]]; then
  # ctrl+C
  echo stop by me
  sleep 2
else
  echo "restart ..."
  echo "wait ..."
  sleep 5
fi
done
)
