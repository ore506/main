# Python-Webapp
Tutorial on making a Webapp using Python, Flask, and mySQL. Tutorial at https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972 
#   m a i n 
 
pip install Flask
pip install -U googlemaps  
export FLASK_APP=application.py

flask run --port=3000 --host=127.0.0.2

--------------------------------------
------------AWS Set Up-----------
EC2  for flask
create ec2 
Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-0e472ba40eb589f49 (64-bit x86) / ami-0a940cb939351ccca (64-bit Arm)

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install -U pip virtualenv
pip3 install -U pip flask
sudo apt install virtualenv
sudo apt install python-pip
pip install flask


sudo apt install python3-flask
sudo apt install gunicorn
sudo apt install nginx
sudo apt install git
sudo apt install nano

copy all the project to the Folder


pip freeze >requierments.txt
virtualenv flask

$source ./bin/activate
Install python module again

$pip install "module"

------
set FLASK_APP=application.py
export FLASK_APP=application.py
set UPLOAD_FOLDER=/home
export UPLOAD_FOLDER=/home
flask run

sudo apt install python3-flask


(Need to add inboud rule for EC2 to accept TCP  port 5000 for 0.0.0.0/0)

 flask run --host 0.0.0.0 --port 5000

curl 0.0.0.0:80

sudo service nginx stop

