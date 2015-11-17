t=0
for b in 2400k 32k
do
    let "t+=1"
    command="ffmpeg -i video.mp4"
for j in $(seq 0 1)
do
    for i in $(seq 0 5)
    do
        let "mi=i+(6*j)"
        if [ "$mi" -gt 9 ]
        then
            break
        fi
        command+=" -vcodec libx264 -acodec copy -vf scale=640:360"
        command+=" -ss 00:0$j:"$i"0 -t 00:00:10 -b:v "$b" -bufsize 64k"
        command+=" videot"$t$mi".mp4"
    done
done
$command
done
exit
