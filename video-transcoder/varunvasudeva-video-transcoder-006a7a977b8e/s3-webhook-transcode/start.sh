#!/bin/bash

session="s3-webhook-transcoding"
tmux kill-session -t ${session}
tmux new-session -d -s ${session}
# cmd="while true; do python3 transcode.py; sleep 10; done"
# tmux send-keys -t ${session} "$cmd" C-m

tmux split-window -t ${session}:0.0 -h
tmux split-window -t ${session}:0.1 -h
tmux select-layout tiled
cmd="while true; do python3 transcode.py; sleep 10; done"
cmd1="while true; do python3 transcode.py; sleep 5; done"
# tmux send-keys -t ${session} "$cmd" C-m
tmux send-keys -t ${session}:0.0 "$cmd" C-m
sleep 2
tmux send-keys -t ${session}:0.1 "$cmd" C-m