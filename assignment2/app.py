from flask import Flask, escape, request
import json
import sqlite as DB

app = Flask(__name__)

# setup sqliteDB
DB.setup_sqliteDB()

# Global variables
# TEST_ID = 0
TEST_MAP = {}
SCANTRON_ID = 0
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
                "scantron_url": "http://localhost:5000/files/{}.pdf".format(scantronID),
                "name": name,
                "subject": subject,
                "score": score,
                "result": result
            }

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

if __name__ == '__main__':
    app.run(debug=True)