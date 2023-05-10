from flask import Flask, render_template, request,redirect, send_from_directory, abort, g
import pymysql
import pymysql.cursors
from flask_login import LoginManager, login_required, current_user, login_user

login_manager=LoginManager()


app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'g67e46htsjdfgikuytraDSASE323'


class User:
     def __init__(self, id, username, banned):
          self.is_authenticated= True
          self.is_anonymous= False
          self.is_active= not banned

          self.username= username
          self.id= id
        
     def get_id(self):
        return str(self.id)
     
@app.get('/media/<path:path>')
def send_media(path):
    return send_from_directory('media', path)
     
    
@login_manager.user_loader
def user_loader(user_id):
     cursor=get_db().cursor()

     cursor.execute("SELECT * from `Users` WHERE `id` ="+ user_id)

     result=cursor.fetchone()

     if result is None:
          return None
     
     return User(result['id'], result['username'], result['banned'])


@app.route("/home")
def index():

    return render_template(
        "home.html.jinja"
        

    )

@app.route('/feed')
def post_feed():
      
      cursor = get_db().cursor()
      
      cursor.execute("SELECT * FROM `Posts` JOIN `Users` ON `Posts`.`user_id`=`Users`.`id` ORDER BY `timestamp` DESC;")

      results = cursor.fetchall()

      return render_template(
        "feed.html.jinja",

        posts=results
        

    )

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    cursor = get_db().cursor()

    photo = request.files['post_image']

    file_name = photo.filename # my_photo.jpg

    file_extension = file_name.split('.')[-1]

    if file_extension.lower() in ['jpg', 'jpeg', 'png', 'gif']:
        photo.save('media/posts/' + file_name)
    else:
        raise Exception('Invalid file type')

    user_id = current_user.id

    cursor.execute(
        "INSERT INTO `posts` (`post_text`, `post_image`, `user_id`) VALUES (%s, %s, %s)", 
        (request.form['post_text'], file_name, user_id)
    )

    return redirect('/feed')
 


@app.route("/sign-in", methods=['POST', 'GET'])
def sign_in():
      if current_user.is_authenticated:
           return redirect('/feed')
      

      if request.method == 'POST':
           cursor = get_db().cursor()


           cursor.execute("SELECT * FROM `Users` WHERE `username` = %s", (request.form['Username']))
           result = cursor.fetchone()

           if result is None:
                return render_template("sign_in.html.jinja")
           

           
           if request.form['Password'] == result['password']:
                user = User(result['id'], result['username'], result['banned'])

                login_user(user)

                return redirect('/feed')


           
           return request.form

      elif request.method == 'GET':
        return render_template("sign_in.html.jinja")
    # if current_user.is_authenticated:
    #     return redirect("/feed") 
    # else:
    #     return render_template("sign_in.html.jinja")
    
    

    # return render_template(
    #     "sign_in.html.jinja"
    # )
   


@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method=='POST':
         #Hanlde signup
        cursor=get_db().cursor()

        profile=request.files['Profile P']
        file_name=profile.filename #my_photo.jpg
        file_extension=file_name.split('.')[-1]

        if file_extension in ['jpj', 'jpeg', 'png', 'gif']:
             profile.save('media/users/'+ file_name)
        else:
             raise Exception('Invalid file type')

        cursor.execute("""
             INSERT INTO `Users` (`username`, `password`, `email`, `display_name`, `bio`, `photo`,`birthdate` )
             VALUES (%s, %s, %s, %s, %s, %s,%s)
        """, (request.form['Username'],request.form['Password'],request.form['email'],request.form['Display Name'],request.form['Biography'],file_name,request.form['Birthdate']))
        
        
        return redirect('/sign-in')
    elif request.method=='GET':
         return render_template('sign_up.html.jinja')

 

    return render_template(
        "sign_up.html.jinja"
    
    )
    
   








def connect_db():
    return pymysql.connect(
    host = "10.100.33.60",
    user = "kheron",
    password = "222755613",
    database= "kheron_social_media",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit = True


)

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route('/profile/<username>')
def user_profile(username):
    cursor= get_db().cursor()

    cursor.execute(' SELECT * FROM `Users` WHERE `username`= %s', (username))

    result= cursor.fetchone()
     
    if result is None:
          abort(404)
        
    cursor.close()

    cursor=get_db().cursor()

    cursor.execute('SELECT *from `Posts` WHERE `user_id` =%s',(result['id']))

    post_result= cursor.fetchall()

    
    

    return render_template('user_profile.html.jinja',  user=result, posts=post_result)

@app.errorhandler(404)
def four_o_four(e):
     return render_template('404.html.jinja')

if __name__=='__main__':
        app.run(debug=True, port=5001)