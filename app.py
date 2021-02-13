from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False




@app.route('/')
def home_page():
    return render_template('base.html', survey = satisfaction_survey)

@app.route('/begin', methods=["POST"])
def redirect_to_start():
    if session.get("responses", False):
        if len(session["responses"]) == len(satisfaction_survey.questions):
            return redirect('/complete')
    else:
        session["responses"] = []
        return redirect('/questions/0')

@app.route('/questions/<int:num>')
def question_pages(num):
    responses = session['responses']
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    if len(responses) != num:
        if len(responses) == 0:
            flash(f'You have not started the survey yet.', 'error')
            return redirect('/')
        flash(f'Invalid questions request. You are on question {len(responses) +1}.', 'error')
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[num]
    return render_template('questions.html', question = question)



@app.route('/answer', methods=['POST'])
def add_answer():

    answer = request.form['answer']

    responses = session['responses']

    responses.append(answer)
    session['responses'] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    return redirect(f'/questions/{len(responses)}')


@app.route('/complete')
def done_with_survey():
    return render_template('complete.html',question=satisfaction_survey.questions , responses=session['responses'])