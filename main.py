from flask import Flask, render_template, request,redirect
import pymysql
import pymysql.cursors
from flask_login import LoginManager

login_manager=LoginManager()


app = Flask(__name__)
login_manager.init_app(app)

class User:
     def __init__(self, id, username, banned):
          self.is_authenticated= True
          self.is_anonymous= False
          self.is_active= not banned

          self.username= username
          self.id= id
        
     def get_id(self):
        return str(self.id)
     
@app.get('/media/')
def send_media(path):
    return send_from_directory('media', path)
     
    
@login_manager.user_loader
def user_loader(user_id):
     cursor=connection.cursor()

     cursor.execute("SELECT * from `users` WHERE `id` ="+ user_id)

     result=cursor.fetchone()

     if result is None:
          return None
     
     return User(result['id'], result['username'], result['banned'])


@app.route("/home")
def index():

    return render_template(
        "home.html.jinja"
        

    )

@app.route('/post')
def post_feed():
      
      cursor = connection.cursor()
      
      cursor.execute("SELECT * FROM `Posts` JOIN `Users` ON `Posts`.`user_id`=`Users`.`id` ORDER BY `timestamp` DESC;")

      results = cursor.fetchall()

      return render_template(
        "feed.html.jinja",

        posts=results
        

    )


@app.route("/sign-in")
def sign_in():

    return render_template(
        "sign_in.html.jinja"
    
    )


@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method=='POST':
         #Hanlde signup
        cursor=connection.cursor()

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
        
        
        return redirect('/feed')
    elif request.method=='GET':
         return render_template('sign_up.html.jinja')


    return render_template(
        "sign_up.html.jinja"
    
    )








connection = pymysql.connect(
    host = "10.100.33.60",
    user = "kheron",
    password = "222755613",
    database= "kheron_social_media",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit = True


)

@app.route('/profile/<username>')
def user_profile(username):
     cursor= connection.cursor()

     cursor.execute(' SELECT * FROM `Users` WHERE `username`= %s', (username))

     result= cursor.fetchone()
     
     return render_template('user_profile.html.jinja', user=result)

if __name__=='__main__':
        app.run(debug=True, port=5001)