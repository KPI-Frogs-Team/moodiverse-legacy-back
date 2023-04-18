from src.sensitive import connection


def retrieve_user(user_id):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT id, username, first_name, last_name, email, birth_date, (SELECT name from sex WHERE id = sex_id) as sex from "user" WHERE id=%s;''', user_id)
        user = cursor.fetchone()
        cursor.close()
        return user

