import os
import openai

from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

verification_token = os.environ['VERIFICATION_TOKEN']

@app.route('/slash', methods=['POST'])
def slash():
    if request.form['token'] == verification_token:
        print(request)
        payload = {'text': 'DigitalOcean Slack slash command is successful!'}
        return jsonify(payload)


if __name__ == '__main__':
    app.run()
