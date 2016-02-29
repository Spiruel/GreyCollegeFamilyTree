from flask import Flask, render_template, request, flash, redirect
import myfamilytree as ft
import register as reg
import re

app = Flask(__name__)
app.secret_key = 'some_secret'

import logging
from logging.handlers import SMTPHandler

file_handler = logging.FileHandler(filename='grey_error.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    global name, html_content
    if request.method == 'GET':
        id = request.args.get('id')
        if id is None:
            return render_template('index.html')
        else:
            return get_html_content(id=id)
    elif request.method == 'POST':
        form_text = request.form['text']
        return get_html_content(name=form_text)
    
def get_html_content(name=None, id=None):
    if id is None:
        if ft.get_person(name=name) == []:
            print 'Could not find person!', name
            error = 'Could not find person.'
            flash(error)
            return render_template('index.html', error=error)
        else:
            start_node = ft.get_person(name=name)[0]
            print 'Found person,', start_node.get_name() + ', making tree.'
            html_content = ft.main(start_node=start_node)
            name = name='Genogram for ' + start_node.get_name() +'.'
            return html_content
    if id is not None:
        if ft.get_person(id=id) == []:
            print 'Could not find person!', id
            error = 'Could not find person.'
            flash(error)
            return redirect('/', code=303)
        else:
            start_node = ft.get_person(id=id)[0]
            print 'Found person,', start_node.get_name() + ', making tree.'
            html_content = ft.main(start_node=start_node)
            name = name='Genogram for ' + start_node.get_name() +'.'
            return html_content
        
@app.route('/register.html')
def register():
    return render_template('register.html')
    
@app.route('/about.html')
def about():
    raise Exception('Deliberate exception raised')
    return render_template('about.html')
    
@app.route('/register.html', methods=['POST'])
def reg_form_post():
    parent1 = request.form['partner1']
    parent2 = request.form['partner2']
    child1 = request.form['child1']
    child2 = request.form['child2']
    familylist = [parent1, parent2, child1, child2]
    pattern = re.compile("^[a-z]{4}\d{2}$")
    for i in familylist:
        if bool(pattern.match(i)) is False:
            return render_template('confirm.html', alert='Error: Please enter a valid CIS username.')
    print familylist
    alert = reg.process(familylist)
    print 'Received family registration!' ,parent1,parent2,child1,child2
    return render_template('confirm.html', alert=alert)
    
@app.route('/confirm/', methods=['GET'])
def confirm():
    if request.method == 'GET':
        id = request.args.get('token')
        tok = reg.confirm_token(id)
        if id is not None and tok is not False:
	    user, randid = tok[:6], tok[6:]
            print 'Successfully got token!', user, randid
            alert = reg.confirm_registration(str(user), str(randid))
            return render_template('confirm.html', alert=alert)
        else:
            return render_template('confirm.html', error='Error: Something is wrong. Maybe the verification links have expired?')
    return render_template('index.html')
  
if __name__ == '__main__':
    app.debug = True
    #app.run(host='0.0.0.0')
    app.run()
    redirect('index.html')

app.debug = True
ft.readdata()
name = ''
html_content = ft.main()
