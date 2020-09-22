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
    args_ = re.findall(r'\<.*?\>', str(s)) 
    args_clean = []
    
    for arg in args_:
        args_clean.append(arg[1:-1])
        
    return args_clean

@app.route('/status', methods=['POST'])
def status():
    if request.form['token'] == verification_token:
        payload = {'text': str(get_args(request.form["text"]))}
        system = load_system()
        
        return jsonify(json.loads(system.get_current_message(), strict=False)) # system.get_current_message() # jsonify(payload)
    
@app.route('/detail', methods=['POST'])
def detail():
    if request.form['token'] == verification_token:
        args = get_args(request.form["text"])
        system = load_system()        
        return jsonify(json.loads(system.get_detail_for_paper(int(args[0])), strict=False)) # system.get_current_message() # jsonify(payload)
    
@app.route('/add', methods=['POST'])
def add():
    if request.form['token'] == verification_token:
        args = get_args(request.form["text"])
        system = load_system()        
        system.add_paper(Paper(args[0], args[1], args[2]))
        save_system(system)
        return "Added paper!" # jsonify(json.loads(system.get_detail_for_paper(int(args[0])), strict=False)) # system.get_current_message() # jsonify(payload)

@app.route('/add_pro', methods=['POST'])
def add_pro():
    if request.form['token'] == verification_token:
        args = get_args(request.form["text"])
        system = load_system()        
        system.add_pro_for_paper(int(args[0]), args[1])
        save_system(system)
        return "Added pro!" # jsonify(json.loads(system.get_detail_for_paper(int(args[0])), strict=False)) # system.get_current_message() # jsonify(payload)

    
@app.route('/add_con', methods=['POST'])
def add_con():
    if request.form['token'] == verification_token:
        args = get_args(request.form["text"])
        system = load_system()        
        system.add_con_for_paper(int(args[0]), args[1])
        save_system(system)
        return "Added con!" # jsonify(json.loads(system.get_detail_for_paper(int(args[0])), strict=False)) # system.get_current_message() # jsonify(payload)

@app.route('/vote', methods=['POST'])
def vote():
    if request.form['token'] == verification_token:
        # print(request.form)
        args = get_args(request.form["text"])
        system = load_system()
        system.add_or_remove_vote_from_paper(int(args[0]), request.form["user_name"])
        save_system(system)
        return "Added/removed vote!"

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
                                        "text": "*<PAPER_INDEX>* <PAPER_SHORT_MESSAGE>"
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
        if(index < len(self.papers)):
            message = '{ "blocks": ['
        
            paper_template = '''{
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": "<PAPER_LONG_MESSAGE>"
                                        }
                                    },'''

            message += paper_template.replace("<PAPER_LONG_MESSAGE>", self.papers[index].get_long_message())


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
        
    def add_pro_for_paper(self, index, pro):
        if(index < len(self.papers)):
            return self.papers[index].add_pro(pro)
        
    def add_con_for_paper(self, index, con):
        if(index < len(self.papers)):
            return self.papers[index].add_con(con)
        
    def add_or_remove_vote_from_paper(self, index, voter):
        if(index < len(self.papers)):
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
        if(voter in self.voters):
            self.voters.remove(voter)
        else:
            self.voters.append(voter)

    def add_pro(self, pro):
        self.pros.append(pro)
        
    def add_con(self, con):
        self.cons.append(con)
        
    def get_short_message(self):
        return "*" + self.title + "* | " + str(len(self.voters)) + " vote(s) \\nURL: " + self.URL + "\\n" + self.description
    
    def get_long_message(self):
        message = self.get_short_message() + "\\n\\n"
        message += "Voter(s):\\n"
        
        for voter in self.voters:
            message += voter + "\\n"
            
        message += "\\nPros:\\n"
        
        for pro in self.pros:
            message += "\\n" + pro
            
        message += "\\n\\nCons:\\n"
        
        for con in self.cons:
            message += "\\n" + cons

        return message
