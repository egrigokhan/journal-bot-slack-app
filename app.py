import os
import openai

from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

verification_token = os.environ['VERIFICATION_TOKEN']

def load_system():
    return ""
    
def save_system():
    return ""

def get_args(s):
    return s[s.find("<")+1:s.find(">")]

@app.route('/slash', methods=['POST'])
def slash():
    if request.form['token'] == verification_token:
        payload = {'text': str(get_args(request.form["text"]))}
        return jsonify(payload)

if __name__ == '__main__':
    app.run()
    
    
    # s = json.dumps(foo.__dict__)

    
    
    
    
    
    
    
class System:
    def __init__(self, papers):
        self.papers = papers
        
    def add_paper(self, paper):
        self.papers.append(paper)
        return "Paper succesfully added!"
        
    def get_current_message(self):
        message = '{ "blocks": ['
        
        paper_template = '''{
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*<PAPER_INDEX> <PAPER_SHORT_MESSAGE>"
                                    }
                                },'''
        
        for (i, p) in enumerate(self.papers):
            message += paper_template.replace("<PAPER_INDEX>", str(i)).replace("<PAPER_SHORT_MESSAGE>", p.get_short_message())
            
        
        message += '''{
                        "type": "divider"
                    },'''
                    
        message += '''{
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "View all tasks with `/task list`\\n Get help at any time with `/task help` or type *help* in a DM with me"
                            }
                        ]
                    }
                ]
            }'''
                    
        return message
    
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
        return "*" + self.title + "* | " + str(len(self.voters)) + " vote(s) \\nURL: " + self.URL + "\\n" + self.description
    
    def get_long_message(self):
        message = self.get_short_message()
        
        for pro in self.pros:
            message += "\n" + pro
            
        message += "\n"
        
        for con in self.cons:
            message += "\n" + cons

        return message
