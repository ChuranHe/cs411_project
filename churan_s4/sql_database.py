import pymysql as mdb

def connect():
    return mdb.connect(host="35.222.100.91",
                       port=3306,
                       user="root",
                       passwd="OwBs2jt9w5ol9tbA",
                       db="Project")

def create_user(email, username, password):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "INSERT INTO User (email, user_pwd, user_name) VALUES (%s, %s, %s);"
    try:
        cur.execute(sql,(email, password, username))
        db_rw.commit()
        return 0
    except Exception as e:
        return e.args[0]

def create_course(course_number, course_name, dept_name, course_GPA, credits):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "INSERT INTO Course (course_number, course_name, dept_name, course_GPA, credits) VALUES (%s, %s, %s, %s, %s);"
    try:
        cur.execute(sql,(course_number, course_name, dept_name, course_GPA, credits))
        db_rw.commit()
        return 0
    except Exception as e:
        return e.args[0]

def check_user(username, password):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "SELECT * FROM User WHERE user_name = %s AND user_pwd = %s"
    cur.execute(sql,(username, password))
    if cur.rowcount == 1:
        return True
    else:
        return False

def check_course(course_number):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "SELECT * FROM Course WHERE course_number = %s"
    cur.execute(sql,(course_number))
    if cur.rowcount == 1:
        return True
    else:
        return False

def update_user(user_name, newpassword):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "UPDATE User SET user_pwd = %s WHERE user_name = %s;"
    cur.execute(sql,(newpassword, user_name))
    db_rw.commit()

def update_course(course_number, course_GPA, credits):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "UPDATE Course SET course_GPA = %s, credits = %s WHERE course_number = %s;"
    cur.execute(sql,(course_GPA, credits, course_number))
    db_rw.commit()

def remove_user(user_name, password):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "DELETE FROM User WHERE user_name = %s AND user_pwd = %s;"
    cur.execute(sql,(user_name, password))
    db_rw.commit()

def remove_course(course_number):
    db_rw = connect()
    cur = db_rw.cursor()
    sql = "DELETE FROM Course WHERE course_number = %s;"
    cur.execute(sql,(course_number))
    db_rw.commit()

def show_all_user():
    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    sql = "SELECT user_id as id, email, user_pwd as password, user_name as username FROM User;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def show_all_course():
    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    sql = "SELECT * FROM Course;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def find_course_by_dept(course_number):
    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    sql = "SELECT * FROM Course WHERE dept_name = %s;"
    cur.execute(sql, (course_number))
    rows = cur.fetchall()
    return rows

def find_course_by_cn(course_number):
    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    sql = "SELECT * FROM Course WHERE course_number = %s;"
    cur.execute(sql, (course_number))
    rows = cur.fetchall()
    return rows

def stage_3_advquery(year, season):
    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    sql = "DROP VIEW IF EXISTS Course_A_rate;"
    cur.execute(sql)
    sql = "CREATE VIEW Course_A_rate AS\
    (SELECT s.course_number AS course_number, s.CRN as CRN, s.percentA AS A_rate, s.instr_name AS instr_name\
    FROM Section s WHERE s.year = %s AND s.semester = %s);"
    cur.execute(sql, (year, season))
    sql = "DROP VIEW IF EXISTS Instr_ratings;"
    cur.execute(sql)
    sql = "CREATE VIEW Instr_ratings AS\
    (SELECT ir.instr_name AS instr_name, ROUND(AVG(ir.ins_rate), 2) AS ins_rating\
    FROM Review ir GROUP BY ir.instr_name);"
    cur.execute(sql)
    sql = "DROP VIEW IF EXISTS Dept_avg_A_rate;"
    cur.execute(sql)
    sql = "CREATE VIEW Dept_avg_A_rate AS\
    (SELECT Course.dept_name as dept_name, ROUND(AVG(Course_A_rate.A_rate), 2) AS dept_avg_A_rate\
    FROM Course JOIN Course_A_rate USING(course_number)\
    WHERE course_number = Course_A_rate.course_number\
    GROUP BY Course.dept_name);"
    cur.execute(sql)
    sql = "SELECT Course_A_rate.course_number AS course_number, Course_A_rate.CRN as CRN, Course_A_rate.A_rate AS A_rate, Dept_avg_A_rate.dept_avg_A_rate AS avg_A_rate,\
        Course_A_rate.instr_name AS instr_name, Instr_ratings.ins_rating AS ins_rating\
    FROM Course_A_rate JOIN Course USING(course_number) JOIN Dept_avg_A_rate USING (dept_name) LEFT JOIN Instr_ratings USING(instr_name)\
    WHERE Course_A_rate.A_rate > Dept_avg_A_rate.dept_avg_A_rate\
    ORDER BY Course_A_rate.course_number ASC;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows