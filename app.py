from flask import Flask, render_template, request
import pandas as pd
import os

# pip install flask pandas

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
data_path = os.path.join(APP_ROOT, 'static', 'pstep.csv')
df = pd.read_csv(data_path)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    unit_number = request.form.get('unitNumber').replace(" ", "").lower()
    all_results = search_unit(unit_number)
    details = [show_details(row) for row in all_results]
    return render_template('index.html', results=all_results, details=details)

def search_unit(unit_number):
    result1 = df[df['Building Number'].astype(str).str.lower().str.cat(df['Unit Number'].astype(str).str.lower(), sep="") == unit_number]
    result2 = df[df['Unit Number'].astype(str).str.lower() == unit_number]
    result3 = df[df['Unit Number'].astype(str).str.lower().str.cat(df['Building Number'].astype(str).str.lower(), sep="") == unit_number]
    result4 = df[df['Building Number'].astype(str).str.lower() == unit_number]

    all_results = pd.concat([result1, result2, result3, result4]).drop_duplicates().to_dict('records')
    return all_results

def show_details(unit_row):
    details_list = []
    fields = [
        ('Address Line 1', 'Address: line1'),
        ('Address Line 2', 'Address: line2'),
        ('Site', 'Site'),
        ('Building Number', 'Building Number'),
        ('Unit Number', 'Unit Number'),
    ]
    
    for label, column in fields:
        if not pd.isna(unit_row.get(column, '')):
            details_list.append(f"{label}: {unit_row[column]}")
    
    return "\n".join(details_list)

#if __name__ == '__main__':
#    app.run(debug=True)
