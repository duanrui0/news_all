if __name__ == '__main__':
    with open('../shuju') as f:
        data = f.readlines()

        # 去除行尾的换行符
    data = [line.strip() for line in data]

    # 构造SQL语句
    sql = 'SELECT {} AS base_id UNION ALL '.format(data[0])
    for i in range(1, len(data)):
        sql += 'SELECT {} AS base_id UNION ALL '.format(data[i])

    print(sql)