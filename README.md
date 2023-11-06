# Simple Comment Web Server

This is a simple web server that allows users to post comments. It is written in Python and uses the Flask framework.
The server stores the comments in a SQLite database. The database file is `comments.db`. It is located in the `data` folder.

## Before you start

You will need to install the following:
```bash
sudo apt-get install libsqlite3-dev

pip3 install -r requirements.txt
```

## Start the server

To start the server, run the following command:
```bash
./start-app.sh
```

In `start-app.sh`, you can change the port number and the host name. The default port number is 5000 and the default host name is `127.0.0.1`. 
And `-w` parameter is used to specify the number of workers. The default number of workers is 4.

## Stop the server

Press `Ctrl+C` to stop the server.

## Example

`index.html` is a simple web page that allows users to test the server. It is located in the `templates` folder.

In the web page, users can enter their name and a comment. When they click the `Submit` button, the comment will be posted to the server.

## Other Tools

In the `tools` folder, there are serveral Python scripts: 
- `delete.py`: delete one comment from the database by id
- `select-1.py`: select one comment from the database by id
- `select-all.py`: select all comments from the database
