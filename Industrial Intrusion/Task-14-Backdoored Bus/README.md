TryHackMe room Backdoored Bus
YouTube video walk through: https://youtu.be/a3vEOOaPqDw

Commnads used on the video:

tar -xf modbus-container-final-xxxx.tar

mkdir -p extracted_layers
jq -r '.[0].Layers[]' manifest.json | while read layer; do
  tar -xf $layer -C extracted_layers/
done

jq -r '.[0].Layers[]' manifest.json | while read layer_tar; do
  echo "Extracting $layer_tar …"
  tar -xf "$layer_tar" -C extracted_layers
done


grep -R -n "curl" extracted_layers/usr/local/lib/python*

sudo docker load -i modbus-container-final-1750975076803.tar

sudo docker images
 
sudo docker inspect <IMAGE_ID>

sudo docker history <IMAGE_ID> --no-trunc

mkdir layers && cd layers

sudo bash -c '
for L in $(docker history --format "{{.ID}}" <IMAGE_ID>| grep -v "<missing>"); do
    mkdir -p "layer_$L"
    docker save "$L" | tar -xf - -C "layer_$L"
    tar -xf "layer_$L/layer.tar" -C "layer_$L" 2>/dev/null
done'

exec()
 subprocess.Popen()
pickle.load() (deserialization attacks)

grep -R -n -E --color=always \
  "eval\(|os\.system\(|subprocess\.Popen\(|exec\(|pickle\.load\(|curl|wget|bash -c|sh -c" \
  . 2>/dev/null
  
  /usr/local/lib/python*
  
           CTF,DockerSecurity,Modbus,CyberSecurity,THM,TryHackMe,CTFWalkthrough,PythonSecurity,Backdoor,StaticAnalysis,CyberSec,HackingChallenge,DockerForensics,OSCommandInjection,InfoSec
