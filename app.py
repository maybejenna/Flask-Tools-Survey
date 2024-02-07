from flask import Flask, request, redirect, render_template, flash, session, make_response
from surveys import satisfaction_survey
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'randomsecretkey'

@app.route("/")
def home_route():
    if request.cookies.get('survey_completed') == 'yes':
        return render_template("already_completed.html")
    else:
        return render_template("home_page.html")

@app.route("/start", methods=["POST"])
def start_survey():
    session["responses"] = []
    # You might want to also reset the survey completion status here, if applicable.
    session['completed'] = False
    resp = make_response(redirect("/questions/0"))
    resp.set_cookie('survey_done', '', expires=0)  # Optionally clear the survey_done cookie
    return resp

@app.route("/satisfaction_survey")
def show_survey_start_page():
    return render_template("satisfaction_survey.html", survey=satisfaction_survey)

@app.route("/questions/<int:question_id>")
def show_question(question_id):
    responses = session.get("responses", [])
    if question_id != len(responses):
        flash('You’re trying to access an invalid question.')
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[question_id]
    return render_template("question.html", question=question)

@app.route("/answer", methods=["POST"])
def handle_answer():
    current_responses = session.get("responses", [])
    selected_answer = request.form['answer']
    current_responses.append(selected_answer)
    session["responses"] = current_responses
    if len(current_responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{len(current_responses)}")

@app.route("/thankyou")
def thank_you():
    response = make_response(render_template("thank_you.html"))
    expires = datetime.now() + timedelta(days=365)
    response.set_cookie('survey_completed', 'yes', expires=expires)
    return response