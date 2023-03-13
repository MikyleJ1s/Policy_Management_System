import time
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
            
            # search for the username and password in the database ... 
            query = "select user_identifier from user_table where binary user_email = '" + request.form['username'] + "' and binary user_password = '" + request.form['password'] + "'"        
            cur.execute(query)
            useraccount = cur.fetchone()

            # check if the user with that username and password exists ... 
            if useraccount:
                app.logger.info("User {} data successfully fetched".format(user_id))
                user_id = useraccount[0]
                
                # user exists so go to the home page ...
                return redirect(url_for('user_policies'))

            # otherwise, no such user was found so stay on the login page ...
            else: 
                time.sleep(2)
                return render_template('login_page.html', error = "Invalid Credentials") 
            
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()
    myconn.close()
 

@app.route("/logging_out", methods = ['POST'])
def logging_out():
    app.logger.info("User has logged out")
    return redirect(url_for('login'))

@app.route("/fetch_policies", methods = ['POST'])
def policies():
    app.logger.info("User policies fetched")
    return redirect(url_for('user_policies'))

@app.route('/policies', methods=['GET', 'POST'])
def user_policies(): 
    
    # get the user identifier ...
    global user_id 
    
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
        cur = myconn.cursor()
                
        # get the name, amount paid and starting date for each policy belonging to the user ...
        cur.execute("select policy_name, round(amount_paid,2), date_acquired from policy_table where user_identifier = '"+str(user_id)+"'")
        pol = cur.fetchall()

        # then display the user's policies ... 
        if request.method == 'GET':
            return render_template('policies_page.html', policies=pol)
        
        return render_template('policies_page.html', policies='')
    
    except Exception as e:
        app.logger.error("Error fetching data as follows {}". format(e))
        myconn.rollback()
    myconn.close()


@app.route('/payments', methods=['GET', 'POST'])
def payments():
    # first get all the user's policies ... 
    myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
    cur = myconn.cursor()     
    cur.execute("select policy_name from policy_table where user_identifier = '" + str(user_id) + "'")    
    policies = cur.fetchall()   
    
    # now add the policies to payment page so it can be considered as an option ...
    return render_template('payment_page.html', policies = policies)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    try:

        if request.method == 'POST':
            myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
            cur = myconn.cursor()    
            
            # get the policy identifier of the policy that the user is paying for ... 
            query = "select policy_identifier from policy_table where user_identifier = '"+str(user_id)+"' and policy_name = '"+request.form.get("options")+"'"
            cur.execute(query)
            policy_id = cur.fetchone()
            
            # put the payment details in the payment table ...
            query = "insert into payment_table (amount_paid, policy_identifier, payment_date, payment_description, user_identifier) values ('"+ request.form['amount_paid'] + "','" + str(policy_id[0])+"','"+str(date.today())+"','"+request.form.get("options")+"','"+str(user_id)+"')"
            cur.execute(query)
            myconn.commit()
            
            # now add the amount paid to policy table so the policy page gets updated as well ...
            query = "select amount_paid from policy_table where policy_identifier = '"+str(policy_id[0])+"'"
            cur.execute(query)
            original_amount = cur.fetchone()

            new_amount = original_amount[0] + float(request.form['amount_paid'])

            query = "update policy_table set amount_paid = '"+ str(new_amount) +"' where policy_identifier = '"+str(policy_id[0])+"'"
            cur.execute(query)
            myconn.commit()
            
            time.sleep(2)
            return redirect(url_for('payments'))

        elif request.method == 'GET':
            return render_template('payment_page.html')        
     
    
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()

    myconn.close()

@app.route('/statistics', methods=['GET', 'POST'])
def stats():
    global user_id 
    try:   
        myconn = mysql.connector.connect(host="localhost", user="root", passwd=dbmspass, database="policy_management_system")
        cur = myconn.cursor()
        
        # get the user payments and display it in a pie chart ...
        cur.execute("select payment_description, sum(amount_paid) from payment_table where user_identifier = '" + str(user_id) + "' group by payment_description")    
        payments = cur.fetchall()
        
        # get all the transaction dates and amount paid ...
        cur.execute("select payment_date,amount_paid from payment_table where user_identifier = '" + str(user_id) + "'")    
        dates = cur.fetchall()
        
        cur.execute("select (MONTH(payment_date)) as themonth, (YEAR(payment_date)) AS theyear, round(SUM(amount_paid),2) AS totalamount FROM payment_table WHERE user_identifier = '"+str(user_id)+"' GROUP BY (MONTH(payment_date)), (YEAR(payment_date)) order by (YEAR(payment_date)), (MONTH(payment_date));")
        info = cur.fetchall()
        # reformat the dates ...
        pay = []
        for i in dates:
            pay.append((str(i[0]).replace('-', ','), i[1]))
        
        # send the data to the stats page ...
        return render_template('stats_page.html', data=payments, dates=pay, info = info)

    
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
            try:
            # update the user's credentials ...  
                query = "update user_table set user_email = '"+ request.form['new_username'] + "', user_password = '" + request.form['new_password']+"' where user_identifier = '"+str(user_id)+"'"
                cur.execute(query)
                myconn.commit()
            except:
                query = "update user_table set user_password = '" + request.form['new_password']+"' where user_identifier = '"+str(user_id)+"'"
                cur.execute(query)
                myconn.commit()
            

            return redirect(url_for('settings'))

        elif request.method == 'GET':
            return render_template('policy_page.html')        
    
    except Exception as e:
        app.logger.exception("The following error was captured {}".format(e))
        myconn.rollback()

    myconn.close()
 
 

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)