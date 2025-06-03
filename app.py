from flask import Flask, render_template, redirect, url_for, request
import json
import os

app = Flask(__name__)

DATA_FILE = 'tools.json'

# Load tools from JSON file or create default list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        tools = json.load(f)
else:
    tools = [
        {'id': 1, 'name': 'Llave inglesa', 'borrowed': False, 'borrower': ''},
        {'id': 2, 'name': 'Destornillador', 'borrowed': False, 'borrower': ''},
        {'id': 3, 'name': 'Martillo', 'borrowed': False, 'borrower': ''}
    ]


def save_tools():
    with open(DATA_FILE, 'w') as f:
        json.dump(tools, f, indent=2)


@app.route('/')
def index():
    return render_template('index.html', tools=tools)


@app.route('/borrow/<int:tool_id>', methods=['POST'])
def borrow(tool_id):
    borrower = request.form.get('borrower', '')
    for tool in tools:
        if tool['id'] == tool_id and not tool['borrowed']:
            tool['borrowed'] = True
            tool['borrower'] = borrower
            save_tools()
            break
    return redirect(url_for('index'))


@app.route('/return/<int:tool_id>', methods=['POST'])
def return_tool(tool_id):
    for tool in tools:
        if tool['id'] == tool_id and tool['borrowed']:
            tool['borrowed'] = False
            tool['borrower'] = ''
            save_tools()
            break
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
