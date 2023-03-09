import mysql.connector
from flask import Flask, redirect, render_template, url_for, request
from datetime import date
app = Flask(__name__)
user_id = ''

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')

    
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    global user_id
    try:
        myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
        cur = myconn.cursor()
         
        if request.method == 'POST':
        
            query = "select user_identifier from user_table where binary user_name = '" + request.form['username'] + "' and binary user_password = '" + request.form['password'] + "'"
            
            cur.execute(query)

            useraccount = cur.fetchone()
            
            if useraccount:
                print(useraccount[0])
                user_id = useraccount[0]
                return redirect(url_for('user_policies'))
            else: 
                return render_template('login_page.html')

    
    except:
        myconn.rollback()
    myconn.close()
 

@app.route("/logging_out", methods = ['POST'])
def logging_out():
    return redirect(url_for('login'))






@app.route("/policies", methods = ['POST'])
def policies():
    return redirect(url_for('user_policies'))

@app.route('/yourpolicies', methods=['GET', 'POST'])
def user_policies(): 
    global user_id # get the user identifier ...
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
        cur = myconn.cursor()
         
        cur.execute("select policy_name from policy_table where user_identifier = '" + str(user_id) + "'")    

        policies = cur.fetchall()
        
        # uncomment this when we are doing sorting / organizing the policies ...  

        #policy_list = []
        #for p in policies:
        #    policy_list.append(p[0])
        
        # get the name, amount paid and date started for each policy belonging to the user ...
        cur.execute("select policy_name, round(amount_paid,2), date_acquired from policy_table where user_identifier = '"+str(user_id)+"'")
        pol = cur.fetchall()

        # we can do a sorting method here ...
        
        # user wants to sort in alphabetical order ...
        # policy_list = sorted(policy_list, reverse=True) 
        
        # elif they want the reverse ...
        # policy_list = sorted(policy_list) 
        
        # get all the policies from the database belonging to this specific user and display it on the page ...
        if request.method == 'GET':
            return render_template('policies_page.html', policies=pol)
        
        return render_template('policies_page.html', policies='')
    
    except:
        myconn.rollback()
    myconn.close()





@app.route('/payments', methods=['GET', 'POST'])
def payments():
   
    return render_template('payment_page.html')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    try:

        if request.method == 'POST':
            myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
            cur = myconn.cursor()    

            query = "insert into payment_table (amount_paid, policy_identifier, payment_date, payment_description) values ('"+ request.form['amount_paid'] + "','" + "1"+"','"+str(date.today())+"','"+request.form['policy_name']+"')"
            print(query)
            cur.execute(query)

            myconn.commit()

            return redirect(url_for('payments'))

        # don't fully understand the get method yet but adding it anyway just in case ...
        elif request.method == 'GET':
            return render_template('payment_page.html')        
    
    except:
        myconn.rollback()

    myconn.close()

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    global user_id # get the user identifier ...
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
        cur = myconn.cursor()
         
        cur.execute("select payment_description,amount_paid from payment_table where policy_identifier = '" + str(user_id) + "'")    

        payments = cur.fetchall()
        
        cur.execute("select payment_date,amount_paid from payment_table where policy_identifier = '" + str(user_id) + "'")    

        dates = cur.fetchall()


        pay = []
        #dates = [('1999-02-21' , 2223.23), ('2000-09-26' , 456), ('2000-01-01', 6.01), ('1999-01-01', 4565.64), ('2023-03-08', 15)]
        for i in dates:
            pay.append((str(i[0]).replace('-', ','), i[1]))



        return render_template('stats_page.html', data=payments, dates=pay)

    
    except:
        myconn.rollback()
    myconn.close()






# when the user wants to update their credentials ...
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('user_page.html')

@app.route('/userprofile', methods = ['GET', 'POST'])
def user_settings():
    
    try:

        if request.method == 'POST':
            myconn = mysql.connector.connect(host="localhost", user="root", passwd="Mikyle123", database="policy_management_system")
            cur = myconn.cursor()    
            
            # first check if the user is updating their credentials to something that is valid ... (still need to do this)
            
            # update the user's credentials ...  
            query = "update user_table set user_name = '"+ request.form['new_username'] + "', user_password = '" + request.form['new_password']+"' where user_identifier = '"+str(user_id)+"'"
            cur.execute(query)
            myconn.commit()

            # go back to viewing the policies ...
            return redirect(url_for('settings'))

        # don't fully understand the get method yet but adding it anyway just in case ...
        elif request.method == 'GET':
            return render_template('policy_page.html')        
    
    except:
        myconn.rollback()

    myconn.close()
 
 
 
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)