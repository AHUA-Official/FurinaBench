from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

def execute_ssh_command(hostname, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        print(error)
        print()
        return {
            'status': 'success',
            'output': output,
            'error': error if error else None
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        ssh.close()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ssh_command', methods=['POST'])
def ssh_command():
    data = request.json
    hostname = data.get('hostname')
    port = data.get('port', 22)
    username = data.get('username')
    password = data.get('password')
    command = data.get('command')


    result = execute_ssh_command(hostname, port, username, password, command)
    return jsonify(result)

if __name__ == '__main__':
    app.run()