import mysql.connector
from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)
user_id = ''
    
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    global user_id
    try:
        myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
        cur = myconn.cursor()
        #dbs = cur.execute("create table users(username varchar(20) not null, id int not null primary key, password varchar(50) not null)")
        #cur.execute("insert into users values ('Bob', 1, 'bobby'), ('Tom', 2, '123'),('Meg', 3, 'passwrd')")
                     
        if request.method == 'POST':
        
            query = "select user_identifier from user_table where user_name = '" + request.form['Username'] + "' and user_password = '" + request.form['Password'] + "'"
                
            cur.execute(query)
            useraccount = cur.fetchone()
            if useraccount:
                user_id = useraccount[0]
                return redirect(url_for('user_policies'))
            else: 
                return render_template('login_page.html', error='Invalid Credentials.')

            
        elif request.method == 'GET':
            return render_template('login_page.html', error='Welcome')
        
        return render_template('login_page.html', error='')
    
    except:
        myconn.rollback()
    myconn.close()

@app.route("/uploaded", methods = ['POST'])
def uploaded():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template('confirmupload.html', confirm="uploaded successfully")

@app.route("/logout", methods = ['POST'])
def login():
    return render_template('login_page.html', error="logged out")

@app.route('/policies', methods=['GET', 'POST'])
def user_policies(): # need to take the user number as an argument ...
    global user_id
    try:   
        print(user_id)
        myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
        cur = myconn.cursor()
        # just testing with user-1 so here we need to get the user number after user has logged in ... 
        cur.execute("select policy_name from policy_table where user_identifier = '" + str(user_id) + "'")    
        print(user_id)
        policies = cur.fetchall()  
        hey = []
        for c in policies:
            hey.append(c[0])
        hey = sorted(hey) # sort alphabetically ...
        #hey = sorted(hey, reverse=True) # sort reverse ...
        for i in hey:
            print(i)
        # get all the policies from the database belonging to this specific user and display it on the page ...
        if request.method == 'GET':
            return render_template('policies_page.html', policies=hey)
        
        return render_template('policies_page.html', policies='')
    
    except:
        myconn.rollback()
    myconn.close()



if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)