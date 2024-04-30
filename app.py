# save this as app.py
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    s_no = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.s_no} - {self.title}"

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['textarea']
        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()  # Commit the changes once
        else:
            return redirect("/")
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route("/update")
def update(sno):
    return "redirect"
    

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = db.get_or_404(Todo, sno)
    # todo = Todo.query.filter_by(s_no=sno).first()
    if request.method == "GET":
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

if __name__ == '__main__':
   app.run(debug=True ,port=8000)