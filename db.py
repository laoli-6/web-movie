import pymysql


# 数据库连接函数
def get_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='test',
                           cursorclass=pymysql.cursors.DictCursor)


# 数据库插入操作
def insert(sql, params):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
        connection.commit()
    except pymysql.Error as e:
        print(f"Error during insert operation: {e}")
    finally:
        connection.close()


# 数据库查询操作
def ins(sql, params):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        connection.commit()
        return result
    except pymysql.Error as e:
        print(f"Error during select operation: {e}")
        return None
    finally:
        connection.close()

