# Create EC2 instance
1. Use ubuntu ec2 instance
2. connect to ec2 instance with ssh

## Update and clone the github repo
1. sudo apt update 
2. sudo apt install python3-venv python3-dev libpq-dev nginx curl
3. mkdir django-project
4. cd django-project/
5. git clone https://github.com/ubaid-shah/django-ekart.git


## Creating a Python Virtual Environment for your Project
1. python3 -m venv venv
2. source venv/bin/activate
3. sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
4. pip3 install -r req.txt

## In settings.py change  'ALLOWED_HOSTS = ['*']'

## Creating systemd Socket and Service Files for Gunicorn
1. sudo nano /etc/systemd/system/gunicorn.socket
2. copy and paste follwoing lines 

`[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target`

3. sudo nano /etc/systemd/system/gunicorn.service
4. copy and paste follwoing lines 

`
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django-project/django-ekart/ecommerce
ExecStart=/home/ubuntu/django-project/django-ekart/ecommerce/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target
`


5. You can now start and enable the Gunicorn socket. This will create the socket file at /run/gunicorn.sock now and at boot. When a connection is made to that socket, systemd will automatically start the gunicorn.service to handle it:

`sudo systemctl start gunicorn.socket`
`sudo systemctl enable gunicorn.socket`


6. Checking for the Gunicorn Socket File
`sudo systemctl status gunicorn.socket`

7. Next, check for the existence of the gunicorn.sock file within the /run directory:
`file /run/gunicorn.sock`

8. If the systemctl status command indicated that an error occurred or if you do not find the gunicorn.sock file in the directory, it’s an indication that the Gunicorn socket was not able to be created correctly. Check the Gunicorn socket’s logs by typing:

`sudo journalctl -u gunicorn.socket`

##  Testing Socket Activation
1. Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:
`sudo systemctl status gunicorn`

2. To test the socket activation mechanism, you can send a connection to the socket through curl by typing:
`curl --unix-socket /run/gunicorn.sock localhost`

3. You should receive the HTML output from your application in the terminal. This indicates that Gunicorn was started and was able to serve your Django application. You can verify that the Gunicorn service is running by typing:

`sudo systemctl status gunicorn`


4. If the output from curl or the output of systemctl status indicates that a problem occurred, check the logs for additional details:

`sudo journalctl -u gunicorn`

5. Check your /etc/systemd/system/gunicorn.service file for problems. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:

`sudo systemctl daemon-reload`
`sudo systemctl restart gunicorn`


## Configure Nginx to Proxy Pass to Gunicorn

Now that Gunicorn is set up, you need to configure Nginx to pass traffic to the process.

Start by creating and opening a new server block in Nginx’s sites-available directory:

`sudo nano /etc/nginx/sites-available/myproject`


edit the following

`
server {
    listen 80;
    server_name 18.232.106.76;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
`


Inside, open up a new server block. You will start by specifying that this block should listen on the normal port 80 and that it should respond to your server’s domain name or IP address:

Save and close the file when you are finished. Now, you can enable the file by linking it to the sites-enabled directory:

`sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled`


