from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone,timedelta
IST = timezone(timedelta(hours=5, minutes=30))
chiro = Flask(__name__)
chiro.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
chiro.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(chiro)
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime, default=lambda: datetime.now(IST).replace(microsecond=0))
    def __repr__(self)->str:
        return f"{self.sno},{self.title}"
@chiro.route("/",methods=["GET","POST"])
def index():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()#add object
    query = request.args.get('query')
    if query:
        alltodo = Todo.query.filter(
            Todo.title.ilike(f'%{query}%') | Todo.description.ilike(f'%{query}%')
        ).all()
    else:
        alltodo = Todo.query.all()    
    print(alltodo)
    return render_template('index.html',alltodo=alltodo)
@chiro.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@chiro.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
@chiro.route("/instructions")
def instructions():
    return render_template("instructions.html")

if __name__=="__main__":
    chiro.run(debug=True,port=10000)
   
