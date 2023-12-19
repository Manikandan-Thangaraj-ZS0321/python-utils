#!/usr/bin/python
import psycopg2

db_name = "zio_pipeline_ui"
db_server_user = "postgres"
db_server_pass = "xk56iIUYV1eihMke7W0gbnfnl4gBkArsF26kttM96R8utWA4hJ"
db_server_host = "intics.db"
db_server_port = 5432


def getCoproConfig():
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
        cur.close()

        return CONFIG

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if conn is not None:
            conn.close()


def getCommonConfig():
    conn = None
    try:
        conn = psycopg2.connect(database=db_name,
                                user=db_server_user,
                                password=db_server_pass,
                                host=db_server_host,
                                port=db_server_port)
        cur = conn.cursor()

        cur.execute("SELECT variable, value FROM config.spw_common_config")
        rows = cur.fetchall()
        CONFIG = dict((x, y) for x, y in rows)
        cur.close()

        return CONFIG

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    copro_config = getCommonConfig()
    print(copro_config)
