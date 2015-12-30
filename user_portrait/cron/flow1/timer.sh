#!/bin/sh
cd /home/ubuntu8/yuankun/new_version/user_portrait/user_portrait/cron/flow1
tmux new-session -s work -d
tmux new_window -n redis -t work
tmux new-window -n es1 -t work
tmux new-window -n es2 -t work
tmux new-window -n es3 -t work
tmux new-window -n es4 -t work
tmux send-keys -t work:redis 'python send_uid.py' C-m
tmux send-keys -t work:es1 'python redis_to_es.py' C-m
tmux send-keys -t work:es2 'python redis_to_es.py' C-m
tmux send-keys -t work:es3 'python redis_to_es.py' C-m
tmux send-keys -t work:es4 'python redis_to_es.py' C-m

