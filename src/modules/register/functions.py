from src.sensitive import connection


def check_email_and_username(email, username):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT EXISTS (SELECT 1 FROM "user" WHERE email = %s OR username = %s);''', (email, username))
        is_exists = cursor.fetchone()[0]

        return is_exists


def add_user_into_db(username, email, hashed_password, birthdate):
    with connection.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO "user" (username, email, password, birth_date, sex_id) VALUES (%s, %s, %s, %s, NULL);''',
            (username, email, hashed_password, birthdate))
        connection.commit()
