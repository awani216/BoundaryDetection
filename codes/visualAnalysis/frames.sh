#!/bin/bash
$cmd=""
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo $line
    IFS='-' read -ra tmp<<<"$line"
    l1=`expr ${tmp[0]} - 20`
    l2=`expr ${tmp[1]} - 20`
    echo ${l1}
    cmd="$cmd && sudo ffmpeg -ss ${l1} -i v2.mp4 -t 40 -vf fps=1 generated2/${l1}_%d.jpg" 
    cmd="$cmd && sudo ffmpeg -ss ${l2} -i v2.mp4 -t 40 -vf fps=1 generated2/${l2}_%d.jpg"  
done < "$1"
cmd=${cmd:3}
echo $cmd




