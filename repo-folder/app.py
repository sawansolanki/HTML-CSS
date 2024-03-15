from flask import Flask, request , render_template

app = Flask(__name__)

@app.route('/')
def func():
    return "Hello, world!"

@app.route('/name')
def fname():
    name = request.args.get('name')
    return "Hello, " + name

@app.route('/addnumber')
def addnum():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    ab = a + b
    #return "The sum of {} and {} is {}".format(a, b, ab)
    return render_template('app-test.html', ab=ab)
    #return "{}".format(ab)

if __name__ == "__main__":
    app.run(debug=True)