from flask import Flask, request, jsonify

app = Flask(__name__)

students = []

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
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    students.append({'name': data['name'], 'roll': data['roll'], 'marks': data['marks']})
    return jsonify({'msg': 'Student added!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)