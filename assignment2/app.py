from flask import Flask, escape, request
import json

app = Flask(__name__)

# Global variables
TEST_ID = 0
TEST_MAP = {}
SCANTRON_ID = 0
SCANTRON_MAP = {}

@app.route('/')
def hello():
    return f'Hello, World!'

@app.route('/api/tests', methods=['POST'])
def createStudent():
    global TEST_ID
    if request.method == 'POST':

        # get subject, answer_keys
        subject = request.json['subject']
        answer_keys = request.json['answer_keys']
        testID = TEST_ID

        TEST_MAP[testID] = {
            "test_id": testID,
            "subject": subject,
            "answer_keys": answer_keys,
            "submissions": [] 
        }
        TEST_ID += 1

        return json.dumps(TEST_MAP[testID]), 201

# POST http://localhost:5000/api/tests/1/scantrons
@app.route('/api/tests/<int:testID>/scantrons', methods=['POST'])
def addStudentIntoClass(testID):
    if request.method == 'POST':
        global SCANTRON_ID
        if testID in TEST_MAP:

            # get Student ID from payload
            subject = request.json['subject']
            actual_answer_keys = request.json['answer_keys']
            scantronID = SCANTRON_ID
            expected_answer_keys = TEST_MAP[testID]['answer_keys']
            result, score = getResultAndScore(actual_answer_keys, expected_answer_keys)

            response = {
                "scantron_id": scantronID,
                "scantron_url": "http://localhost:5000/files/{}.pdf".format(scantronID),
                "name": "Foo Bar",
                "subject": "Math",
                "score": score,
                "result": result
            }

            # Add new submission into TEST_MAP
            TEST_MAP[testID]['submissions'].append(response)

            SCANTRON_ID += 1
            return json.dumps(response), 201
        
        return "Test not found"

def getResultAndScore(actual, expected):

    score = 0
    points = 100 / len(expected)
    result = {}
    for key in actual:
        result[key] = {
            "actual": actual[key],
            "expected": expected[key]
        }
        if actual[key] != expected[key]:
            score += points
    return result, int(score)

@app.route('/api/tests/<int:testID>', methods=['GET'])
def getClass(testID):
    if request.method == 'GET':
        if (testID in TEST_MAP):
            return json.dumps(TEST_MAP[testID])
            
        return "TEST not found"

if __name__ == '__main__':
    app.run(debug=True)