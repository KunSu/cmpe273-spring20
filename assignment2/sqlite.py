#!/usr/bin/python
import sqlite3
import json

def setup_sqliteDB():
    conn = sqlite3.connect('test.db')

    # Setup up local SQLite DB
    conn.execute('DROP TABLE IF EXISTS test;')
    conn.execute('DROP TABLE IF EXISTS scantron;')
    conn.execute('DROP TABLE IF EXISTS test_submissions;')

    # Create test Table
    conn.execute(
        '''
        CREATE TABLE test
        (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            subject              TEXT    NOT NULL,
            answer_keys          JSON    NOT NULL
        );
        '''
    )

    # Create scantron Table
    conn.execute(
        '''
        CREATE TABLE scantron
        (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name                 TEST    NOT NULL,
            subject              TEXT    NOT NULL,
            answer_keys          JSON    NOT NULL
        );
        '''
    )

    # Create test submissions Table
    conn.execute(
        '''
        CREATE TABLE test_submissions
        (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id             INT      NOT NULL,
            scantron_id         INT      NOT NULL,
            FOREIGN KEY(test_id) REFERENCES test(id),
            FOREIGN KEY(scantron_id) REFERENCES scantron(id)
        );
        '''
    )
    
    conn.commit()
    conn.close()
    print("Database setup successfully")

def create_test(subject, answer_keys):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute('''INSERT INTO test (subject, answer_keys) VALUES(?, ?)''', (subject, json.dumps(answer_keys),))
    id = c.lastrowid

    conn.commit()
    conn.close()
    return id

def create_scantron(name, subject, actual_answer_keys):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute('''INSERT INTO scantron (name, subject, answer_keys) VALUES(?, ?, ?)''', (name, subject, json.dumps(actual_answer_keys),))
    id = c.lastrowid

    conn.commit()
    conn.close()
    return id

def addSubmission(test_id, scantron_id):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute('''INSERT INTO test_submissions (test_id, scantron_id) VALUES(?, ?)''', (test_id, scantron_id,))

    conn.commit()
    conn.close()

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

def getScantronSubmissions(test_id):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    result = c.execute('''SELECT subject, answer_keys FROM test WHERE id = ?''', (test_id,))

    actual_answer_keys = {}
    expected_answer_keys = {}

    for row in result:
        test_subject = row[0]
        expected_answer_keys = json.loads(row[1])

    result = c.execute('''
        SELECT id, name, subject, answer_keys
        FROM (SELECT scantron_id FROM test_submissions WHERE test_id = ?) as result
        LEFT JOIN scantron 
        ON result.scantron_id = scantron.id
    ''', (test_id,))

    submissions = []
    for row in result:
        scantronID = row[0]
        name = row[1]
        subject = row[2]
        actual_answer_keys = json.loads(row[3])
        result, score = getResultAndScore(actual_answer_keys, expected_answer_keys)

        submission = {
            "scantron_id": scantronID,
            "scantron_url": "http://localhost:5000/files/{}.pdf".format(scantronID),
            "name": name,
            "subject": subject,
            "score": score,
            "result": result
        }
        submissions.append(submission)

    conn.commit()
    conn.close()

    response = {
        "test_id": test_id,
        "subject": test_subject,
        "answer_keys": expected_answer_keys,
        "submissions": submissions
    }
    return response