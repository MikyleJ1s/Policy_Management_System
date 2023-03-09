import mysql.connector
from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)

@app.route("/checkout")
def payment():
    return render_template('payment.html', error="error making payment")






if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(debug=True)