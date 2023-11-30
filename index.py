from flask import Flask, render_template, request, url_for, redirect
import sqlite3 
from konsepOOP import *

app = Flask('__name__') 

conn = sqlite3.connect('db_belajar_jalan.db',check_same_thread=False,isolation_level=None)
#update ke-3
@app.route('/', methods = ['GET', 'POST'])
def index():
	cur = conn.cursor()
	data = cur.execute('select * from terbaru').fetchall()

	a = tagar().fetchA()
	if request.method == 'GET':
		print(a)
		return render_template('index.html', data=data,	a=a)
	elif request.method == 'POST':
		search = cur.execute('select * from terbaru where LOWER(judul)=LOWER("{}")'.format(request.form.get('ok'))).fetchall()	
		if(search):
			return render_template('cari.html', hebat=search)
		else:
			return render_template('notfound.html')

@app.route('/dash', methods = ['GET','POST'])
def dash():
	Aj = request.form.get('Hebat')
	Ak = request.form.get('kategori')
	Ad = request.form.get('deskripsi')

	if request.method == 'GET':
		return render_template('info.html')
	else:
		curs = conn.cursor()
		fs = request.files['sampul']
		fp = request.files['file']

		cek = curs.execute(f"insert into terbaru values (null,'{Aj}','{Ak}','{Ad}','{fp.filename}','{fs.filename}')")
		fp.save('static/pdf/'+fp.filename)
		fs.save('static/img/'+fs.filename)

		conn.commit()
		# return Aj
		#return Ad

		if cek:
			return redirect(url_for('index'))
		else:
			return 'gagal'



@app.route('/admin', methods = ['GET', 'POST'])
def login():
	user = request.form.get('user')
	pw = request.form.get('pass')
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		l = Login(user,pw)
		if l.Check() == '200':
			return redirect(url_for('dash'))
		else:
			return render_template('login.html')

@app.route('/baca/<int:keren>')
def baca(keren):
	cur = conn.cursor()
	medata = cur.execute(f'select * from terbaru where id={keren}').fetchall()	
	print(medata)
	return render_template('read.html',medata=medata)

if __name__ == '__main__':
	app.run(debug=True)
