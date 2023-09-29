# Simple Web Service 25.09.2023
import matplotlib
import csv
from flask import Flask, render_template, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
from io import BytesIO

matplotlib.use('Agg')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('survey.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        # Possible to save into database or handle it in some way
        print(f"Name: {name}, Age: {age}")
        save_survey_to_csv(name, age)
        # return to main page
        return redirect(url_for('index'))


def save_survey_to_csv(name, age, filename="survey_data.csv"):
    # Prepare the data to be written
    data_to_write = [name, age]
    # Check if the file exists
    file_exists = False
    try:
        with open(filename, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Write or append data to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)

        # If the file was just created, write the headers
        if not file_exists:
            headers = ['Name', 'Age']
            writer.writerow(headers)

        writer.writerow(data_to_write)

    return "Survey data saved successfully!"


@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'


@app.route('/contact')
def show_my_contacts():
    return '+420776058370, kianushkolosov@gmail.com, Jakutska 423/14, Praha 10'


@app.route('/profile/<username>/<int:age>')
def profile(username, age):
    return render_template('profile.html', user_name=username, age=age)


@app.route('/view_results')
def view_results(filename="survey_data.csv"):
    results = []
    ages = []
    try:
        # Read the data from the CSV file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # skip header
            next(reader, None)
            for row in reader:
                # Assuming 'Name' is the first column and 'Age' is the second column
                results.append({"name": row[0], "age": row[1]})
                ages.append(round(float(row[1])))
    except FileNotFoundError:
        return "No survey results available yet."

    # Generating Histogram
    plt.hist(ages, bins=10, color='blue', edgecolor='black')
    plt.title('Distribution of Ages')
    plt.xlabel('Age')
    plt.ylabel('Number of Participants')

    # Save it to a BytesIO stream
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    output = "<h1>Survey Results:</h1>"
    for result in results:
        output += f"Name: {result['name']} | Age: {result['age']}<br>"

    output += '<h2>Age Histogram:</h2>'
    output += '<img src="/plot.png" alt="Histogram">'
    output += "<br><a href='/'>Back to Survey</a>"
    return output


@app.route('/plot.png')
def plot_png():
    ages = []

    try:
        with open('survey_data.csv', 'r') as file:
            reader = csv.reader(file)
            # skip header
            next(reader, None)
            for row in reader:
                ages.append(int(round(float(row[1]))))
    except FileNotFoundError:
        return "No survey data to plot."

    # Generate the plot and return it
    plt.hist(ages, bins=10, color='blue', edgecolor='black')
    plt.title('Distribution of Ages')
    plt.xlabel('Age')
    plt.ylabel('Number of Participants')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')
