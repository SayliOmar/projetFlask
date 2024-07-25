from flask import Flask, render_template, request, session, redirect ,url_for, flash, session
from flask_migrate import Migrate

from Model import db , User

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ecole1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)

with app.app_context():
    db.create_all()


migrate=Migrate(app, db)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name="ilyas", title="Acceuil")








@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        
        # Récupérer l'utilisateur correspondant à l'email fourni
        user = User.query.filter_by(email=email).first()
        if user:
            # Vérifier si le mot de passe correspond
            if user.password== password:
                flash('Vous êtes connecté!', 'success')
                 # Stocker l'ID de l'utilisateur dans la session
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                flash('Mot de passe incorrect!', 'error')
        else:
           
            flash('Utilisateur non trouvé!', 'error')       
    return render_template('login.html', title='Login')
    
    


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        rePassword=request.form['rePassword']
        if password != rePassword:
            flash('le deux mot de passe ne sont pas le meme', 'error')
            return redirect(url_for('inscription'))
        else:
            
            newUser=User(email=email, password=password)
            db.session.add(newUser)
            db.session.commit()
            flash("Brovo! vous etes bien Inscrit", "success")
            return redirect(url_for('login'))
    return render_template('inscription.html', title='inscription')

@app.route('/sedeconnecter')
def deconnecter():
    
    # Supprimer l'ID de l'utilisateur de la session
    session.pop('user_id', None)
    flash('Vous êtes déconnecté!', 'success')
    return redirect(url_for('login'))

@app.route('/formation')
def formation():
    return render_template('formation.html', title="formation")



@app.route('/contact')
def contact():
    return render_template('contact.html', title='contact')



@app.route('/tableBoard', methods=['GET', 'POST'])
def tableBoard():
    users = User.query.all()
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        rePassword=request.form['rePassword']
        if password != rePassword:
            flash('le deux mot de passe ne sont pas le meme', 'error')
            return redirect(url_for('tableBoard'))
        else:
            
            newUser=User(email=email, password=password)
            db.session.add(newUser)
            db.session.commit()
            flash("Brovo! vous etes bien Inscrit", "success")
            return redirect(url_for('tableBoard'))
    return render_template('tableauBord.html', title="table", users=users)




# ajout d'un user


@app.route('/add_user', methods=['POST'])
def add_user():
    email = request.form['email']
    password = request.form['password']
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('tableBoard'))



# suppresson d'un user

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('tableBoard'))






# modfcaton d'un user

@app.route('/edit_user/<int:user_id>', methods=['POST', 'GET'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('tableBoard'))
    else:
        return render_template('modifier.html', user=user)



    
if __name__=="__main__":
    app.run(debug=True)


