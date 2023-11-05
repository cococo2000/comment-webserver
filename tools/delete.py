import sqlite3

def delete_comment_by_id(comment_id):
    try:
        db_connection = sqlite3.connect('../data/comments.db')
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM user_comments WHERE id = ?", (comment_id,))
        db_connection.commit()
        if cursor.rowcount > 0:
            print(f"Comment with ID {comment_id} has been deleted.")
        else:
            print(f"No comment found with ID {comment_id}.")
        db_connection.close()
    except Exception as e:
        print(f'Error occurred while deleting the comment: {str(e)}')

if __name__ == '__main__':
    comment_id = int(input("Enter the ID of the comment to delete: "))
    delete_comment_by_id(comment_id)
