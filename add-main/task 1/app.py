from flask import Flask, render_template, request, redirect, url_for, flash
import pickle

app = Flask(__name__)
app.secret_key = "supersecretkey"

# File to store numbers using pickle
PICKLE_FILE = 'numbers.pkl'

# Function to load numbers from pickle file
def load_numbers():
    try:
        with open(PICKLE_FILE, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

# Function to save numbers to pickle file
def save_numbers(numbers):
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(numbers, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get numbers from form input
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
        except ValueError:
            flash("Please enter valid numbers", "error")
            return redirect(url_for('index'))

        # Perform addition
        result = num1 + num2

        # Load existing numbers and add new result
        numbers = load_numbers()
        numbers.append((num1, num2, result))
        save_numbers(numbers)

        flash(f"Result of {num1} + {num2} = {result}", "success")
        return redirect(url_for('index'))

    # Display stored numbers
    numbers = load_numbers()
    return render_template('index.html', numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)
