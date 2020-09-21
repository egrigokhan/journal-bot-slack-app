import os
import openai

from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/slash', methods=['POST'])
def slash():
    if request.form['token'] == verification_token:
        payload = {'text': 'DigitalOcean Slack slash command is successful!'}
        return jsonify(payload)


if __name__ == '__main__':
    app.run()
