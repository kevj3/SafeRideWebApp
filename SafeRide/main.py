from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, query
from flask_login import login_required, login_manager, login_user, logout_user, current_user, UserMixin, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['SECRET_KEY'] = 'saferide'
login_manager = LoginManager(app)
login_manager.init_app(app)


class Driver(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


class Rides(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    pickup = db.Column(db.String(80))
    dropoff = db.Column(db.String(80))
    comments = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        pickup = request.form['pick']
        dropoff = request.form['drop']
        comments = request.form['comment']
        ride = Rides(name=name, phone=phone, pickup=pickup, dropoff=dropoff, comments=comments)

        db.session.add(ride)
        db.session.commit()
        return redirect('/confirmation/' + name)
    return render_template('home.html')


@app.route('/rides')
def rides():
    ride = Rides.query.all()
    return render_template("ride.html", ride=ride)

@app.route('/confirmation/<name>')
def confirm(name):
    return render_template("confirmation.html",name=name)


@app.route('/ControlPanel')
@login_required
def driver():
    ride = Rides.query.all()
    return render_template("driver.html", ride=ride)

@app.route('/ControlPanel/<id>')
def delete(id):
    ride = Rides.query.filter_by(id=id).first()
    db.session.delete(ride)
    db.session.commit()
    return redirect(url_for('driver'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('Logout.html')


@app.route('/AboutUs')
def aboutus():
    return render_template('about.html')


@app.errorhandler(404)
def err404(err):
    return render_template('error.html')


@app.errorhandler(401)
def err401(err):
    return render_template('error.html')


@login_manager.user_loader
def user_loader(uid):
    user = Driver.query.get(uid)
    return user


@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Driver.query.filter_by(username=username).first()
        if user != None:
            if password == user.password:
                login_user(user)
                return redirect(url_for('driver'))
            return 'FAIL'
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
