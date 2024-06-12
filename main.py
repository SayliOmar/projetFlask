from flask import Flask, render_template, request, session, redirect ,url_for, flash

from Model import db , User

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ecole.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name="ilyas", title="Acceuil")








@app.route('/login')
def login():
    return render_template('login.html',title='login' )


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        rePassword=request.form['rePassword']
        newUser=User(email=email, password=password)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('inscription.html', title='inscription')


@app.route('/formation')
def formation():
    return render_template('formation.html', title="formation")



@app.route('/contact')
def contact():
    return render_template('contact.html', title='contact')
if __name__=="__main__":
    app.run(debug=True)


