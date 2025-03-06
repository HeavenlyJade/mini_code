import json

import pymysql


class MySQLDatabase:
    def __init__(self):
        # DEV_DATABASE_URL=mysql+pymysql://root:Ikasinfo123@192.168.11.223:3306/backend?charset=utf8mb4
        # DEV_DATABASE_URL=mysql+pymysql://root:root@192.168.10.163:3308/backend_user_client?charset=utf8mb4
        self.host = "192.168.10.163"
        self.port = 3308
        self.user = "root"
        self.password = "root"
        self.database = "backend"
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def query(self, sql, params=None):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()


def change_bool(filed: str):
    if not filed:
        return filed
    if filed.lower() == "true":
        return True
    elif filed.lower() == "false":
        return False
    else:
        return filed


class ParameterChange:

    def __init__(self):
        self.db_client = MySQLDatabase()

    def mian(self):
        sql1 = """ SELECT * FROM params_log LIMIT  0,1000 """
        data = self.db_client.query(sql1)
        for i in data:
            param_log_uuid = i["param_log_uuid"]
            sql2 = f""" SELECT * FROM params_attribute_log WHERE param_log_uuid ="{param_log_uuid}"  """
            sql_data2 = self.db_client.query(sql2)
            context_content = {}
            parameter_content = {}
            # print(sql_data2)
            for sql_dict in sql_data2:
                attribute_type = sql_dict["attribute_type"]
                attribute_name = sql_dict["attribute_name"]
                value = sql_dict["value"]
                try:
                    value = json.loads(value)
                except:
                    pass
                try:
                    value = float(value)
                except:
                    pass
                try:
                    value = change_bool(value)
                except:
                    pass
                if attribute_type == "context":
                    context_content[attribute_name] = value
                elif attribute_type == "parameter":
                    parameter_content[attribute_name] = value
            context_content_json = json.dumps(context_content)
            parameter_content_json = json.dumps(parameter_content)
            update_sql = f""" UPDATE  params_log set  context_content= '{context_content_json}',parameter_content='{parameter_content_json}'
             WHERE param_log_uuid ='{param_log_uuid}' """
            self.db_client.execute(update_sql)


if __name__ == '__main__':
    ParameterChange().mian()
