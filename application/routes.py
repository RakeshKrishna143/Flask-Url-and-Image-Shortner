from application import app
from flask import render_template,redirect,session,url_for,abort
from application.forms import UrlShortnerForm,ImageShortenForm
import os
import json
from werkzeug.utils import secure_filename
@app.route('/')
@app.route('/index')
def index():
    form1 = UrlShortnerForm()
    form2 = ImageShortenForm()
    return render_template('index.html',form1=form1,form2=form2,codes=session.keys())

@app.route('/your-url',methods=['GET','POST'])
def your_url():
    form1 = UrlShortnerForm()
    form2 = ImageShortenForm()
    urls = {}
    code = ''
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
    if form1.validate_on_submit():
        url = form1.url.data 
        code = form1.code.data   
        if code in urls.keys():
            flash('The code is already taken')
            return redirect('/index')
        else:
            urls[code] = {'url':url}
            with open('urls.json','w') as urls_file:
                json.dump(urls,urls_file)
                session[code] = True
    if form2.validate_on_submit():
        file = form2.file.data 
        code = form2.code.data 
        if code in urls.keys():
            flash('The code is already taken')
            return redirect('/index')
        else:
            full_name = code + secure_filename(file.filename)
            file.save('C:/Users/Rakesh/Desktop/Url Shortner/application/static/images/'+full_name)
            urls[code] = {'file':full_name}
            with open('urls.json','w') as urls_file:
                json.dump(urls,urls_file)
                session[code] = True
    return render_template('your_url.html',code=code)

@app.route('/<code>')

def return_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)

        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                return redirect(url_for('static',filename='images/'+urls[code]['file']))
    return abort(404)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
@app.route('/api')
def api():
    return jsonify(list(session.keys()))