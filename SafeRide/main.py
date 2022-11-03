from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, login_user, logout_user, current_user, UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides_database.sqlite'
db = SQLAlchemy(app)


# app.config['SECRET_KEY'] = 'saferide'
# login_manager = LoginManager(app)
# login_manager.init_app(app)

# class Driver(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80))
#     password = db.Column(db.String(80))
#
class rides(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.Integer)
    pickup = db.Column(db.String(80))
    dropoff = db.Column(db.String(80))
    comment = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ride = rides()
        ride.name = request.form['name']
        ride.phone = request.form['phone']
        ride.pickup = request.form['pick']
        ride.dropoff = request.form['drop']
        ride.comment = request.form['comment']

        db.session.add(ride)
        db.session.commit()
        return "<h1>Success</h1>"
    return render_template('home.html')


@app.route('/ride')
def ride():
    return render_template('ride.html')


@app.route('/AboutUs')
def aboutus():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.errorhandler(404)
def err404(err):
    return render_template('error.html')


@app.errorhandler(401)
def err401(err):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
