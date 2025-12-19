from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Expense, Category

"""
Flask : A micro web framework written in Python.
render_template : Renders a template from the template folder with the given context.
redirect : Returns a response object and redirects the user to the target location.
url_for : Generates a URL to the given endpoint with the method provided.
request : Used to handle incoming request data.
flash : Used to generate informative messages in the application.
Flask-Login : A Flask extension that provides user session management.
LoginManager : Manages user sessions in Flask applications.
login_user : Logs a user in.
logout_user : Logs a user out.
login_required : A decorator that restricts access to logged-in users.
current_user : Proxy for the current logged-in user.
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    return render_template('login.html')

DEFAULT_CATEGORIES = [
    {'name': 'Food', 'description': 'Expenses on food and dining'},
    {'name': 'Transport', 'description': 'Expenses on transportation'},
    {'name': 'Utilities', 'description': 'Expenses on utilities like electricity, water, internet'},
    {'name': 'Entertainment', 'description': 'Expenses on movies, games, and other entertainment'},
    {'name': 'Healthcare', 'description': 'Medical and healthcare-related expenses'},
]

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if db.session.query(User).filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        else:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in!', 'success')

            for category in DEFAULT_CATEGORIES:
                new_category = Category(
                    name=category['name'],
                    description=category['description'],
                    user_id=new_user.id
                )
                db.session.add(new_category)
            db.session.commit()


            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    expenses = db.session.query(Expense).filter_by(user_id=current_user.id).all()
    category_totals = {}
    for exp in expenses:
        category = db.session.get(Category, exp.category_id)
        if category.name in category_totals:
            category_totals[category.name] += exp.amount
        else:
            category_totals[category.name] = exp.amount
       
    suggestions = []
    if category_totals:
        max_category = max(category_totals, key=category_totals.get)
        max_amount = category_totals[max_category]
        if max_amount > 50000:
            suggestions.append(f"You spend Rp{max_amount} on {max_category}. Consider reducing it.")
        else:
            suggestions.append(f"Your spending is within healthy limits.")

    return render_template(
        'dashboard.html', 
        name=current_user.username, 
        expenses=expenses,
        categories = list(category_totals.keys()),
        totals = list(category_totals.values()),
        suggestions=suggestions
    )

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    categories = db.session.query(Category).filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category_id = int(request.form['category'])
        
        new_expense = Expense(
            title=title,
            amount=amount,
            date=date,
            user_id=current_user.id,
            category_id=category_id
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html', categories=categories)

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = db.session.get(Expense, expense_id)
    categories = db.session.query(Category).filter_by(user_id=current_user.id).all()

    if expense.user_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        expense.category_id = int(request.form['category'])

        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_expense.html', expense=expense, categories=categories)

@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense.user_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('dashboard'))

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/categories')
@login_required
def list_categories():
    categories = db.session.query(Category).filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if db.session.query(Category).filter_by(name=name, user_id=current_user.id).first():
            flash('Category already exists!', 'error')
            return redirect(url_for('add_category'))
        else:
            new_category = Category(name=name, description=description, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully!', 'success')
            return redirect(url_for('list_categories'))
    
    return render_template('add_category.html')

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = db.session.get(Category, category_id)

    if request.method == 'POST':
        new_name = request.form['name']

        existing_category = db.session.query(Category).filter(
            Category.name == new_name,
            Category.id != category_id,
            Category.user_id == current_user.id
        ).first()

        if existing_category:
            flash('Category name already exists!', 'error')
            return redirect(url_for('edit_category', category_id=category_id))

        category.name = new_name
        category.description = request.form['description']
        db.session.commit()

        flash('Category updated successfully!', 'success')
        return redirect(url_for('list_categories'))

    return render_template('add_category.html', category=category)


@app.route('/categories/delete/<int:category_id>')
@login_required
def delete_category(category_id):
    category = db.session.get(Category, category_id)

    if db.session.query(Expense).filter_by(category_id=category_id).first():
        flash('Cannot delete category with associated expenses!', 'error')
        return redirect(url_for('list_categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('list_categories'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






