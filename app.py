import os
import re
import os.path

from flask import Flask
from flask import request, jsonify
import json
import pickle

app = Flask(__name__)

verification_token = os.environ['VERIFICATION_TOKEN']

def load_system():
    if(os.path.isfile('system.pickle')):
        with open('system.pickle', 'rb') as f:
            print("Found system, opening...")
            return pickle.load(f)

    else:
        print("No system found, creating...")
        return System()
    
def save_system(system):
    with open('system.pickle', 'wb') as f:
            print("Saving system...")
            pickle.dump(system, f)

def get_args(s):
    return re.findall(r'\<.*?\>', s) 

@app.route('/slash', methods=['POST'])
def slash():
    if request.form['token'] == verification_token:
        payload = {'text': str(get_args(request.form["text"]))}
        system = load_system()
        system.add_paper(Paper("Paper 1", "paper_1.com", "Best paper ever"))
        system.add_paper(Paper("Paper 2", "paper_2.com", "Second best paper ever"))
        save_system(system)
        return '{ "blocks": [ { "type": "section", "text": { "type": "mrkdwn", "text": "*0 Paper 1 | 0 vote(s) \nURL: paper_1.com\nBest paper ever" } }, { "type": "section", "text": { "type": "mrkdwn", "text": "*1 Paper 2 | 0 vote(s) \nURL: paper_2.com\nSecond best paper ever" } }, { "type": "section", "text": { "type": "mrkdwn", "text": "*2 Paper 1 | 0 vote(s) \nURL: paper_1.com\nBest paper ever" } }, { "type": "section", "text": { "type": "mrkdwn", "text": "*3 Paper 2 | 0 vote(s) \nURL: paper_2.com\nSecond best paper ever" } }, { "type": "divider" }, { "type": "context", "elements": [ { "type": "mrkdwn", "text": "View all tasks with /task list\n Get help at any time with /task help or type help in a DM with me" } ] } ] }' # system.get_current_message() # jsonify(payload)

if __name__ == '__main__':
    app.run()
    
    
    # s = json.dumps(foo.__dict__)

    
    
    
    
    
    
    
class System:
    def __init__(self, papers = []):
        self.papers = papers
        
    def to_dict(self):
        dict = self.__dict__
        
        p_dict = []
        for p in self.papers:
            p_dict.append(p.toJSON())
            
        dict["papers"] = p_dict
        
        return dict
        
    def from_dict(self, j):
        self.__dict__ = json.loads(j)
        
        papers_ = []
        
        for p in papers:
            papers_.append(json.loads(p))
            
        self.papers = papers_
        
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
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
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
