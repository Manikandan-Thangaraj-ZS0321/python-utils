#!/usr/bin/python
import psycopg2
import gc

db_name = "zio_pipeline_ui_local"
db_server_user = "postgres"
db_server_pass = "password"
db_server_host = "intics.db"
db_server_port = 5432


def get__copro__config():
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
        config = dict((x, y) for x, y in rows)
        cur.close()
        return config
    except psycopg2.Error as error:
        raise error
    except Exception as exception:
        return exception
    finally:
        gc.collect()
        if conn is not None:
            conn.close()


def get__common__config():
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
        config = dict((x, y) for x, y in rows)
        cur.close()
        return config
    except psycopg2.Error as error:
        raise error
    except Exception as exception:
        return exception
    finally:
        gc.collect()
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    copro_config = get__common__config()
    print(copro_config)
