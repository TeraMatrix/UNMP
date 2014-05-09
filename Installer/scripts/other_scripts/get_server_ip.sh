#echo `ifconfig  | grep 'eth0' | tr -s ' ' | cut -d ' ' -f5`

echo `/sbin/ifconfig \
       | grep '\<inet\>' \
       | sed -n '1p' \
       | tr -s ' ' \
       | cut -d ' ' -f3 \
       | cut -d ':' -f2`
