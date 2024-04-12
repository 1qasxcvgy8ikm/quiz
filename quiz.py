from random import randint,shuffle
from flask import Flask, session, redirect, url_for, request, render_template
from db_scripts import get_question_after,get_quizes,check_answer
import os

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)
def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['total'] = 0
    session['answers'] = 0
def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id,answer):
        session['answers'] += 1
def question_form (question):
    answers_list = [question[2],question[3],question[4],question[5]]
    shuffle(answers_list)
    return render_template(
    'test.html',question = question[1],quest_id = question[0],answers_list = answers_list
    )
def index ():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return redirect(url_for('test'))
def test ():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(result)
def result ():
    html = render_template('result.html',right = session['answers'],total = session['total'])
    session.clear()
    return html

folder = os.getcwd()
app = Flask(__name__,template_folder=folder,static_folder=folder)
app.config['SECRET_KEY'] = 'VeryStrongKey'
app.add_url_rule('/','index',index,methods = ['POST','GET'])
app.add_url_rule('/test','test',test,methods = ['POST','GET'])
app.add_url_rule('/result','result',result,methods = ['POST','GET'])
app.run()