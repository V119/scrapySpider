class SqlUtils:
    @staticmethod
    def generate_insert_sql(item):
        tb_name = 'news'

        sql = 'INSERT INTO ' + tb_name + ' ('
        tb_fields = ''
        tb_values = ''
        for tb_f in item:
            tb_fields = tb_fields + tb_f + ', '
            tb_values = tb_values + '"' + str(item[tb_f]) + '", '

        return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'
