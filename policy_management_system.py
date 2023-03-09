import mysql.connector
from Logic import DatabaseUser
from flask import Flask, redirect, render_template, url_for, request
obj = DatabaseUser("localhost","root","Neville123","test_schema")
# hello there comment
print("ok committing")
app = Flask(__name__)
user_id = ''
@app.route("/")
def form():
    return render_template("login_page.html")
@app.route('/data/', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        form_data = request.form
        password = form_data.get("Password")
        username = form_data.get("Username")
        if obj.isValidUser(username, password):
            return render_template('policies_page.html',form_data = form_data)
        else:
            return render_template('val.html', form_data = form_data)   


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