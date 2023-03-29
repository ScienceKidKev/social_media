from flask import Flask, render_template, request,redirect
import pymysql
import pymysql.cursors




app = Flask(__name__)


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
        cursor.execute("""
             INSERT INTO `Users` ('username', 'password', 'email', 'display_name', 'bio', 'photo' )
             VALUES (%s, %s, %s, %s, %s, %s)
        """[])

        return request.form
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

if __name__=='__main__':
        app.run(debug=True)