#this file is for dividing videos into frames.
#!/bin/bash

$cmd=""
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo $line
    IFS='-' read -ra tmp<<<"$line"
    l1=`expr ${tmp[1]} - 20`
    l2=`expr ${tmp[0]} - ${tmp[1]} + 40`
    echo ${l1}
    cmd="$cmd && sudo ffmpeg -ss ${l1} -i {$2} -t ${l2} -vf fps=1 {$3}/${l1}_%d.jpg"   
done < "$1"
cmd=${cmd:3}
echo $cmd




