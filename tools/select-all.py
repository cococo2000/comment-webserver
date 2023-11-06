import sqlite3

def query_database():
    try:
        db_connection = sqlite3.connect('../data/comments.db')
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM user_comments")
        rows = cursor.fetchall()
        for row in rows:
            comment_id, parent_id, table_id, name, content = row
            print(f"ID: {comment_id}, Parent ID: {parent_id}, Table ID: {table_id}, Name: {name}, Content: {content}")
        db_connection.close()
    except Exception as e:
        print(f'Error occurred while querying the database: {str(e)}')

if __name__ == '__main__':
    query_database()
