import pandas as pd
from flask import Flask, render_template, request, jsonify

from df_client import DialogFlowProccess
from process import Process

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('form.html')


@app.route('/execute', methods=['POST'])
def execute():
    text = request.form['text']
    df = DialogFlowProccess().recognize_text(text=text)
    pr = Process(df["intent"], df["parameters"])
    data = pd.read_csv("MOCK_DATA.csv")
    if text:
        return jsonify(
            {
                'result': pr.get_df_field(),
                'result2': pr.get_sql_field(),
                'result3': pr.get_result_field(data)
            }
        )


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
