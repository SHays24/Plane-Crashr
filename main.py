import os
sitekey1 = os.environ['sitekey1']
secretkey = os.environ['secretkey']
#import all the webserver stuff
from flask import Flask, render_template, request, redirect
#import the sqlite stuff
import sqlite3
from datetime import datetime
#the name of your app - we'll use this a bunch
app = Flask(__name__)
import jinja2
def datetime_format(value, format="%d %b %Y"):
  dte = datetime.strptime(value, format)
  return dte.strftime("%Y%%20%m%%20%d")
env = jinja2.Environment()
jinja2.filters.FILTERS['datetime_format'] = datetime_format

#when someone goes to /reset in the website...
@app.route('/reset')
#call the function reset_db()
def reset_db():
    #connect to the database
    conn = sqlite3.connect('database.db')
    #make a message that sayd "Opened the database successfully"
    msg = "Opened database successfully"
    #drop the table called animals -- allows you to change the table called "animals"
    conn = sqlite3.connect('database.db')
    try:
      conn.execute("DROP TABLE IF EXISTS planeCrashes;")
    #create the table called planeCrashes with the defined fields
    except:
      #This Print Was Intentially left Blank
      print()
    finally:
      conn.execute("CREATE TABLE planeCrashes(animal_id INTEGER PRIMARY KEY AUTOINCREMENT, date, [Location / Operator], [Aircraft Type / Registration], fatalities, People);")
      #add to the message with "Table created successfully"
      #the <br/> renders as a new line in HTML
      msg = msg + "Table created successfully"
      #close the connection to the database
      conn.commit()
      conn.close()
      #send back to the main flask webserver what it should do.
      return render_template('reset.html', msg=msg)

#when someone goes to the address /enternew on the website
@app.route('/enternew')
#call the function new_animal()
def new_animal():
    
  if request.method == 'GET':
        #make an empty message

        #This is tricky, but it's just trapping errors for us.
        #try means, see if you get to the end of a series of steps and if
        #everything works then we're fine and if it doesn't
        #do the "except" steps and undo everything you did in the try section.

            #assign each of the pieces of information we receive to a new variable

      #this is the template based form code
      return render_template("animal.html", sitekey=sitekey1)
      #fat = request.form['fat']

#when someone goes to the address /addrec on the website
#they could either be posting or getting (POST, put stuff there, GET, request stuff)
@app.route('/addrec', methods=['POST', 'GET'])
#call the function addrec
def addrec():
    #if they POSTed information --> that means they pressed submit on our animal.html page
    #which doesn't do anything but return what the webserver should do
    #go to the animal.html page
  if request.method == 'POST':
    sev = request.form['sev']
    date = request.form['date']
    lo = request.form['lo']
    atr = request.form['atr']
    fat = request.form['fat']
    ppl = request.form['ppl']
#print that to the screen
    print(sev, date, lo, atr, fat)
    #msg1 = str(sev+" "+ date +" "+ lo +" "+ atr +" "+ fat +" "+ppl)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if date != "":
      msg1 = "date"
      cur.execute("SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE date='{}'".format(date))
    elif lo != "":
      msg1 = "location / operator"
      cur.execute("SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE [Location / Operator] Like '%{}%';".format(lo))
      rows1 = cur.fetchall()
    elif atr != "":
      msg1 = "Aircraft Type / Registration"
      cur.execute("SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE [Aircraft Type / Registration] Like '%{}%';".format(atr))
    elif fat != "":
      msg1 = "Fatalities"
      cur.execute("SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE Fatalities={};".format(int(fat)))
    elif ppl != "":
      msg1 = "People"
      cur.execute("SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE People={};".format(int(ppl)))
    elif sev != "":
      cur.execute("""SELECT date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes WHERE Date LIKE '%{}';""".format(sev))
    rows1 = cur.fetchall()
    #if len(rows1) == 0:
      #msg1 = "No crashes found"
      #return render_template("result.html", msg=msg1)
    con.commit()
    con.close()
    return render_template("list.html", rows=rows1)
    print(msg1)
#return what the webserver should do next,
#go to the result page with the msg variable as msg
  print()

@app.route('/updatedata_nuclearlaunchkey')
def keycheck():
  if request.method == 'GET':
    return render_template('result (copy).html')
  elif request.method == 'POST':
    return redirect("/updatedata")
#when someone goes to the address / (i.e. the home page, no extra address)
@app.route('/')
#run the function home
def home():
    #which does nothing
    #but returns what the webserver should do next
    #go to the home page
    return render_template('home.html')

@app.route('/fixfatcolumn')
def fixfatcolumn():
  import re
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  cur.execute('''SELECT Fatalities FROM planeCrashes''')
  data = cur.fetchall()
  i = 1
  #cur.execute('''ALTER TABLE planeCrashes ADD COLUMN People''')
  try:
    for string in i:
      if i == 5017:
        break
      print(data[i],)
      strings = re.sub(r"\(\d+\)|\([?]\)", "", str(data[i-1]))
      print(strings)
      print(i)
      a, b = strings.split('/')
      print(a, b, i,)

      a = a.strip(r"('")
      print(a)
      with open("test.txt",'a',encoding = 'utf-8') as f:
         f.write(str(a,) + "\n")
      b = b.strip("',)")
      print(b)
      with open("test.txt",'a',encoding = 'utf-8') as f:
         f.write(str(b,) + "\n")
      cur.execute(f"""UPDATE OR REPLACE planeCrashes SET Fatalities = ?, People = ? WHERE animal_id = ?;""", (a, b, i))
      con.commit()
      i += 1
  finally:
    cur.execute("""DELETE FROM planeCrashes WHERE Date IS NULL""")
    con.commit()
    con.close()
    return "it done now"
            
      
#when someone goes to the address /updatedata (this is for updating the data based on new json files uploaded to the folder jsonFiles)
@app.route('/updatedata')
#run the function updateData
def updateData():
  import time
  import pandas as pd
  year = 1920
  curYear = int(time.strftime("%Y", time.gmtime()))+1
  print(curYear)
  for year in range(2021, curYear):
    url = f'http://www.planecrashinfo.com/{year}/{year}.htm'
    dfs = pd.read_html(url, header = 0)
    new_csv = dfs[0].to_csv(index=False)
    with open(f'crashDatabase/{year}.csv', 'w') as f:
      f.write(new_csv)
    #time.sleep(2)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    df = pd.read_csv(f"crashDatabase/{year}.csv")
    df.to_sql("planeCrashes", con, if_exists='append', index=False)
    cur.execute("SELECT * FROM planeCrashes")
    print(cur.fetchall())
    con.commit
    con.close
  return 'it worked'


@app.route('/listnew')
def get_listnew():
  #connect to the db
  con = sqlite3.connect("database.db")
  #makes us able to reference each field by name
  con.row_factory = sqlite3.Row
  #make a cursor which helps us do all the things
  cur = con.cursor()
  #execute a select on the data in the database
  cur.execute("select date, [Location / Operator], [Aircraft Type / Registration], Fatalities, People FROM planeCrashes")
  #fetch all the records
  rows1 = cur.fetchall()
  con.commit()
  con.close()
  #return what the webserver should do next,
  #go to the list page with the rows variable as rows
  return render_template("list.html", rows=rows1)


#Check that this isn't being run by another module
if __name__ == '__main__':
    #run on the host 0.0.0.0
    app.run(debug=True, host='0.0.0.0')

#using the animal cards from https://aca.edu.au/resources/decision-trees-animal-trading-cards/
