from flask import Flask,request,render_template,redirect,url_for
import sqlite3 as db

app=Flask(__name__)


@app.route('/')
def search():
	return render_template('newhome.html')


@app.route('/result',methods=['POST','GET'])
def result():
	if request.method=="POST":
		srch=request.form['search']
		con=db.connect('webhosp.db')
		cur=con.cursor()
		query='SELECT * FROM hosp WHERE name LIKE ?'
		cur.execute('SELECT * FROM hosp WHERE name LIKE ?', ('%{}%'.format(srch),))
		th=['hid','name','city','addr','special','contact','type']
		l=cur.fetchall()
		nl=[]
		for row in l:
			di={}
			for i in range(len(th)):di[th[i]]=row[i]
			nl.append(di)
		return render_template('result.html',res=nl)
