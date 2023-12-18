from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

app.secret_key = 'Qazxswedcvfrtgbnhy'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snippet_input', methods=['GET', 'POST'])
def snippet_input():
    if request.method == 'POST':
        snippet = request.form['code_snippet']
        session['code_snippet'] = snippet  # Save snippet to session
        return redirect(url_for('practice'))
    return render_template('snippet_input.html')

@app.route('/practice')
def practice():
    snippet = session.get('code_snippet', '')
    attempt_count = session.get('attempt_count', 0)

    # Redirect to the final challenge after 3 attempts
    if attempt_count >= 3:
        return redirect(url_for('final_challenge'))

    return render_template('practice.html', code_snippet=snippet, attempt_number=attempt_count + 1)

@app.route('/check_attempt', methods=['POST'])
def check_attempt():
    user_attempt = request.form.get('user_attempt')
    correct_snippet = session.get('code_snippet', '')
    attempt_count = session.get('attempt_count', 0)

    if user_attempt == correct_snippet:
        session['attempt_count'] = attempt_count + 1
        return redirect(url_for('practice'))
    else:
        return redirect(url_for('error'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/final_challenge')
def final_challenge():
    # Reset the attempt count or perform any other cleanup
    session.pop('attempt_count', None)
    return render_template('final_challenge.html')

@app.route('/submit_final_challenge', methods=['POST'])
def submit_final_challenge():
    user_attempt = request.form.get('user_attempt_final')
    correct_snippet = session.get('code_snippet', '')

    if user_attempt == correct_snippet:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('error'))

@app.route('/continue')
def continue_practice():
    # Reset the session or provide options
    session.pop('code_snippet', None)
    session.pop('attempt_count', None)
    return render_template('continue.html')

if __name__ == '__main__':
    app.run(debug=True)
