from flask import Flask, request, render_template, jsonify
from answer_questions import process_code

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        meridian = 'AM'
        year, month, day = request.form['date'].split('-')
        hour, minute = request.form['hour'].split(':')
        # PM or AM?
        if int(hour) > 11:
            meridian = 'PM'
            # Iqual to 12, ignore it
            if int(hour) != 12:
                hour = str(int(hour) - 12)
                # Numbers with one digit, concatenate zero
                if int(hour) < 10:
                    hour = '0' + hour

        # Usa Selenium para procesar el parametro
        return jsonify(process_code(request.form['code'], day, month, year, hour, minute, meridian))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
