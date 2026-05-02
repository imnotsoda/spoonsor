import psycopg2
import psycopg2.extras
import os

#PostgreSQL credentials
#NOTE: On the EC2 server, these are replaced with env variables to avoid hardcoding
DB_CONFIG = {
    "host":     "localhost",
    "database": "fundraising_db",
    "user":     "hyunjicho",
    "password": "",
    "port":     5432
}

#opens a connection to the db using the config/credentials above ^
def get_connection():
    return psycopg2.connect(**DB_CONFIG) 
    #the "**" unpacks the dictionary 
    # so it's like calling psycopg2.connect("host"=..., "database"=..., ...)

#for the SELECT queries (when we read data)
def query(sql, params=None, fetchall=True):
    """
    Run a SELECT query and return results as a list of dicts.
    Uses parameterized queries to prevent SQL injection.
    """
    conn = get_connection() #open db connection
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            #arg: RealDicCursor -> returns results as dicts, which r easier to display w frontend

            cur.execute(sql, params)
            #CORE FEATURE ^ 
            # passes params separately, instead of directly concatenating string
            # -> prevents SQL injection
            return cur.fetchall() if fetchall else cur.fetchone()
    finally:
        conn.close()

#for INSERT, UPDATE, DELETE (when we write data)
def execute(sql, params=None):
    """
    Run an INSERT, UPDATE, or DELETE and commit.
    Uses parameterized queries to prevent SQL injection.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)

        conn.commit() 
        # without this, changes r only temporary and r rolled back when connection closes
    finally:
        conn.close()

#when running multiple operations at once (to ensure atomicity)
def execute_transaction(statements):
    """
    Run multiple SQL statements as a single atomic transaction.
    If any statement fails, all changes are rolled back.
    Uses PostgreSQL's default READ COMMITTED isolation level.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for sql, params in statements:
                cur.execute(sql, params)
        conn.commit()
    except Exception as e:
        conn.rollback() #if anything fails mid-transaction, 
                        # rollback & undo everything back
                        # to the start to ensure consistency
        raise e
    finally:
        conn.close()