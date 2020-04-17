from flask import Flask, escape, request, render_template, url_for
import os
import json
import sqlite as DB

app = Flask(__name__)

# setup sqliteDB
DB.setup_sqliteDB()

# local cache variables
TEST_MAP = {}
SCANTRON_MAP = {}

@app.route('/')
def hello():
    return f'Hello, World!'

@app.route('/api/tests', methods=['POST'])
def createTest():
    if request.method == 'POST':

        # get subject, answer_keys
        subject = request.json['subject']
        answer_keys = request.json['answer_keys']

        testID = DB.create_test(subject, answer_keys)
        TEST_MAP[testID] = {
            "test_id": testID,
            "subject": subject,
            "answer_keys": answer_keys,
            "submissions": [] 
        }
        
        return json.dumps(TEST_MAP[testID]), 201

@app.route('/api/tests/<int:testID>/scantrons', methods=['POST'])
def createSubmission(testID):
    if request.method == 'POST':
        if testID in TEST_MAP:

            # get date ID from payload
            name = request.json['name']
            subject = request.json['subject']
            actual_answer_keys = request.json['answer_keys']

            # get data from DB and cache
            scantronID = DB.create_scantron(name, subject, actual_answer_keys)
            expected_answer_keys = TEST_MAP[testID]['answer_keys']
            result, score = DB.getResultAndScore(actual_answer_keys, expected_answer_keys)

            response = {
                "scantron_id": scantronID,
                "scantron_url": "http://localhost:5000/files/{}.json".format(scantronID),
                "name": name,
                "subject": subject,
                "score": score,
                "result": result
            }

            # Save uploaded file into server
            json_file_name = "{}.json".format(scantronID)
            with open('files/' + json_file_name, "w") as outfile: 
                outfile.write(json.dumps(request.json))

            # Add new submission into TEST_MAP
            DB.addSubmission(testID, scantronID)
            TEST_MAP[testID]['submissions'].append(response)

            return json.dumps(response), 201
        
        return "Test not found"

@app.route('/api/tests/<int:testID>', methods=['GET'])
def getClass(testID):
    if request.method == 'GET':
        
        # if the test exists in the cache, then read from cache
        if (testID in TEST_MAP):
            return json.dumps(TEST_MAP[testID])
        else :
            response = DB.getScantronSubmissions(testID)
            return json.dumps(response)

@app.route('/files/<int:fileID>.json', methods=['GET'])
def getFile(fileID):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "files", "{}.json".format(fileID))
    data = json.load(open(json_url))
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)