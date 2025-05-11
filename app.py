from flask import Flask, render_template, request, redirect, url_for
import pymysql
from db import  ins,insert
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('login.html')
# 登录页面路由，渲染登录页面
@app.route('/login.html')
def login():
    return render_template('login.html')
# 登录路由，处理登录请求
@app.route('/login/api', methods=['POST'])
def login_api():
    ID = request.form.get('name')
    password = request.form.get('passwd')
    sql = "SELECT ID, password FROM user WHERE ID = %s"
    user_list = ins(sql, (ID,))
    if user_list is None or len(user_list) == 0:
        return "ID不存在！"
    else:
        user_id = user_list[0]['ID']  # 获取用户ID
        if password == user_list[0]['password']:
            return render_template('index.html', user_id=user_id)
        return "密码错误！"


#注册
@app.route('/register.html')
def register():
    return render_template('register.html')
# 注册路由，处理注册请求
@app.route('/register', methods=['POST'])
def register_api():
    ID = request.form.get('ID')
    password = request.form.get('passwd')
    yespassword = request.form.get('yespasswd')
    QQ = request.form.get('qq')
    Email = request.form.get('email')
    # 打印表单数据到控制台
    print(f"Received registration data: ID={ID}, password={password}, yespassword={yespassword}, QQ={QQ}, Email={Email}")
    if not all([ID, password, QQ, Email]):
        return "参数不完整！"
    elif password != yespassword:
        return "密码不一致！"
    sql = "INSERT INTO user (ID, password, QQ, Email) VALUES (%s, %s, %s, %s)"
    try:
        insert(sql, (ID, password, QQ, Email))
        return redirect(url_for('login'))
    except pymysql.err.IntegrityError:
        return 'ID重复！'
    return "注册成功"


#更改密码
@app.route('/forgetpasswd.html')
def change_password():
    return render_template('forgetpasswd.html')
# 处理更改密码表单提交的路由
@app.route('/forgetpasswd', methods=['POST'])
def forgetpasswd():
    ID = request.form.get('ID')
    QQ = request.form.get('QQ')
    Email = request.form.get('Email')
    new_password = request.form.get('new_password')
    yes_password = request.form.get('yes_password')
    if new_password != yes_password:
        return "密码不一致！"
    sql = "SELECT * FROM user WHERE ID = %s AND QQ = %s AND Email = %s"
    user_list = ins(sql, (ID, QQ, Email))
    if not user_list:
        return "用户信息不匹配！"
    update_sql = "UPDATE user SET password = %s WHERE ID = %s"
    insert(update_sql, (new_password, ID))
    # 成功更改密码后重定向到登录页面
    return redirect(url_for('login'))


# 假设这是删除账户的路由
@app.route('/delete_account.html')
def delete_account():
    return render_template('delete_account.html')


# 处理删除账户表单提交的路由
@app.route('/delete_account', methods=['POST'])
def perform_delete_account():
    ID = request.form.get('ID')
    password = request.form.get('password')

    # 检查账号和密码是否匹配
    sql = "SELECT * FROM user WHERE ID = %s AND password = %s"
    user_list = ins(sql, (ID, password))

    if user_list:
        # 账号和密码匹配，删除账户
        delete_sql = "DELETE FROM user WHERE ID = %s"
        insert(delete_sql, (ID,))
        return redirect(url_for('login'))
    else:
        # 账号和密码不匹配，显示错误消息
        return '账号或密码错误'

#关于我们
@app.route('/about')
def about():
    return render_template('about.html')
#关于我们
@app.route('/animation')
def animation():
    return render_template('animation.html')
#关于我们
@app.route('/movie')
def movie():
    return render_template('movie.html')
#关于我们
@app.route('/tvshow')
def tvshow():
    return render_template('tvshow.html')
#关于我们
@app.route('/variety')
def variety():
    return render_template('variety.html')
#关于我们
@app.route('/documentary')
def documentary():
    return render_template('documentary.html')

if __name__ == '__main__':
    app.run(debug=True)
