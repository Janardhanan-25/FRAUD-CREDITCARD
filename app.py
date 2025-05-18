from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        card_number = request.form['card_number']
        amount = float(request.form['amount'])
        location = request.form['location']
        time = request.form['time']

        if amount > 10000:
            session['blocked_card'] = True
            session['card_number'] = card_number
            return redirect(url_for('puzzle'))
        else:
            return render_template('result.html', result='Safe Transaction')

    return render_template('index.html')

@app.route('/puzzle', methods=['GET', 'POST'])
def puzzle():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == '8':
            session['blocked_card'] = False
            return redirect(url_for('unblock'))
        else:
            error = "Incorrect! Try again."
            return render_template('puzzle.html', error=error)
    return render_template('puzzle.html')

@app.route('/unblock')
def unblock():
    if 'blocked_card' in session and not session['blocked_card']:
        return render_template('result.html', result='Card Unblocked')
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
