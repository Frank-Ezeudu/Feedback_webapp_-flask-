from flask import Flask, render_template, request  
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/benz'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)  

class Feedback(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    customer = db.Column(db.String(200), unique=True)  
    dealer = db.Column(db.String(200))  
    rating = db.Column(db.Integer)  
    comments = db.Column(db.Text)  

    def __init__(self, customer, dealer, rating, comments):  
        self.customer = customer  
        self.dealer = dealer  
        self.rating = rating  
        self.comments = comments  

@app.route('/')  
def index():  
    return render_template('index.html')  

@app.route('/submit', methods=['POST'])  
def submit():  
    if request.method == 'POST':  
        customer = request.form['customer']  
        dealer = request.form['dealer']  
        rating = request.form['rating']  
        comments = request.form['comments']  

        if customer == '' or dealer == '':
            return render_template('index.html',message='please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer , dealer , rating , comments)      
            return render_template('success.html')  
        else:  
            return render_template('index.html', message="Please enter required fields")  

if __name__ == '__main__':  
    app.run(debug=True)   