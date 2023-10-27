# Modified app.py based on the pseudocode for troubleshooting and fixing the application

# Step 1: Check Imports and Dependencies
from flask import Flask, render_template, request, jsonify
import pandas as pd

# Step 2: Validate Data File
# Assuming pstep.csv is in the same directory as app.py for this example. If not, provide the full path.
data_path = "pstep.csv"
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    df = pd.DataFrame()  # Empty DataFrame if file not found

# Step 3: Examine Routes
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search_unit():
    # Step 4: Form Data Handling
    unit_number = request.form.get('unit_number', '').replace(" ", "").lower()
    
    if not unit_number:
        return jsonify({"error": "Unit number is missing"}), 400
    
    # Step 5: Data Query
    if df.empty:
        return jsonify({"error": "Data file missing or empty"}), 500
    
    try:
        # Assuming columns 'Building Number' and 'Unit Number' exist in the DataFrame
        query_string = df['Building Number'].astype(str).str.lower() + df['Unit Number'].astype(str).str.lower()
        result = df[query_string == unit_number]
        
        if result.empty:
            return jsonify({"error": "Unit not found"}), 404
        
        return jsonify(result.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Running the application
if __name__ == '__main__':
    app.run(debug=True)
