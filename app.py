from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:flask@db:3306/flask'
db.init_app(app)

class Departaments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departaments_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Departaments %r>' % self.id

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=False)
    hire_date = db.Column(db.Integer, default=False)
    job_id = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    comission_pct = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)
    departament_id = db.Column(db.Integer, nullable=False)
    #висвітлення рядка
    def __repr__(self):
        return '<Employees %r>' % self.id




@app.route('/', methods=["GET"] )
def index():
    return render_template('index.html')


@app.route('/create-departament', methods=['POST','GET'])
def create_department():
    #отримує дані з реквесту
    if request.method == 'POST':

        departaments_name=request.form['departaments_name']
        manager_id=request.form['manager_id']
        location_id=request.form['location_id']
        department =(
            Departaments(
                departaments_name=departaments_name,
                manager_id=manager_id,
                location_id=location_id
            ))

        try:
            #добавити в базу даних
            db.session.add(department)
            #зберегти
            db.session.commit()
            return redirect('/departments')
        except:
            return "Error"
    else:
        return render_template('create-departament.html')



@app.route('/create-employee', methods=['POST','GET'])
def create_employee():
    #отримує дані з реквесту
    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        job_id = request.form['job_id']
        salary = request.form['salary']
        comission_pct = request.form['comission_pct']
        manager_id = request.form['manager_id']
        departament_id = request.form['departament_id']

        employee = Employees(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             phone_number=phone_number,
                             job_id=job_id,
                             salary=salary,
                             comission_pct=comission_pct,
                             manager_id=manager_id,
                             departament_id=departament_id)

        try:
            #добавити в базу даних
            db.session.add(employee)
            #зберегти
            db.session.commit()
            return redirect('/employees')
        except:
            return "Error Employee Add"
    else:
        return render_template('create-employee.html')


@app.route('/departments', methods=["GET"] )
def departments():
    departments = Departaments.query.all()
    return render_template('departments.html', departments=departments)


@app.route('/employees', methods=["GET"] )
def employees():
    employees = Employees.query.order_by(Employees.id.desc()).all()
    return render_template('employees.html', employees=employees)

@app.route('/employee/<int:id>', methods=["GET"] )
def employee_detail(id):
    employee = Employees.query.get(id)
    return render_template('employee_detail.html', employee=employee)

@app.route('/employee/<int:id>/delete', methods=["GET"] )
def employee_delete(id):
    employee = Employees.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/employees')
    except:
        return "Error for delete Employee"

@app.route('/employee/<int:id>/update', methods=['POST','GET'])
def employee_update(id):

    employee = Employees.query.get(id)
    #отримує дані з реквесту
    if request.method == 'POST':
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.email = request.form['email']
        employee.phone_number = request.form['phone_number']
        employee.job_id = request.form['job_id']
        employee.salary = request.form['salary']
        employee.comission_pct = request.form['comission_pct']
        employee.manager_id = request.form['manager_id']
        employee.departament_id = request.form['departament_id']

        try:
            #зберегти
            db.session.commit()
            return redirect('/employees')
        except:
            return "Error update employees "
    else:
        employee = Employees.query.get(id)
        return render_template('employee_update.html', employee=employee)



@app.route('/departments/<int:id>', methods=["GET"] )
def department_detail(id):
    department = Departaments.query.get(id)
    return render_template('post-detail.html', departments=departments)

@app.route('/departments/<int:id>/delete', methods=["GET"] )
def department_delete(id):
    department = Departaments.query.get_or_404(id)
    try:
        db.session.delete(department)
        db.session.commit()
        return redirect('/departments')
    except:
        return "Error for delete departments"

@app.route('/departments/<int:id>/update', methods=['POST','GET'])
def department_update(id):
    department = Departaments.query.get(id)
    #отримує дані з реквесту
    if request.method == 'POST':
        department.departaments_name=request.form['departaments_name']
        department.manager_id=request.form['manager_id']
        department.location_id=request.form['location_id']

        try:
            #зберегти
            db.session.commit()
            return redirect('/departments')
        except:
            return "Error update department"
    else:
        department = Departaments.query.get(id)
        return render_template('department_update.html', department=department)

with app.app_context():
    db.create_all()


app.run(host='0.0.0.0', port=8080, debug=True)



