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

    
    
    
    
    
    
    
    
    
class Paper:
    def __init__(self, title, URL, description, pros = [], cons = [], voters = []):
        self.title = title
        self.URL = URL
        self.description = description
        self.pros = pros
        self.cons = cons
        self.voters = voters

    def add_pro(self, pro):
        self.pros.append(pro)
        
    def add_con(self, con):
        self.cons.append(con)
        
    def get_short_message(self):
        return ""
    
    def get_long_message(self):
