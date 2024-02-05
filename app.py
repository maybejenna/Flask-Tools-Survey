from flask import Flask, request, redirect, render_template

from surveys import satisfaction_survey 

app = Flask(__name__)

responses = []

@app.route("/")
def home_route(): 
    return render_template("home_page.html")

@app.route("/satisfaction_survey")
def show_survey_start_page():
    # Pass survey title and instructions to the template
    return render_template("satisfaction_survey.html", 
                           survey=satisfaction_survey)

@app.route("/questions/<int:question_id>")
def show_question(question_id):
    if question_id != len(responses):
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[question_id]
    return render_template("question.html", question=question)

@app.route("/answer", methods=["POST"])
def handle_answer():
    # Get the selected answer from the form data
    selected_answer = request.form['answer']

    # Append the answer to the responses list
    responses.append(selected_answer)

    # Check if the survey is complete
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")  # Redirect to a thank you page
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/thankyou")
def thank_you():
    return render_template("thank_you.html")