from flask import Flask, jsonify, send_from_directory, CORS
import pandas as pd
import numpy as np
import json, os

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, 'titanic.csv'))

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors)

@app.route('/api/stats')
def stats():
    with open(os.path.join(BASE_DIR, 'stats.json')) as f:
        data = json.load(f)
    # Convert numpy/int keys
    data['class_breakdown'] = {int(k): v for k, v in data['class_breakdown'].items()}
    data['class_survival_rates'] = {int(k): v for k, v in data['class_survival_rates'].items()}
    return jsonify(data)

@app.route('/api/charts')
def charts():
    chart_files = [
        {'id': 'survival_by_class',   'title': 'Survival by Passenger Class',          'file': 'survival_by_class.png'},
        {'id': 'age_distribution',    'title': 'Age Distribution by Survival',          'file': 'age_distribution.png'},
        {'id': 'survival_by_sex',     'title': 'Survival Rate by Gender',               'file': 'survival_by_sex.png'},
        {'id': 'fare_distribution',   'title': 'Fare Distribution (Log Scale)',          'file': 'fare_distribution.png'},
        {'id': 'survival_by_embark',  'title': 'Survival by Port of Embarkation',       'file': 'survival_by_embark.png'},
        {'id': 'correlation_heatmap', 'title': 'Feature Correlation Heatmap',           'file': 'correlation_heatmap.png'},
    ]
    for c in chart_files:
        c['url'] = f"/static/charts/{c['file']}"
    return jsonify(chart_files)

@app.route('/api/data/sample')
def sample_data():
    sample = df.head(20).replace({np.nan: None})
    return jsonify({
        'columns': list(df.columns),
        'rows': sample.values.tolist(),
        'total_rows': len(df),
    })

@app.route('/api/data/survived-by-class-sex')
def survived_by_class_sex():
    result = df.groupby(['Pclass', 'Sex'])['Survived'].agg(['sum','count','mean']).reset_index()
    result['rate'] = (result['mean'] * 100).round(1)
    result.columns = ['class','sex','survived','total','mean','rate']
    return jsonify(result.to_dict(orient='records'))

@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'charts'), filename)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'rows': len(df)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
