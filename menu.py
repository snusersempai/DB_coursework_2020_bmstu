from flask import Flask, render_template,request,redirect, url_for
from db_connect import db_connect
import mysql.connector
app = Flask(__name__)

@app.route('/menu/', methods=['GET', 'POST'])
def menu():
    try:
        point = request.args['point']
    except:
        point = None
    if (point == '1'):
        return redirect(url_for('zapros1'))
    if (point == '2'):
        return redirect(url_for('zapros2'))
    if (point == '3'):
        return redirect(url_for('zapros3'))
    if (point == '4'):
        return redirect(url_for('zapros4'))
    if (point == '5'):
        return redirect(url_for('zapros5'))
    if (point == '6'):
        return redirect(url_for('zapros6'))
    if (point == '7'):
        return redirect(url_for('proc'))
    elif (point =='exit'):
        return('Good_by!!!')
    else:
        return render_template('main_menu.html')

@app.route('/zapros1/',methods=['GET','POST'])
def zapros1():
        	conn = db_connect('root','root')
        	cursor = conn.cursor()
        	_SQL = """
                    SELECT id, surname, `date`, weight
                    FROM tab ;"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['id', 'surname','date','weight']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros1.html',blanks = res)


@app.route('/zapros2/',methods=['GET','POST'])
def zapros2():
        	conn = db_connect('root','root')
        	cursor = conn.cursor()
        	_SQL = """
                    SELECT surname
                    FROM tab
                    WHERE `date` >= '2017.03.01' AND `date` <= '2017.03.31' AND id_dog = 'XXX' ;"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['surname']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros2.html', blanks = res)


@app.route('/zapros3/',methods=['GET','POST'])
def zapros3():
        	conn = db_connect('root','root')
        	cursor = conn.cursor()
        	_SQL = """SELECT id_dog, company, tel_num, state, address, surname, weight
                    FROM `client` JOIN ttn USING(id_dog)
                    WHERE weight=(SELECT MAX(weight) FROM ttn WHERE `date` BETWEEN '2017.03.01' AND '2017.03.31') ;"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['id_dog', 'company','tel_num','state','address','surname','weight']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros3.html', blanks = res)

@app.route('/zapros4/',methods=['GET','POST'])
def zapros4():
        	conn = db_connect('root','')
        	cursor = conn.cursor()
        	_SQL = """SELECT surname
                    FROM employ LEFT JOIN ttn USING(id_employ)
                    WHERE id IS NULL"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['surname']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros4.html',blanks = res)

@app.route('/zapros5/',methods=['GET','POST'])
def zapros5():
        	conn = db_connect('root','root')
        	cursor = conn.cursor()
        	_SQL = """SELECT surname
                    FROM employ LEFT JOIN(SELECT * FROM ttn
                    WHERE YEAR(`date`)=2017 AND MONTH(`date`)=03) tab USING(id_employ)
                    WHERE id IS NULL;"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['surname']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros5.html',blanks = res)

@app.route('/zapros6/',methods=['GET','POST'])
def zapros6():
        	conn = db_connect('root','root')
        	cursor = conn.cursor()
        	_SQL = """SELECT AVG(weight), MONTH(`date`) AS `Month`
                    FROM ttn
                    WHERE YEAR(`date`)=2017
                    GROUP BY MONTH(`date`)"""
        	cursor.execute(_SQL)
        	result = cursor.fetchall()
        	res = []
        	schema = ['avg weight', 'month']
        	for blank in result:
        		res.append(dict(zip(schema,blank)))
        	return render_template('zapros6.html',blanks = res)

@app.route('/proc/',methods=['GET','POST'])
def proc():

	if 'send' in request.form and request.form['send']=='Отправить':
		conn = db_connect('root', '')
		cursor = conn.cursor()
		month = request.form['month']
		year = request.form['year']
		print('Check 1')
		a = check(month,year)  # Вызвали функцию проверки наличия таких отчетов в БД
		print('a= ',a)
		if (a == 0):  # Таких отчетов нет в БД
			args = (year,month)
			result = cursor.callproc('pupa', args)  # result содержит входные параметры
			conn.commit()
			print('result=',result)
			return 'Отчет успешно создан'
		else:
			return 'Такой отчет уже существует'
	else:
		return render_template('proc.html')


def check(month,year):
	conn = db_connect('root', '')
	cursor = conn.cursor()
	_SQL = """Select count(*) from f_table
	where f_month= %s and f_year=%s"""
	cursor.execute(_SQL,(month,year))
	result = cursor.fetchall()
	a = result[0][0]
	return a


app.run(debug=True)
