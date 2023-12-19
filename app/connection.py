#!/usr/bin/python
import psycopg2
import configparser
from app.src.util.loggers import *


def connect():
    conn = None
    try:
        conn = psycopg2.connect(database=db_name,
                                user=db_server_user,
                                password=db_server_pass,
                                host=db_server_host,
                                port=db_server_port)
        cur = conn.cursor()

        cur.execute("SELECT variable, value FROM config.copro_config")
        rows = cur.fetchall()
        CONFIG = dict((x, y) for x, y in rows)
        cur.execute('SELECT version()')
        cur.close()

        return CONFIG

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Exception occurred while database connection {}".format(error))
        return error

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    copro_config = connect()
    print(copro_config)
