#!/bin/bash
base="/home/transcoder/video-transcoder"
session="transcoding-procress"

cd $base
tmux kill-window -t ${session}
tmux new-session -d -s ${session}
tmux split-window -t ${session} -v
tmux split-window -t ${session}:0.1 -v
tmux split-window -t ${session}:0.0 -h
tmux split-window -t ${session}:0.1 -h
tmux split-window -t ${session}:0.3 -h
tmux split-window -t ${session}:0.4 -h
tmux split-window -t ${session}:0.6 -h
tmux split-window -t ${session}:0.7 -h
tmux select-layout tiled

cmd0="cd vod-qc; while true; do python3 vod-qc.py; sleep 3; done"
cmd1="cd vod-qc; while true; do python3 vod-qc.py; sleep 5; done"
cmd2="cd vod-qc; while true; do python3 vod-qc.py; sleep 7; done"
tmux send-keys -t ${session}:0.0 "$cmd0" C-m
sleep 4
tmux send-keys -t ${session}:0.1 "$cmd1" C-m
#sleep 7
#tmux send-keys -t ${session}:0.2 "$cmd2" C-m


cmd3="cd vod-transcoder; while true; do python3.8 vod-transcoder.py 0;sleep 3; done"
cmd4="cd vod-transcoder; while true; do python3.8 vod-transcoder.py 1;sleep 5; done"
cmd5="cd vod-transcoder; while true; do python3.8 vod-transcoder.py 2;sleep 7; done"
tmux send-keys -t ${session}:0.3 "$cmd3" C-m
sleep 4
tmux send-keys -t ${session}:0.4 "$cmd4" C-m
sleep 7
tmux send-keys -t ${session}:0.5 "$cmd5" C-m

cmd6="cd sprite_gen; while true; do python3.8 sprite_gen.py 2;sleep 1; done"
tmux send-keys -t ${session}:0.6 "$cmd6" C-m

#cmd7="cd vod-transcoder;while true; do bash getPercent.sh; sleep 1; done"
#tmux send-keys -t ${session}:0.7 "$cmd7" C-m

