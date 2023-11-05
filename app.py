# coding: utf-8

# Description: This is the main file for the Flask server.
# It contains the routes for the API endpoints.
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# allow CORS for all domains on all routes
CORS(app)

# connect to database
db_connection = sqlite3.connect('data/comments.db', check_same_thread=False)
cursor = db_connection.cursor()

# create table if not exists
cursor.execute(''' \
    CREATE TABLE IF NOT EXISTS user_comments ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        parent_id INTEGER, \
        name TEXT, \
        content TEXT \
    ) \
''')
db_connection.commit()

# add new user comment
@app.route('/submit-comment', methods=['POST'])
def receive_data():
    try:
        print("\nAdd new comment...")
        data = request.get_json()
        name = data['name']
        content = data['content']
        parent_id = data.get('parent_id', 0)
        # check if name and content are empty
        if not name or not content:
            print('Name and content cannot be empty')
            return jsonify({'error': 'Name and content cannot be empty'})
        print('Name: {name}'.format(name=name))
        print('Content: {content}'.format(content=content))
        print('Parent ID: {parent_id}'.format(parent_id=parent_id))
        cursor.execute("INSERT INTO user_comments (parent_id, name, content) VALUES (?, ?, ?)", (parent_id, name, content))
        db_connection.commit()
        comment_id = cursor.lastrowid
        print('Data received and stored successfully with ID: {id}'.format(id=comment_id))
        return jsonify({'id': comment_id, 
                        "name": name,
                        "content": content, 
                        "parent_id": parent_id,
                        'message': 'Data received and stored successfully'})
    except Exception as e:
        print('Error occurred while receiving data: "{error}"'.format(error=str(e)))
        return jsonify({'error': str(e)})

# query user comment by id
@app.route('/query-comment', methods=['GET'])
def query_comment():
    try:
        comment_id = request.args.get('id')
        print('\nQuerying comment with ID {id}...'.format(id=comment_id))
        cursor.execute("SELECT * FROM user_comments WHERE id = ?", (comment_id,))
        row = cursor.fetchone()
        if row:
            comment_id, parent_id, name, content = row
            # print(f"ID: {comment_id}, Parent ID: {parent_id}, Name: {name}, Content: {content}")
            return jsonify({'id': comment_id, 'parent_id': parent_id, 'name': name, 'content': content})
        else:
            print(f"No comment found with ID {comment_id}.")
            return jsonify({'message': f'No comment found with ID {comment_id}.'})
    except Exception as e:
        print(f'Error occurred while querying the comment: {str(e)}')
        return jsonify({'error': str(e)})

# query all user comments
@app.route('/query-comments', methods=['GET'])
def query_comments():
    try:
        print('\nQuerying all comments...')
        cursor.execute("SELECT * FROM user_comments")
        rows = cursor.fetchall()
        comments = []
        for row in rows:
            comment_id, parent_id, name, content = row
            print(f"ID: {comment_id}, Parent ID: {parent_id}, Name: {name}, Content: {content}")
            comments.append({'id': comment_id, 'parent_id': parent_id, 'name': name, 'content': content})
        return jsonify(comments)
    except Exception as e:
        print(f'Error occurred while querying the database: {str(e)}')
        return jsonify({'error': str(e)})

# delete user comment by id
@app.route('/delete-comment', methods=['DELETE'])
def delete_comment():
    try:
        comment_id = request.args.get('id')
        print('\nDeleting comment with ID {id}...'.format(id=comment_id))
        cursor.execute("DELETE FROM user_comments WHERE id = ?", (comment_id,))
        db_connection.commit()
        if cursor.rowcount > 0:
            print(f"Comment with ID {comment_id} has been deleted.")
            return jsonify({'message': f'Comment with ID {comment_id} has been deleted.'})
        else:
            print(f"No comment found with ID {comment_id}.")
            return jsonify({'message': f'No comment found with ID {comment_id}.'})
    except Exception as e:
        print(f'Error occurred while deleting the comment: {str(e)}')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
