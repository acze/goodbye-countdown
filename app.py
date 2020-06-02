from flask import Flask,render_template
import datetime
from datetime import timedelta,date

app = Flask(__name__)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def justday(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def secondsleft(employees,now):
    seconds_left = {}
    for employee in employees:
        time_to_work = 0
        #last day
        if justday(now) == justday(employee["date"]):
            if(now.hour < now.replace(hour=8, minute=0, second=0, microsecond=0).hour):
                time_to_work = 8 * 60 * 60
            else:
                time_to_work = int((now.replace(hour=16, minute=0, second=0, microsecond=0) - now) / timedelta(seconds=1))
        else:
            for single_date in daterange(now, employee["date"]):
                single_date_day = justday(single_date)
                #exclude weekends and vacations
                if not(single_date.weekday() in [5,6] or single_date_day in employee["excluded"]):
                    #today
                    if single_date_day == justday(now):
                        timeslice = int((now.replace(hour=16, minute=0, second=0, microsecond=0) - now) / timedelta(seconds=1))
                        if timeslice >= 0:
                            time_to_work += timeslice
                    else:
                        time_to_work += 8 * 60 * 60
        seconds_left[employee["name"]] = time_to_work
        print("{} has {} seconds of work left".format(employee["name"],time_to_work))
    return seconds_left

@app.route('/')
def index():
    employees = [
        {
            "name" : "Marek",
            "date" : datetime.datetime(2020, 6, 30, 16, 0, 0),
            "excluded" : [
            datetime.datetime(2020, 6, 19),
            datetime.datetime(2020, 6, 22),
            datetime.datetime(2020, 6, 23),
            datetime.datetime(2020, 6, 24),
            datetime.datetime(2020, 6, 25),
            datetime.datetime(2020, 6, 26)
            ]
        },
        {
            "name": "Szymon",
            "date" : datetime.datetime(2020, 6, 30, 16, 0, 0),
            "excluded": []
        },
        {
            "name": "Adam",
            "date" : datetime.datetime(2020, 8, 31, 16, 0, 0),
            "excluded": []
        },
        {
            "name": "Szczepan",
            "date" : datetime.datetime(2020, 6, 30, 16, 0, 0),
            "excluded": []
        }
    ]

    now = datetime.datetime.now()
    return render_template('index.html',secondsleft=secondsleft(employees,now))

if __name__ == '__main__':
    app.run(debug=True)