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

    
    
    
    
    
    
    
class System:
    def __init__(self, papers):
        self.papers = papers
        
    def add_paper(self, paper):
        self.papers.append(paper)
        return "Paper succesfully added!"
        
    def get_current_message(self):
        for p in self.papers:
            print(p.title)
    
    def get_detail_for_paper(self, index):
        if(index < self.papers.count):
            return self.papers[index].get_long_message()
        
    def add_pro_for_paper(self, index, pro):
        if(index < self.papers.count):
            return self.papers[index].add_pro(pro)
        
    def add_con_for_paper(self, index, con):
        if(index < self.papers.count):
            return self.papers[index].add_con(con)
        
    def add_or_remove_vote_from_paper(self, index, voter):
        if(index < self.papers.count):
            return self.papers[index].add_or_remove_vote(voter)
    
class Paper:
    def __init__(self, title, URL, description, pros = [], cons = [], voters = []):
        self.title = title
        self.URL = URL
        self.description = description
        self.pros = pros
        self.cons = cons
        self.voters = voters
        
    def add_or_remove_vote(self, voter):
        if(voters.contains(voter)):
            voters.remove(voter)
        else:
            voters.append(voter)

    def add_pro(self, pro):
        self.pros.append(pro)
        
    def add_con(self, con):
        self.cons.append(con)
        
    def get_short_message(self):
        return "*" + self.title + "* | " + str(len(self.voters)) + " vote(s) \nURL: " + self.URL + "\n" + self.description
    
    def get_long_message(self):
        message = self.get_short_message()
        
        for pro in self.pros:
            message += "\n➕" + pro
            
        message += "\n"
        
        for con in self.cons:
            message += "\n➖" + cons

        return message
