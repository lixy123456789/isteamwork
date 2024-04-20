from flask import Flask, request, jsonify
import nbformat
from nbconvert import PythonExporter
app = Flask(__name__)

@app.route('/')

@app.route('/get_population', methods=['POST'])
def get_population_route():
    data = request.get_json()
    items = data['items']

    # Import the Python script and call the function
    from project_irs import get_population
    population = get_population(items)
    return jsonify(population)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
