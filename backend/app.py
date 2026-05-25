from flask import Flask, jsonify, send_from_directory
import pandas as pd
import numpy as np
import json, os

app = Flask(__name__, static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = None

def get_df():
    global df
    if df is None:
        df = pd.read_csv(os.path.join(BASE_DIR, 'titanic.csv'))
    return df

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stats')
def stats():
    with open(os.path.join(BASE_DIR, 'stats.json')) as f:
        data = json.load(f)

    data['class_breakdown'] = {
        int(k): v for k, v in data.get('class_breakdown', {}).items()
    }

    data['class_survival_rates'] = {
        int(k): v for k, v in data.get('class_survival_rates', {}).items()
    }

    return jsonify(data)


@app.route('/api/charts')
def charts():
    chart_files = [
        {'id': 'survival_by_class', 'title': 'Survival by Passenger Class', 'file': 'survival_by_class.png'},
        {'id': 'age_distribution', 'title': 'Age Distribution by Survival', 'file': 'age_distribution.png'},
        {'id': 'survival_by_sex', 'title': 'Survival Rate by Gender', 'file': 'survival_by_sex.png'},
        {'id': 'fare_distribution', 'title': 'Fare Distribution (Log Scale)', 'file': 'fare_distribution.png'},
        {'id': 'survival_by_embark', 'title': 'Survival by Port of Embarkation', 'file': 'survival_by_embark.png'},
        {'id': 'correlation_heatmap', 'title': 'Feature Correlation Heatmap', 'file': 'correlation_heatmap.png'},
    ]

    for c in chart_files:
        c['url'] = f"/static/charts/{c['file']}"

    return jsonify(chart_files)


@app.route('/api/data/sample')
def sample_data():
    df_local = get_df()
    sample = df_local.head(20).replace({np.nan: None})

    return jsonify({
        'columns': list(df_local.columns),
        'rows': sample.values.tolist(),
        'total_rows': len(df_local),
    })


@app.route('/api/data/survived-by-class-sex')
def survived_by_class_sex():
    df_local = get_df()

    result = (
        df_local.groupby(['Pclass', 'Sex'])['Survived']
        .agg(survived='sum', total='count', rate='mean')
        .reset_index()
    )

    result['rate'] = (result['rate'] * 100).round(1)

    return jsonify(result.to_dict(orient='records'))


@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, 'static', 'charts'),
        filename
    )

@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 204

@app.route('/health')
def health():
    try:
        df_local = get_df()
        return jsonify({'status': 'ok', 'rows': len(df_local)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)