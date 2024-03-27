import mysql.connector

# 建立与数据库的连接
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senlife@123",
    database="scrapy_school"
)

# 创建一个游标对象
mycursor = mydb.cursor()

# 插入数据的SQL语句
sql = "INSERT INTO schools (name, province_id, city_id, article_title, content, publish_date, article_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# 示例数据
school_data = [
    ("School A", 1, 101, "Article 1", "Content 1", "2024-01-01", "http://example.com/article1"),
    ("School B", 2, 102, "Article 2", "Content 2", "2024-01-02", "http://example.com/article2"),
    # 其他学校数据
]

# 执行插入操作
mycursor.executemany(sql, school_data)

# 提交事务
mydb.commit()

# 输出插入的行数
print(mycursor.rowcount, "record(s) inserted.")
