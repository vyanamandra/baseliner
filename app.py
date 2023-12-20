from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

def execute_command():
    command = "ansible-playbook -i inventory/hosts main.yml"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in iter(process.stdout.readline, b''):
        yield line.decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(execute_command(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
