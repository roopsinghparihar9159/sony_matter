#!/bin/bash

action=$1

session="aol-live"
if [[ "$action" == "stop"]]; then
	tmux kill-session -t ${session}
elif [[ "$action" == "start" ]]; then
	tmux kill-session -t ${session}
	tmux new-window -d -s ${session}
	
fi