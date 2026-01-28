
import pymysql
from ssqatest.src.helpers.config_helpers import get_database_credentials
from ssqatest.src.configs.generic_configs import GenericConfigs


def read_from_db(sql):
    db_creds = get_database_credentials()
    connection = None

    try:
        # connect to database
        # Use the database name from credentials (from .env or GenericConfigs fallback)
        db_name = db_creds['db_name']
        print(f"🔍 Executing SQL query: {sql}")
        connection = pymysql.connect(
            host=db_creds['db_host'],
            port=db_creds['db_port'],
            user=db_creds['db_user'],
            password=db_creds['db_password'],
            database=db_name
        )

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        db_data = cursor.fetchall()
        cursor.close()
        return db_data

    finally:
        if connection:
            connection.close()


def get_order_from_db_by_order_no(order_no):

    # Get database name from credentials (from .env or GenericConfigs fallback)
    db_creds = get_database_credentials()
    schema = db_creds['db_name']
    table_prefix = GenericConfigs.DATABASE_TABLE_PREFIX

    sql = f"SELECT * FROM {schema}.{table_prefix}posts WHERE ID = {order_no} AND post_type = 'shop_order_placehold';"
    db_order = read_from_db(sql)

    return db_order










