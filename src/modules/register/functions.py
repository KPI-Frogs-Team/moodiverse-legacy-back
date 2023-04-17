from src.sensitive import connection


def check_email_and_username(email, username):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT EXISTS (SELECT 1 FROM "user" WHERE email = %s OR username = %s);''', (email, username))
        is_exists = cursor.fetchone()[0]

        return is_exists
