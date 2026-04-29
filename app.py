
from flask import Flask, request, jsonify
import pymysql
import boto3
import json
from datetime import datetime

app = Flask(__name__)

DB_HOST = 'students.cvwcyoa8uwdr.ap-south-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASS = 'Student@123'
DB_NAME = 'students'
S3_BUCKET = 'student-app-backup-aws'

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route('/')
def home():
    return '''
    <html>
    <body style="font-family:Arial; margin:40px;">
      <h2>Student App</h2>
      Name: <input id="name"><br><br>
      Roll No: <input id="roll"><br><br>
      Marks: <input id="marks" type="number"><br><br>
      <button onclick="add()">Add Student</button>
      <button onclick="load()">View Students</button>
      <div id="list"></div>
      <script>
        function add() {
          fetch('/students', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
              name: document.getElementById('name').value,
              roll: document.getElementById('roll').value,
              marks: document.getElementById('marks').value
            })
          }).then(r=>r.json()).then(d=>{ alert(d.msg); load(); });
        }
        function load() {
          fetch('/students').then(r=>r.json()).then(data=>{
            let h = '<br><table border="1" cellpadding="8"><tr><th>Roll</th><th>Name</th><th>Marks</th></tr>';
            data.forEach(s=> h += '<tr><td>'+s.roll+'</td><td>'+s.name+'</td><td>'+s.marks+'</td></tr>');
            document.getElementById('list').innerHTML = h + '</table>';
          });
        }
      </script>
    </body>
    </html>
    '''

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll, marks FROM students")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{'name': r[0], 'roll': r[1], 'marks': r[2]} for r in rows])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json

    # Save to RDS MariaDB
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, roll, marks) VALUES (%s, %s, %s)",
        (data['name'], data['roll'], data['marks'])
    )
    conn.commit()
    conn.close()

    # Save backup to S3
    s3 = boto3.client('s3', region_name='ap-south-1')
    backup = {
        'name': data['name'],
        'roll': data['roll'],
        'marks': data['marks'],
        'time': str(datetime.now())
    }
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"backups/{data['roll']}.json",
        Body=json.dumps(backup)
    )

    return jsonify({'msg': 'Student added to MariaDB and backed up to S3!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
