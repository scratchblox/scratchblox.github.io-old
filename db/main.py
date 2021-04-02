import flask
app = flask.Flask(__name__)
import sqlite3
import os, base64
from flask_cors import CORS



CORS(app, orgins=["https://scratchblox.tk/"])

def generate_session():
    return base64.b64encode(os.urandom(16))


from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('primary.db', check_same_thread=False)

        return con

    except Error:

        print(Error)




con = sql_connection()
cursorObj = con.cursor()

def sql_decode(sqlObject):
  response = []
  for i in sqlObject:
      response.append(i)
  return response

def get_user_from_token(token):
  cursorObj.execute(f"SELECT username FROM user WHERE token = \"{token}\"")
  result = cursorObj.fetchone()
  if result:
    return result[0]
  else:
    return None

def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO user(id, username, password, token, rank) VALUES(?, ?, ?, ?, ?)', entities)
    
    con.commit()
def sql_fetch_users(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM user')

    rows = cursorObj.fetchall()

    response = []

    for row in rows:

        response.append(row)
    return response
def login(username, password):
  cursorObj.execute(f"SELECT token from user WHERE username='{username}' AND password = '{password}';")
  userdata = cursorObj.fetchone()
  if not userdata:
    return flask.jsonify({"message":"login incorrect"}), 403
  else:
    if userdata[0] == "":
      new_token = generate_session()
      cursorObj.execute(f"UPDATE user SET token = \"{new_token}\" WHERE username=\"{username}\" AND password = \"{password}\"")
      con.commit()
      return flask.jsonify({"message":"200", "_token":str(new_token)})
    else:
      return flask.jsonify({"message":"200", "_token":userdata[0]})

    return
def createNewAccount(id, username, password):
  exists = cursorObj.execute(f"""
  SELECT COUNT(1)
  FROM user
  WHERE username = '{username}';
  """)
  for i in exists:
    exists = i
  if exists == (0,):
    data = (id, username, password, "", 1)
    sql_insert(con, data)
    return True
  elif exists == (1,):
    return False

@app.route('/getusers', methods=["POST","GET"])
def getusers():
  return flask.jsonify({"users": (sql_fetch_users(con))})

@app.route('/register', methods=["POST"])
def makeaccount():
  username = flask.request.form.get("username")
  password = flask.request.form.get("password")
  _temp = cursorObj.execute("SELECT COUNT(*) FROM user")
  newid = int(sql_decode(_temp)[0][0]) + 1
  instance = createNewAccount(newid, username, password)
  if instance == True:
    return flask.jsonify({"message":"registered", "status":"200"}), 200
  elif instance == False:
    return flask.jsonify({"message":"username is taken", "status":"300"}), 200

@app.route('/auth/login', methods=["POST"])
def auth():
  username = flask.request.form.get("username")
  password = flask.request.form.get("password")
  return login(username, password)

@app.route('/auth/token', methods=["POST"])
def check():
  token = flask.request.form.get("token")
  response = get_user_from_token(token)
  if response:
    return flask.jsonify({"message":"200", "user":response}), 200
  else:
    return flask.jsonify({"message":"invalid token"}), 403

app.run("0.0.0.0", 8080, threaded=True)
