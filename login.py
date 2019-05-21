from pymysqlpool.pool import Pool


class Login:
    def __init__(self,
                 user, password, host, db, port,
                 **kwargs):
        self.pool = Pool(user=user,
                         password=password,
                         host=host,
                         db=db,
                         port=port)
        self.pool.init()

    def login(self, user_name, password):
        cmd_str = """
SELECT PASSWORD('{password}') = password FROM TB_USER 
    WHERE user_id='{user_name}'
        """
        connection = self.pool.get_conn()
        cur = connection.cursor()
        cur.execute(cmd_str.format(password=password, user_name=user_name))
        result = list(cur.fetchone().values())[0]

        self.pool.release(connection)
        if result == 1:
            return True
        else:
            return False

if __name__ == '__main__':
    import sys
    import json

    with open(sys.argv[1]) as f:
        config = json.loads(f.read())
    l = Login(**config)
    res = l.login("hulk","password")
    print(res)
