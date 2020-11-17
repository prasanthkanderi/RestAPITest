from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class DBTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.String(30), default='default yes')
    date_created = db.Column(db.String(200), default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def launch_page():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = DBTest(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue Occurred'
    else:
        tasks = DBTest.query.order_by(DBTest.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = DBTest.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue Occurred'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = DBTest.query.get_or_404(id)

    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            pass
            return 'Issue Occurred'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
