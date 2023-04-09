import psycopg2

# Returns the connection (conn). Use conn.cursor() to execute SQL statements.
def connect(db_url = "postgresql://postgres:opendoor@localhost:5432/postgres"):
    conn = psycopg2.connect(db_url)
    return conn

def populate_database(cur):
    insert_statement = """
    INSERT INTO
        profiles(user_id, dorm, major, description) 
    VALUES
        ('test1', 'a', 'aa', 'aaa'),
        ('test2', 'b', 'bb', 'bbb'),
        ('test3', 'c', 'cc', 'ccc'),
        ('test4', 'd', 'dd', 'ddd'),
        ('test5', 'e', 'ee', 'eee')
    ON CONFLICT DO NOTHING
    RETURNING *;
    
    INSERT INTO
        users(user_id, password, profile)
    VALUES
        ('test1', 'aa', 'test1'),
        ('test2', 'bb', 'test2'),
        ('test3', 'cc', 'test3'),
        ('test4', 'dd', 'test4'),
        ('test5', 'ee', 'test5')
    ON CONFLICT DO NOTHING
    RETURNING *;
    
    INSERT INTO
        activities(activity_id, title, fee, reservation_needed, rsvp_list)
    VALUES
        (1, 'activity a', 0, false, ARRAY['test1', 'test2']),
        (2, 'activity b', 5, true, ARRAY['']),
        (3, 'activity c', 2000, false, ARRAY['test3'])
    ON CONFLICT DO NOTHING
    RETURNING *;
    """
    
    error_statement = """
    INSERT INTO
        users(user_id, password, profile)
    VALUES
        ('testerr', 'error', 'wrong')
    RETURNING *;
    """
    
    cur.execute(insert_statement)
    records = cur.fetchall()
    print(records)

def test_db():
    conn = connect()
    cur = conn.cursor()
    
    populate_database(cur)
    
    fetch_statement = """
    SELECT * FROM activities;
    """
    cur.execute(fetch_statement)
    records = cur.fetchall()
    print(records)

    conn.commit()
    conn.close()