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