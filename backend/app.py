from flask import Flask, jsonify, send_from_directory, make_response
import pandas as pd
import numpy as np
import json, os

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, 'titanic.csv'))

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}


def cors(data, status=200):
    resp = make_response(jsonify(data), status)
    for k, v in CORS_HEADERS.items():
        resp.headers[k] = v
    return resp

# Handle preflight OPTIONS for all /api/ routes
@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    resp = make_response('', 204)
    for k, v in CORS_HEADERS.items():
        resp.headers[k] = v
    return resp

# Handler for GET requests for /api/stats routes
@app.route('/api/stats')
def stats():
    # parses json file to a dictionary
    with open(os.path.join(BASE_DIR, 'stats.json')) as f:
        data = json.load(f)
    # ensures keys are integers so frontend recieves numbers instead of text, since JSON keys are always strings
    data['class_breakdown'] = {int(k): v for k, v in data['class_breakdown'].items()}
    data['class_survival_rates'] = {int(k): v for k, v in data['class_survival_rates'].items()}
    return cors(data)

# returns metadata about charts
@app.route('/api/charts')
def charts():
    chart_files = [
        {'id': 'survival_by_class',   'title': 'Survival by Passenger Class',     'file': 'survival_by_class.png'},
        {'id': 'age_distribution',    'title': 'Age Distribution by Survival',     'file': 'age_distribution.png'},
        {'id': 'survival_by_sex',     'title': 'Survival Rate by Gender',          'file': 'survival_by_sex.png'},
        {'id': 'fare_distribution',   'title': 'Fare Distribution (Log Scale)',    'file': 'fare_distribution.png'},
        {'id': 'survival_by_embark',  'title': 'Survival by Port of Embarkation', 'file': 'survival_by_embark.png'},
        {'id': 'correlation_heatmap', 'title': 'Feature Correlation Heatmap',     'file': 'correlation_heatmap.png'},
    ]
    # Add new key value pair for each chart based on its filename (url : /static/charts/filename.png)
    for c in chart_files:
        c['url'] = f"/static/charts/{c['file']}"
    return cors(chart_files)

# Handles GET requests for /api/data/sample
@app.route('/api/data/sample')
def sample_data():
    # replaces first 20 rows of dataframe with None instead of NaN for JSON serialization
    sample = df.head(20).replace({np.nan: None})
    return cors({
        'columns': list(df.columns),
        'rows': sample.values.tolist(),
        'total_rows': len(df),
    })

@app.route('/api/data/survived-by-class-sex')
def survived_by_class_sex():
    result = df.groupby(['Pclass', 'Sex'])['Survived'].agg(['sum','count','mean']).reset_index()
    result['rate'] = (result['mean'] * 100).round(1)
    result.columns = ['class','sex','survived','total','mean','rate']
    return cors(result.to_dict(orient='records'))

@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    resp = send_from_directory(os.path.join(BASE_DIR, 'static', 'charts'), filename)
    for k, v in CORS_HEADERS.items():
        resp.headers[k] = v
    return resp

@app.route('/health')
def health():
    return cors({'status': 'ok', 'rows': len(df)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)