import mysql.connector
from flask import Flask, redirect, render_template, url_for, request
from datetime import date
import logging
app = Flask(__name__)
user_id = ''
#logger config
logger = logging.getLogger(__name__)
logging.basicConfig(filename="PMS.log", level = logging.DEBUG, format = f"%(asctime)s %(levelname)s %(message)s")
#global dbms password variable
dbmspass = "Mikyle123"

@app.route('/', methods=['GET', 'POST'])
def login():
    app.logger.info("Logout page called")
    return render_template('login_page.html')

    
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    global user_id
    try:
        myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
        cur = myconn.cursor()
        if request.method == 'POST':
        
            query = "select user_identifier from user_table where binary user_name = '" + request.form['username'] + "' and binary user_password = '" + request.form['password'] + "'"        
            cur.execute(query)
            useraccount = cur.fetchone()
            app.logger.info("User {} data successfully fetched".format(user_id))
            if useraccount:
                user_id = useraccount[0]
                return redirect(url_for('user_policies'))
            else: 
                return render_template('login_page.html') 
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()
    myconn.close()
 

@app.route("/logging_out", methods = ['POST'])
def logging_out():
    app.logger.info("Logout path initialised")
    return redirect(url_for('login'))

@app.route("/fetch_policies", methods = ['POST'])
def policies():
    app.logger.info("User policies fetched")
    return redirect(url_for('user_policies'))

@app.route('/policies', methods=['GET', 'POST'])
def user_policies(): 
    global user_id # get the user identifier ...
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
        cur = myconn.cursor()
                
        # get the name, amount paid and date started for each policy belonging to the user ...
        cur.execute("select policy_name, round(amount_paid,2), date_acquired from policy_table where user_identifier = '"+str(user_id)+"'")
        pol = cur.fetchall()

        if request.method == 'GET':
            return render_template('policies_page.html', policies=pol)
        
        return render_template('policies_page.html', policies='')
    
    except Exception as e:
        app.logger.error("Error fetching data as follows {}". format(e))
        myconn.rollback()
    myconn.close()


@app.route('/payments', methods=['GET', 'POST'])
def payments():
    myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
    cur = myconn.cursor()     
    cur.execute("select policy_name from policy_table where user_identifier = '" + str(user_id) + "'")    
    policies = cur.fetchall()   
    return render_template('payment_page.html', policies = policies)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    try:

        if request.method == 'POST':
            myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
            cur = myconn.cursor()    
            
            query = "select policy_identifier from policy_table where user_identifier = '"+str(user_id)+"' and policy_name = '"+request.form.get("options")+"'"
            cur.execute(query)
            policy_id = cur.fetchone()
            
              
            # check if the user has put in a valid insurance name ...  
            if policy_id:
                # put it in the payment table (like a bank statement) ...
                query = "insert into payment_table (amount_paid, policy_identifier, payment_date, payment_description, user_identifier) values ('"+ request.form['amount_paid'] + "','" + str(policy_id[0])+"','"+str(date.today())+"','"+request.form.get("options")+"','"+str(user_id)+"')"
                cur.execute(query)
                myconn.commit()
                
                # get the amount paid in order to update it to the total amount paid ...
                query = "select amount_paid from policy_table where policy_identifier = '"+str(policy_id[0])+"'"
                cur.execute(query)

                original_amount = cur.fetchone()

                new_amount = original_amount[0] + float(request.form['amount_paid'])

                query = "update policy_table set amount_paid = '"+ str(new_amount) +"' where policy_identifier = '"+str(policy_id[0])+"'"

                cur.execute(query)
                myconn.commit()
            return redirect(url_for('payments'))

        # don't fully understand the get method yet but adding it anyway just in case ...
        elif request.method == 'GET':
            return render_template('payment_page.html')        
     
    
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()

    myconn.close()

@app.route('/statistics', methods=['GET', 'POST'])
def stats():
    global user_id # get the user identifier ...
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
        cur = myconn.cursor()

        
        #cur.execute("select payment_description,amount_paid from payment_table where user_identifier = '" + str(user_id) + "'")
        cur.execute("select payment_description, sum(amount_paid) from payment_table where user_identifier = '" + str(user_id) + "' group by payment_description")    

        payments = cur.fetchall()
        
        cur.execute("select payment_date,amount_paid from payment_table where user_identifier = '" + str(user_id) + "'")    

        dates = cur.fetchall()


        pay = []
        for i in dates:
            pay.append((str(i[0]).replace('-', ','), i[1]))
        



        return render_template('stats_page.html', data=payments, dates=pay)

    
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
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
            myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
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
    
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()

    myconn.close()
 
 
 
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)