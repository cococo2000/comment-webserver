import sqlite3

def query_comment_by_id(comment_id):
    try:
        db_connection = sqlite3.connect('../data/comments.db')
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM user_comments WHERE id = ?", (comment_id,))
        row = cursor.fetchone()
        if row:
            comment_id, parent_id, table_id, name, content = row
            print(f"ID: {comment_id}, Parent ID: {parent_id}, Table ID: {table_id}, Name: {name}, Content: {content}")
        else:
            print(f"No comment found with ID {comment_id}.")
        db_connection.close()
    except Exception as e:
        print(f'Error occurred while querying the comment: {str(e)}')

if __name__ == '__main__':
    comment_id = int(input("Enter the ID of the comment to query: "))
    query_comment_by_id(comment_id)
