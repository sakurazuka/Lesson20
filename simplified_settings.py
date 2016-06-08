# coding=utf-8
from bottle import static_file,request,post,HTTPError,redirect,response
from bottle import route,template,run
import sqlite3
from datetime import date
import os,os.path, sys
sys.path.append(os.path.abspath('./libs'))
from gviz_api_py.gviz_api  import DataTable

@route('/', 'GET')
@route('/list', 'GET')
def simplified_list():
	db = sqlite3.connect('./db/test.db').cursor()
	rows=db.execute('SELECT * from users').fetchall()
	db.close()
	return template('./views/simplified_list.html',rows=rows)
	
@route('/edit', 'GET')
def simplified_edit():
	params={'account_name':unicode(request.query['account_name'],'utf-8'),'user_photo':'','submit_type':'更新'}
	db = sqlite3.connect('./db/test.db').cursor()
	row=db.execute('SELECT * from users where account_name=?', (params['account_name'],)).fetchone()
	if row and len(row)==2:
		params['account_name']=row[0]
		params['user_photo']=row[1]
	db.close()
			
	return template('./views/simplified_settings.html',params)

@route('/edit', 'POST')
def simplified_edit_post():
	#POSTで渡されたリクエストパラメータの値を取得
	params={'account_name':unicode(request.forms.get('account_name',''),'utf-8'),
	'bfr_account_name':unicode(request.forms.get('bfr_account_name',''),'utf-8'),
	'submit_type':'更新'}

    #POSTで渡されたファイル情報を取得
	photo=request.files.get('photo')  
	if photo and photo.filename:
		photo.save('./upload',overwrite=True) 
		params['user_photo']='./upload/'+photo.filename
		conn = sqlite3.connect('./db/test.db')
		db=conn.cursor()
		db.execute('''UPDATE users set account_name= ? , user_photo = ?  where account_name=?''',
			(params['account_name'], params['user_photo'], params['bfr_account_name'],))
		conn.commit()
		db.close()
	return redirect('/list')	

@route('/insert', 'GET')
def simplified_insert():
	return template('./views/simplified_settings.html', {'url':'./insert','submit_type':'登録'})	

@route('/insert', 'POST')
def simplified_insert():
	#POSTで渡されたリクエストパラメータの値を取得
	params={'account_name':unicode(request.forms.get('account_name',''),'utf-8'),'submit_type':'登録'}

    #POSTで渡されたファイル情報を取得
	photo=request.files.get('photo')  
	if photo and photo.filename:
		photo.save('./upload',overwrite=True) 
		params['user_photo']='./upload/'+photo.filename
		conn = sqlite3.connect('./db/test.db')
		db=conn.cursor()
		db.execute('''INSERT  INTO users  (account_name, user_photo ) values (?,?) ''',
		 (params['account_name'], params['user_photo'], ))
		conn.commit()
		db.close()

	return redirect('/list')	

@route('/delete', 'POST')
def simplified_delete():
	#POSTで渡されたリクエストパラメータの値を取得
	params={'account_name':unicode(request.forms.get('account_name'),'utf-8')}
	conn = sqlite3.connect('./db/test.db')
	db=conn.cursor()
	row=db.execute('SELECT * from users where account_name=?', (params['account_name'],)).fetchone()
	if row and len(row)==2:
		user_photo=row[1]
		if os.path.isfile(user_photo):
			os.remove(user_photo) 
	db.execute('''DELETE  FROM users  WHERE account_name=?''',
	 (params['account_name'], ))	
	conn.commit()
	db.close()

	return redirect('/list')	

@route('/bmi', 'GET')
def simplified_bmi():
	params={'account_name':unicode(request.query['account_name'],'utf-8')}
	db = sqlite3.connect('./db/test.db').cursor()
	row=db.execute('SELECT * from users where account_name=?', (params['account_name'],)).fetchone()
	db.close()
	if row:
		params['user_photo']=row[1]
		
		return template('./views/simplified_bmi.html',params) 
		
	return HTTPError(404, 'Page not found')

@route('/api/bmi','GET')
def simplified_api_bmi():
	description={'date':('date',u'日付'), 'bmi':('number',u'BMI')}
	data = []
	data.append({'date':date(2013,7,1),'bmi':21.4})
	data.append({'date':date(2013,8,1),'bmi':22.4})
	data.append({'date':date(2013,9,1),'bmi':22.7})
	data.append({'date':date(2013,10,01),'bmi':23.1})
	
	data_table = DataTable(description)
	data_table.LoadData(data)
	response.content_type = 'application/json; charset=utf-8'
	req_id=0
	if 'tqx' in request.query:
		tqx=request.query['tqx']
		if  tqx:
			req_id=dict([p.split(':') for p in tqx.split(';')]).get('reqId', req_id)

	return data_table.ToJSonResponse(columns_order=("date", "bmi"),req_id=req_id)

@route('/api/bmidb','GET')
def simplified_api_bmidb():
	params={'account_name':unicode(request.query['account_name'],'utf-8')}
	description={'date':('date',u'日付'), 'bmi':('number',u'BMI')}
	data = []
	db = sqlite3.connect('./db/test.db').cursor()
	rows=db.execute(
	'''SELECT  bmi, date from bmi_data where account_name=? 
	order by DATE(date)''', (params['account_name'],)).fetchall()
	db.close()
	
	for row in rows:
		[yyyy,mm,dd]=map(int,row[1].split('-',))
		data.append({'date':date(yyyy,mm,dd),'bmi':row[0]})
	
	data_table = DataTable(description)
	data_table.LoadData(data)
	response.content_type = 'application/json; charset=utf-8'
	req_id=0
	if 'tqx' in request.query:
		tqx=request.query['tqx']
		if  tqx:
			req_id=dict([p.split(':') for p in tqx.split(';')]).get('reqId', req_id)

	return data_table.ToJSonResponse(columns_order=("date", "bmi"),req_id=req_id)

@route('/<directory>/<filename:re:.*\.(png|jpg|jpeg|gif)>')
def upload_file(directory, filename):
	if directory in ('images','upload'): 
		return static_file(filename, root=directory,mimetype='image/*')
	return HTTPError(404, 'Page not found')

run(host='localhost', port=8080, debug=True )