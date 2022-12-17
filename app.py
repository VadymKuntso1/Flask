from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    disc = db.Column(db.String(200), nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    endTime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<POST %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About Project'


@app.route('/name/<string:name>')
def user(name):
    return 'Name: '+name


@app.route('/remove/<int:id>')
def remove(id):
    post1 = ToDoList.query.get(id)
    db.session.delete(post1)
    db.session.commit()
    return redirect(url_for('list'))

@app.route('/post/<int:id>')
def post(id):
    post1 = ToDoList.query.get(id)
    return render_template('post.html',post=post1)


@app.route('/create', methods=['get','post'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        disc = request.form['disc']
        additionalTime = int( request.form['endTime'])
        endTime = datetime.utcnow() + timedelta(days=additionalTime)
        todolist = ToDoList(title = title,disc = disc,endTime=endTime)
        try:
            db.session.add(todolist)
            db.session.commit()
            return redirect('/')
        except Exception as a:
            return 'Error'+str(a)
    else:
        return render_template('create.html')


@app.route('/list')
def list():
    list = ToDoList.query.order_by(ToDoList.createTime).all()

    return render_template('list.html',list = list)

@app.route('/itstep')
def itstep():
    pass

if __name__ == '__main__':
    app.run(debug=True)


