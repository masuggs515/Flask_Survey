from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


responses = []

@app.route('/')
def home_page():
    return render_template('base.html', survey = satisfaction_survey)

@app.route('/begin', methods=["POST"])
def redirect_to_start():
    responses.clear()
    return redirect('/questions/0')

@app.route('/questions/<int:num>')
def question_pages(num):
    if (responses is None):
        return redirect('/')
    if len(responses) != num:
        if len(responses) == 0:
            flash(f'You have not started the survey yet.', 'error')
            return redirect('/')
        flash(f'Invalid question of id: {num} You are on question {len(responses)}.', 'error')
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[num]
    return render_template('questions.html', question = question)



@app.route('/answer', methods=['POST'])
def add_answer():

    answer = request.form['answer']

    responses.append(answer)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    return redirect(f'/questions/{len(responses)}')


@app.route('/complete')
def done_with_survey():
    return render_template('complete.html', responses=responses)