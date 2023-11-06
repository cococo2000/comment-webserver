# Simple Comment Web Server

This is a simple web server that allows users to post comments. It is written in Python and uses the Flask framework.
The server stores the comments in a SQLite database. The database file is `comments.db`. It is located in the `data` folder.

## Before you start

You will need to install the following:
```bash
sudo apt-get install libsqlite3-dev

pip3 install -r requirements.txt
```

## Test the server

- Start the server
  - To start the server, run the following command:
	```bash
	./start-app.sh
	```
  - In `start-app.sh`, you can change the port number and the host name. The default port number is 5000 and the default host name is `127.0.0.1`. 
  - `-w` parameter is used to specify the number of workers. The default number of workers is 4.

- Stop the server
  - Press `Ctrl+C` to stop the server.

## Deploy the server

To use the system service manager (such as systemd) to manage a Gunicorn process and ensure it runs continuously on your server, you can follow these steps:

- Edit the content of `comment-webserver.service`
  - Description: A description of the service.
  - User and Group: The user and group under which the service should run.
  - WorkingDirectory: The root directory of your Comment Web Server.
  - ExecStart: The command to start the Gunicorn process.
  - Restart: Specifies when the service should be restarted. "always" means it will automatically restart whenever it exits.
- Copy `comment-webserver.service` to `/etc/systemd/system`
```bash
sudo cp comment-webserver.service /etc/systemd/system
```
- Enable and start the service 
```bash
sudo systemctl enable comment-webserver.service
sudo systemctl start comment-webserver.service
```
Or reload the service if you have made any changes to the service file
```bash
sudo systemctl daemon-reload
```
- Manage the service
  - Check the status of the service
  ```bash
  sudo systemctl status comment-webserver.service
  ```
  - Stop the service
  ```bash
  sudo systemctl stop comment-webserver.service
  ```
  - Restart the service
  ```bash
  sudo systemctl restart comment-webserver.service
  ```
  - Disable the service
  ```bash
  sudo systemctl disable comment-webserver.service
  ```

## Example

`index.html` is a simple web page that allows users to test the server. It is located in the `templates` folder.

In the web page, users can enter their name and a comment. When they click the `Submit` button, the comment will be posted to the server.

## Tools

In the `tools` folder, there are serveral Python scripts: 
- `delete.py`: delete one comment from the database by id
- `select-1.py`: select one comment from the database by id
- `select-all.py`: select all comments from the database


## Appendix

### Configuring Apache2 as a Reverse Proxy

- Add ProxyPass and ProxyPassReverse to the VirtualHost configuration file (`/etc/apache2/sites-available/default-ssl.conf`)
```
        <VirtualHost 172.31.19.160:443>
                ServerName www.example.com
                ServerAlias example.com
                ServerAdmin webmaster@localhost
                DocumentRoot /var/www/html

                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined

                SSLEngine on
                SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
                SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

                SSLProxyEngine on
                SSLProxyVerify none
                SSLProxyCheckPeerCN off
                SSLProxyCheckPeerName off

                <Location /comment>
                        ProxyPass https://localhost:5000/
                        ProxyPassReverse https://localhost:5000/
                </Location>
        </VirtualHost>
```

- Enable the proxy modules
```
sudo a2enmod proxy
sudo a2enmod proxy_http
```

- Restart Apache2
```
sudo systemctl restart apache2
```

### Some Bugs

These bugs are found in `/var/log/apache2/error.log` during the test of the server.

  - `SSL Proxy requested for evaluation.benchcouncil.org:443 but not enabled [Hint: SSLProxyEngine]`
    - Solution: add `SSLProxyEngine on` to the VirtualHost configuration file

  - `Error during SSL Handshake with remote server returned by /comment/query-comments` 
    - Solution: add `SSLProxyVerify none` (`SSLProxyCheckPeerCN off` and `SSLProxyCheckPeerName off`) to the VirtualHost configuration file

