from flask import Blueprint, session, render_template
import uuid
from QuizGame.getQuestions import example_get_questions

main = Blueprint("main", __name__)

# Main route for the host. Tää pitäs ehkä suojata jotenkin, ettei useempi pääse liittymään?
@main.route('/host')
def host():
    return render_template('host.html')

# Route for the players
@main.route('/user')
def user():
    question = example_get_questions()
    # Luodaan uusi id käyttäjälle, jos ei jo ole.
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template("user.html", question=question, user_id=session['user_id'])

