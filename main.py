from flask import Flask , redirect, render_template , url_for, request , make_response, flash , abort
from flask_bootstrap import Bootstrap5
from sqlalchemy import INTEGER, String , Float , Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column ,relationship
import requests
from form import Add_Anime, ADD_Manga , RegisterForm , LoginForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user , login_required
from flask_migrate import Migrate
import random
from dotenv import load_dotenv
import os




load_dotenv()



#api
CLIENT_ID = os.getenv('Anime_key') #anime website api

headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID  # Authentication header
}


# anime api url 
Anime_url = 'https://api.jikan.moe/v4/anime'

#manga api url 
Manga_url = "https://api.jikan.moe/v4/manga"



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('Flask_key') # hear create a flask key go to the chat gpt and search for create a flask key and here

Bootstrap5(app)

#here i can add flask_login class to add some advance feature in login page or register page that can user need details to login in website

login_manager = LoginManager()
login_manager.init_app(app)


class base(DeclarativeBase):
    pass


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Manga_Anime-database.db"

# here i can use pgadmin 4 for database 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL') # you can add here your own database connect to pgadmin4 


db = SQLAlchemy(model_class=base)
# here i can use migrate for migration database like manage database using migration it time to time update database 
migrate = Migrate(app, db)  # Add migration support
db.init_app(app)

# creating table from  sqlalchemy 
class Anime_table(db.Model):
    __tablename__ = 'Animetable'
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    #here i create a relationship but i don't know properly how is this work 
    user_id : Mapped[int] = mapped_column(INTEGER, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User',back_populates='anime_list')
    
    
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(INTEGER, nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)
    ranking: Mapped[int] = mapped_column(INTEGER, nullable=False)
    img_url: Mapped[str] = mapped_column(String(500),nullable=False)


    
class Manga_table(db.Model):
    __tablename__  = 'Mangatable'
    id :Mapped[int] = mapped_column(INTEGER,primary_key=True)
    
    user_id : Mapped[int] = mapped_column(INTEGER,db.ForeignKey('users.id'), nullable=False)
    user = relationship('User',back_populates='manga_list')
    
    
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(INTEGER, nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)
    ranking: Mapped[int] = mapped_column(INTEGER, nullable=False)
    img_url: Mapped[str] = mapped_column(String(500),nullable=False)
    
    

class User(UserMixin,db.Model):
    __tablename__ ="users"
    id : Mapped[int] = mapped_column(INTEGER,primary_key=True)
    name :Mapped[str] = mapped_column(String(250),nullable=False)
    email : Mapped[str] = mapped_column(String(250), unique=True , nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False) 
    
    
    anime_list = relationship('Anime_table',back_populates='user',cascade='all , delete')
    manga_list = relationship('Manga_table',back_populates='user',cascade='all , delete')
    


with app.app_context():
    db.create_all()
    
    

@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


# Custom error message when user is not logged in
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('error.html'),401 

# -------------------------------------------------------------------------------------------------------------------------------------------    
                                        #I CAN ADD  THIS CODE   EXAMPLE                                                                     | 
                                        #                                                                                                   |
                                        # new_anime = Anime_table(                                                                          |
                                        #     title = 'Naruto',                                                                             |
                                        #     year = 2002,                                                                                  |
                                        #     description = 'Naruto is a Japanese manga series written and illustrated by Masashi Kish',    |
                                        #     rating = 9.0,                                                                                 |
                                        #     review = "Nice anime",                                                                        |
                                        #     img_url = "https://cdn.myanimelist.net/images/anime/10/47347l.jpg",                           |
                                        #     ranking = 2                                                                                   |
                                        # )                                                                                                 |
                                        # with app.app_context():                                                                           |
                                        #         db.session.add(new_anime)                                                                 |
                                        #         db.session.commit()       
                                        # 
                                       #  is_authenticated  function return us boolean value like true or false like if user
                                       # is login then return us true or if user not then  give us false value 
                                        
                                        # 
                                        # 
                                        # |
#--------------------------------------------------------------------------------------------------------------------------------------------  




# this function show you all result that name you  search  on Add page
@app.route('/add',methods=["GET","POST"])
@login_required
def add():
    form = Add_Anime()
    if form.validate_on_submit():
        response = requests.get(Anime_url, params={'q':form['form_title'],'limit':10},headers=headers)
        data = response.json()['data']
        return render_template('select.html',data=data)
    return render_template('add.html',form=form , current_user=current_user)


# this function use add a details on home page like img or everyting
@app.route('/find',methods=['GET','POST'])
@login_required
def find():
    anime_id = request.args.get('id')
    print(f"Anime ID received: {anime_id}")  # check id in api response in my case is mal_id instend of id  if you are doing with id then you are grting error
    # see "TypeError: The view function for 'find' did not return a valid response. 
    # The function either returned None or ended without a return statement. "
    if anime_id:
        url_id = f"{Anime_url}/{anime_id}"
        response = requests.get(url_id,headers=headers)
        data = response.json().get('data', []) # why i m using this for : in api response all details  are present in data list that's why i use her
        new_anime = Anime_table(
            title=data.get('title_english', data.get('title', 'Unknown')),# like if title english does'nt exist then for backup we are going with title 
            year=data.get('aired', {}).get('prop', {}).get('from', {}).get('year', 'Unknown'),# this line are nested i don't know this line i get this line from chatgpt 
            description=data.get('synopsis', 'No description available'),
            img_url=data.get('images', {}).get('jpg', {}).get('large_image_url', ''),
            rating=data.get('score', 0),
            ranking=data.get('rank', 0),
            user_id = current_user.id
        )
        db.session.add(new_anime)
        db.session.commit()
        return redirect(url_for('home'))
    
random_images = [
    'https://i.pinimg.com/736x/f6/46/c8/f646c85acc80d81c624ef773f7f286cd.jpg',
    'https://i.pinimg.com/736x/62/3e/42/623e42c2d4575acae673ba2a0c980141.jpg',
    'https://i.pinimg.com/736x/f1/fc/ce/f1fcce4ae0c44bba68e79ef7784b28a6.jpg',
    'https://i.pinimg.com/736x/0d/e6/ce/0de6ce49c65a596a91aba63dcc4a19ea.jpg',
    'https://i.pinimg.com/736x/ff/f5/c1/fff5c1a6ac2e774d5ff54aaa99362d38.jpg',
    'https://i.pinimg.com/736x/89/60/56/896056ec3e9dbe88f0a1fdf9f0fdfc17.jpg',
    'https://i.pinimg.com/736x/40/31/00/403100c729d0ef4551aeadfa57d9cbf7.jpg',
    'https://i.pinimg.com/736x/0f/4b/da/0f4bdaa376d435f008611da63c4df185.jpg',
    'https://i.pinimg.com/736x/22/b7/fe/22b7fee54c5adc17c8d14b8400c52117.jpg',
    'https://i.pinimg.com/736x/75/64/0d/75640dd67564c24a73156febff0c75ba.jpg',
    'https://i.pinimg.com/736x/c7/e2/b4/c7e2b4d1644500e428a6a00b7d8cd640.jpg',
    'https://i.pinimg.com/736x/40/30/68/403068f9a7ea2e39a1519dc98da0e674.jpg'
]

@app.route("/random-image")
def random_image():
    return redirect(random.choice(random_images))  

@app.route('/')
def home():
    if current_user.is_authenticated:
        anime_list = Anime_table.query.filter_by(user_id = current_user.id).all() # like that if current_user is authenticated then ,
        #it check first,
        #if user added  some data in past then it  show you then  how it works or  do it using user_id stored in anime or manga if not then  it show no data. 
        #if user logout then all session data are delete only session data not database data
    else:
        anime_list =[]  # why i add empty list beacuse of if no one is login then show empty list if user login then find by user_id 

    return render_template('index.html',anime_list=anime_list, current_user=current_user)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        response=  db.session.execute(db.select(User).where(User.email ==  email))
        user_data = response.scalar()
        if user_data:
            flash('This Email Already Exist !')
            return redirect(url_for('login'))
        hash_password = generate_password_hash(request.form.get('password'),
                                            method='pbkdf2:sha256',
                                            salt_length=16)
        new_user = User(
            name = request.form.get('name'),
            email = request.form.get('email'),
            password = hash_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        # this line ogf code automatically login in website you don't need to add information in login page 
        login_user(new_user)
        
        return redirect(url_for('home'))
    return render_template('register.html', form=form, current_user=current_user)





@app.route('/login', methods=['GET','POST'])
def  login():
    form = LoginForm()
    if form.validate_on_submit():
        email =  request.form.get('email')
        password = request.form.get('password')
        
        response = db.session.execute(db.select(User).where(User.email == email))
        users = response.scalar()
        if not users:
            flash('Please Check Your Email !')
            return redirect(url_for('login'))
        elif not check_password_hash(users.password, password) :
            flash('Please Check Your Password')
            return redirect(url_for('login'))
        else:
            login_user(users)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, current_user=current_user)






@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile',methods=['GET','POST'])
def profile():
    form = RegisterForm()
    if form.validate_on_submit:
        password = request.form.get('password')
    return render_template('profile.html', passw=password, current_user=current_user)




@app.route("/delete")
@login_required
def delete():
    anime_id = request.args.get("id")
    anime = db.get_or_404(Anime_table, anime_id)
    if anime.user_id != current_user.id:
        abort(403) 
    db.session.delete(anime)
    db.session.commit()
    return redirect(url_for("home"))

#----------------------Manga--Section _______________________________________

@app.route('/manga')
@login_required
def Manga():
    if current_user.is_authenticated:
        Manga = Manga_table.query.filter_by(user_id = current_user.id).all()
    else :
        Manga = []
    return render_template('manga.html',manga_list = Manga, current_user=current_user)

@app.route('/addmanga',methods=["GET","POST"])
@login_required
def add_manga():
    form = ADD_Manga()
    if form.validate_on_submit():
        response = requests.get(Manga_url,params={"q":form['Manga_title'].data})
        data = response.json().get('data', [])
        print(data)
        return render_template("select_manga.html",response=data)
    return render_template('add_manga.html',form=form, current_user=current_user)
    
    
    
    
@app.route('/add/manga',methods=['GET','POST'])
@login_required
def find_manga():
    manga_id = request.args.get('id')
    if manga_id:
        manga_id_url = f"{Manga_url}/{manga_id}"
        response = requests.get(manga_id_url)
        data = response.json().get('data',[])
        new_manga = Manga_table(
            title=data.get('title_english', data.get('title', 'Unknown')),# like if title english does'nt exist then for backup we are going with title 
            year=data.get('aired', {}).get('prop', {}).get('from', {}).get('year', 'Unknown'),# this line are nested i don't know this line i get this line from chatgpt 
            description=data.get('synopsis', 'No description available'),
            img_url=data.get('images', {}).get('jpg', {}).get('large_image_url', ''),
            rating=data.get('score', 0),
            ranking=data.get('rank', 0),
            user_id = current_user.id # how it work  like if user is login then user can add data ok if user is not then data is not present in user list ok 
        )
        db.session.add(new_manga)
        db.session.commit()
        return redirect(url_for('Manga'))



@app.route('/remove',methods=['GET', 'POST'])
@login_required
def manga_delete():
    manga_id = request.args.get("id")
    if manga_id:
        manga = db.get_or_404(Manga_table, manga_id)
        if manga.user_id != current_user.id:
            abort(403) 
        db.session.delete(manga)
        db.session.commit()
        return redirect(url_for("Manga"))
    return redirect(url_for("Manga"))


if __name__ == "__main__":
    app.run(debug=True,port=5009)
