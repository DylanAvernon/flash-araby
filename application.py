import os
import pyarabic.araby as araby
import requests

from bs4 import BeautifulSoup
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


dbv = SQL("sqlite:///verbs.db")


@app.route("/")
@login_required
def index():
    
    user = session["user_id"]
    verbs = []
    
    # Queries the database for all verbs that the current user is studying. 
    # Handles error that occurs when the query is invalid, for example there are no verbs. 
    try:
        dbv.execute("SELECT verb FROM base WHERE generated_id IN (SELECT verb_id FROM vocabulary WHERE user_id = :user)", user=user)
    except:
        verbs = []
    else:
        verbs = dbv.execute("SELECT verb FROM base WHERE generated_id IN (SELECT verb_id FROM vocabulary WHERE user_id = :user)", user=user)
        
    return render_template("index.html", verbs=verbs)
        
@app.route("/login", methods=["GET", "POST"])
def login():
    
    # Forget an previous user id.
    session.clear()
    
    if request.method == "POST":
        
        # Get user information from HTML forms.
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("alt_apology.html", message="All fields must be filled")
        
        # Check if the retrieved information matches a known user.
        row = dbv.execute("SELECT * FROM users WHERE username = :username",username=username)
        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
                return render_template("alt_apology.html", message="Invalid username or password")
        
        # Create the session for the user.
        session["user_id"] = row[0]["user_id"]
        
        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    # Get user inputs.
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    
    # Check if fields are empty.
    if not username or not password or not confirmation:
        return render_template("alt_apology.html", message="All fields must be filled")
        
    # Check if passwords match.
    if password != confirmation:
        return render_template("alt_apology.html", message="Passwords do not match")
    
    # Check if name and email already exist in the database.
    match = dbv.execute("SELECT user_id FROM users WHERE username = :username", username=username)
    if len(match) > 0:
        return render_template("alt_apology.html", message="That username has already been used.")
    
    hashed = generate_password_hash(password)
        
    # If all checks are passed, insert name and email into the database.
    dbv.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)
    
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    
    user = session["user_id"]
    
    if request.method == "GET":
        verbs = dbv.execute("SELECT verb FROM base WHERE generated_id IN (SELECT verb_id FROM vocabulary WHERE user_id = :user)", user=user)
        return render_template("search.html", verbs=verbs)
    
    # Lists of possible user specifications.
    tenses = ["past", "present"]
    persons = ["1st", "2nd", "3rd"]
    numbers = ["singular", "plural", "dual"]
    genders = ["masculine", "feminine", "neutral"]
    
    # Arrays for holding the results of database searches.
    forms_verbs = []
    forms_pronouns = []
    
    # Get user specifications from html form.
    html_verb = request.form.get("verb")
    input_tenses = request.form.getlist("tenses")
    input_persons = request.form.getlist("persons")
    input_numbers = request.form.getlist("numbers")
    input_genders = request.form.getlist("genders")
    
    # Check that the user specified a verb.
    if html_verb == None:
        return render_template("apology.html", message="You must choose a verb")

    # Check that the user's input consists only of Arabic characters and tashkeel.
    for char in html_verb:
        if (char not in araby.LETTERS) and (char not in araby.TASHKEEL):
            return render_template("apology.html", message="This program only supports Arabic characters, shadda, and vowel markers")
    
    # Check if user provided a specification. If not, specification is set to all possible verb forms.
    if len(input_tenses) == 0:
        for tense in tenses:
            input_tenses.append(tense)
    
    if len(input_persons) == 0:
        for person in persons:
            input_persons.append(person)
    
    if len(input_numbers) == 0:
        for number in numbers:
            input_numbers.append(number)
    
    if len(input_genders) == 0:
        for gender in genders:
            input_genders.append(gender)
    
    # Get verb conjugation table from reverso.
    response = requests.get(f"https://conjugator.reverso.net/conjugation-arabic-verb-{html_verb}.html")
    if response.ok == False:
        return render_template("apology.html", message="That verb doesn't exist")
    
    # Create soup object for html parsing
    soup = BeautifulSoup(response.text, "html.parser")
            
    # Extract verb forms from the html file.
    verb_forms = soup.find_all(class_="verbtxt-term")
    
    # Ensure that the verb used in the tests matches the encoding of the verb stored in the DB.
    soup_verb = verb_forms[6].get_text()
    
    # Loop through the database searching for all verb forms that match the user's specifications.
    # Genertes the full verb table if no specifications are provided.
    for tense in input_tenses:
        for person in input_persons:
            for number in input_numbers:
                for gender in input_genders:
                    try:
                        dict_entries = dbv.execute(f"SELECT {tense}_{person}_{number}_{gender}.verb FROM {tense}_{person}_{number}_{gender} WHERE {tense}_{person}_{number}_{gender}.id = (SELECT generated_id FROM base WHERE verb = :soup_verb)", soup_verb=soup_verb)
                        pron_entries = dbv.execute(f"SELECT {tense}_{person}_{number}_{gender}.pronoun FROM {tense}_{person}_{number}_{gender} WHERE {tense}_{person}_{number}_{gender}.id = (SELECT generated_id FROM base WHERE verb = :soup_verb)", soup_verb=soup_verb)    
                    except:
                        continue
                    else:
                        forms_verbs.append(list(dict_entries[0].values()))
                        forms_pronouns.append(list(pron_entries[0].values()))
    
    # Check that the verb form exists.
    if len(forms_verbs) == 0:
        return render_template("apology.html", message="Sorry but that verb form does not exist. Try making a new deck.")
    
    return render_template("study.html", forms_verbs=forms_verbs, forms_pronouns=forms_pronouns)
       
        
@app.route("/verbentry", methods=["GET", "POST"])
@login_required
def verbentry():
    
    user = session['user_id']
    
    if request.method == "GET":
        return render_template("verbentry.html")
        
    # Store users input in a variable.
    html_verb = request.form.get("verb")
    
    # Check that the user's input consists only of Arabic characters and tashkeel.
    for char in html_verb:
        if (char not in araby.LETTERS) and (char not in araby.TASHKEEL):
            return render_template("apology.html", message="This program only supports Arabic characters, shadda, and vowel markers")
    
    # Get verb conjugation table from reverso.
    response = requests.get(f"https://conjugator.reverso.net/conjugation-arabic-verb-{html_verb}.html")
    if response.ok == False:
        return render_template("apology.html", message="That verb doesn't exist")
    
    # Create soup object for html parsing
    soup = BeautifulSoup(response.text, "html.parser")
            
    # Extract verb forms from the html file.
    pronouns = soup.find_all(class_="graytxt")
    verb_forms = soup.find_all(class_="verbtxt-term")
    
    # Ensure that the verb used in the tests matches the encoding of the verb stored in the DB.
    soup_verb = verb_forms[6].get_text()
    
    # Check if the user's input has already been entered into the database.
    matchdb = dbv.execute("SELECT generated_id FROM base WHERE verb = :verb", verb=soup_verb)
    if len(matchdb) != 0:
        verb_id = matchdb[0]['generated_id']
        idmatch = dbv.execute("SELECT generated_id FROM base WHERE generated_id IN (SELECT verb_id FROM vocabulary WHERE user_id = :user) AND generated_id = :verb_id", user=user, verb_id=verb_id)
        if len(idmatch) != 0:
            return render_template("apology.html", message="This verb is already in your learner profile")
        else:
            dbv.execute("INSERT INTO vocabulary VALUES(?, ?)", verb_id, user)
            return redirect("/search")
            
    # Insert base element into base table of the database.
    dbv.execute('''INSERT INTO base VALUES(?, ?)''', None, verb_forms[6].get_text())
            
    # Store primary id in a variable for linking other tables to base table.
    primary_id = dbv.execute('''SELECT generated_id FROM base WHERE verb=?''', verb_forms[6].get_text())
    
    # # # # # # # # # # # # # # # # # # # # # # # # # #
    #Insert verb forms and pronouns into the database.#
    # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Past verb forms.
    dbv.execute("INSERT INTO past_1st_singular_neutral VALUES(?, ?, ?)", pronouns[0].get_text(), verb_forms[0].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO past_1st_plural_neutral VALUES(?, ?, ?)", pronouns[16].get_text(), verb_forms[16].get_text(), primary_id[0]['generated_id'])
    
    
    dbv.execute("INSERT INTO past_2nd_singular_masculine VALUES(?, ?, ?)", pronouns[2].get_text(), verb_forms[2].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO past_2nd_singular_feminine VALUES(?, ?, ?)", pronouns[4].get_text(), verb_forms[4].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO past_2nd_dual_neutral VALUES(?, ?, ?)", pronouns[10].get_text(), verb_forms[10].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO past_2nd_plural_masculine VALUES(?, ?, ?)", pronouns[18].get_text(), verb_forms[18].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO past_2nd_plural_feminine VALUES(?, ?, ?)", pronouns[20].get_text(), verb_forms[20].get_text(), primary_id[0]['generated_id'])
    
    
    dbv.execute("INSERT INTO past_3rd_singular_masculine VALUES(?, ?, ?)", pronouns[6].get_text(), verb_forms[6].get_text(), primary_id[0]['generated_id'] )
    dbv.execute("INSERT INTO past_3rd_singular_feminine VALUES(?, ?, ?)", pronouns[8].get_text(), verb_forms[8].get_text(), primary_id[0]['generated_id'] )
    dbv.execute("INSERT INTO past_3rd_dual_masculine VALUES(?, ?, ?)", pronouns[12].get_text(), verb_forms[12].get_text(), primary_id[0]['generated_id'] )
    dbv.execute("INSERT INTO past_3rd_dual_feminine VALUES(?, ?, ?)", pronouns[14].get_text(), verb_forms[14].get_text(), primary_id[0]['generated_id'] )
    dbv.execute("INSERT INTO past_3rd_plural_masculine VALUES(?, ?, ?)", pronouns[22].get_text(), verb_forms[22].get_text(), primary_id[0]['generated_id'] )
    dbv.execute("INSERT INTO past_3rd_plural_feminine VALUES(?, ?, ?)", pronouns[24].get_text(), verb_forms[24].get_text(), primary_id[0]['generated_id'])
    

    # Present verb forms.
    dbv.execute("INSERT INTO present_1st_singular_neutral VALUES(?, ?, ?)", pronouns[26].get_text(), verb_forms[26].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_1st_plural_neutral VALUES(?, ?, ?)", pronouns[42].get_text(), verb_forms[42].get_text(), primary_id[0]['generated_id'])
    

    dbv.execute("INSERT INTO present_2nd_singular_masculine VALUES(?, ?, ?)", pronouns[28].get_text(), verb_forms[28].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_2nd_singular_feminine VALUES(?, ?, ?)", pronouns[30].get_text(), verb_forms[30].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_2nd_dual_neutral VALUES(?, ?, ?)", pronouns[36].get_text(), verb_forms[36].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_2nd_plural_masculine VALUES(?, ?, ?)", pronouns[44].get_text(), verb_forms[44].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_2nd_plural_feminine VALUES(?, ?, ?)", pronouns[46].get_text(), verb_forms[46].get_text(), primary_id[0]['generated_id'])
    

    dbv.execute("INSERT INTO present_3rd_singular_masculine VALUES(?, ?, ?)", pronouns[32].get_text(), verb_forms[32].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_3rd_singular_feminine VALUES(?, ?, ?)", pronouns[34].get_text(), verb_forms[34].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_3rd_dual_masculine VALUES(?, ?, ?)", pronouns[38].get_text(), verb_forms[38].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_3rd_dual_feminine VALUES(?, ?, ?)", pronouns[40].get_text(), verb_forms[40].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_3rd_plural_masculine VALUES(?, ?, ?)", pronouns[48].get_text(), verb_forms[48].get_text(), primary_id[0]['generated_id'])
    dbv.execute("INSERT INTO present_3rd_plural_feminine VALUES(?, ?, ?)", pronouns[50].get_text(), verb_forms[50].get_text(), primary_id[0]['generated_id'])
    
    dbv.execute("INSERT INTO vocabulary VALUES(?, ?)", primary_id[0]['generated_id'], user)
    
    return redirect("/search")
    
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    
    user = session["user_id"]
    
    if request.method == "GET":
        verbs = dbv.execute("SELECT verb FROM base WHERE generated_id IN (SELECT verb_id FROM vocabulary WHERE user_id = :user)", user=user)
        return render_template("delete.html", verbs=verbs)
    
    verb = request.form.get("verb")
    
    # Check that the user specified a verb.
    if verb == None:
        return render_template("apology.html", message="You must choose a verb")
        
    dbv.execute("DELETE FROM vocabulary WHERE verb_id = (SELECT generated_id FROM base WHERE verb = :verb) AND user_id = :user", verb=verb, user=user)
    
    return redirect("/delete")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("alt_apology.html", message="An error occured")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

        
