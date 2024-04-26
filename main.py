from flask import Flask, render_template, url_for, redirect, abort, request, jsonify, make_response
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from forms.user import LoginForm, RegisterForm, UpdateForm, CheckEmailForm, ChangePasswordForm
from forms.product import ProductForm, UpdateProductForm
from forms.feedback import FeedbackForm
from data import db_session, feedbacks_api
from data.users import User
from data.product import Product
from data.feedbacks import Feedback
from data.cart import Cart
from flask_restful import Api
from werkzeug.utils import secure_filename
import datetime as dt
import data.users_resources as users_resources
import os

""" Задачи:
1. Реализовать мобильную адаптацию
"""

""" Команды alembic
alembic revision --autogenerate -m "Коментарии"
alembic upgrade head - upgrade выполняет код для изменения состояния базы
                       downgrade — код для возврата к предыдущему состоянию
"""


UPLOAD_FOLDER = "static/img/product_img"

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(
    days=15
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)


# Функция для проверки и сохранения изображения продукта
def save_image_product(image):
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return filename
    return None


'''Потом может сделаю'''
# Функция для проверки и сохранения изображения юзера
# def save_image_user(image):
#     if image:
#         filename = secure_filename(image.filename)
#         image_path = os.path.join("static/img/user_img/", filename)
#         image.save(image_path)
#         return filename
#     return None


# загрузка пользователей
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# главная страница
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    # рендер главной страницы
    return render_template(
        'index.html',
        title='Guitar House',
        css=url_for('static', filename='css/style.css'),
        js=url_for('static', filename='js/main.js'),
        sum_price=summary
    )


# страница с товарами
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    # форма добавления товара
    form = ProductForm()
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    # действия при добавлении товара
    products = db_sess.query(Product).all()
    if form.validate_on_submit():
        product = Product()

        product.title = form.name.data
        product.price = form.price.data
        product.content = form.description.data
        product.category_id = form.category.data

        image_file1 = save_image_product(form.image1.data)
        if image_file1:
            product.image1 = image_file1
        image_file2 = save_image_product(form.image2.data)
        if image_file2:
            product.image2 = image_file2

        current_user.product.append(product)

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/shop')
    # поиск
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        products = db_sess.query(Product).filter(Product.title.ilike(f'%{search_term}%')).all()
        return jsonify(
            {
                'products': [
                    {
                        'title': product.title,
                        'content': product.content,
                        'id': product.id,
                        'img': product.image1
                    }
                    for product in products
                ]
            }
        )
    # рендер страницы с товарами
    return render_template(
        'shop.html',
        title='Guitar House / Товар',
        css=url_for('static', filename='css/shop.css'),
        js=url_for('static', filename='js/main.js'),
        form=form,
        products=products,
        sum_price=summary
    )


# странциа с отзывами
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # форма добавления отзыва
    form = FeedbackForm()
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    #  действия при добавлении отзыва
    feedback = db_sess.query(Feedback).all()
    if form.validate_on_submit():
        feedback = Feedback(
            text=form.text.data
        )
        current_user.feedback.append(feedback)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/contact')
    # рендер страницы с отзывами
    return render_template(
        'contact.html',
        title='Guitar House / Контакты',
        css=url_for('static', filename='css/contact.css'),
        js=url_for('static', filename='js/main.js'),
        form=form,
        feedback=feedback,
        sum_price=summary
    )


# страница корзины
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    cart_items = db_sess.query(Cart).filter(Cart.user_id == current_user.id)
    # рендер страницы с корзиной
    return render_template(
        'cart.html',
        title='Guitar House / Корзина',
        css=url_for('static', filename='css/cart.css'),
        js=url_for('static', filename='js/main.js'),
        sum_price=summary,
        cart_items=cart_items
    )


# удаление товара из корзины
@app.route('/del-cart-item/<int:id>', methods=['GET', 'POST'])
@login_required
def del_item(id):
    # действия удаление товара из корзины
    db_sess = db_session.create_session()
    cart = db_sess.query(Cart).filter(Cart.id == id).first()
    if cart:
        db_sess.delete(cart)
        db_sess.commit()
        return redirect('/cart')
    else:
        abort(404)


# добавление товара в корзину
@app.route('/add-cart/<int:id>', methods=['GET', 'POST'])
@login_required
def add_cart(id):
    # действия добавления товара в корзину
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    if product:
        if product in current_user.cart:
            return redirect('/shop')
        else:
            cart = Cart(
                product_id=product.id,
                user=current_user,
                price=product.price
            )
            db_sess.merge(cart)
            db_sess.commit()
            return redirect('/shop')


# страница личного кабинета
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # форма для редактирования данных пользователя
    form = UpdateForm()
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    # действия при редактировании данных пользователя
    products = db_sess.query(Product).filter(Product.user_id == current_user.id).all()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.full_name = form.full_name.data
            user.age = form.age.data
            user.birthday = form.birthday.data
            user.email = form.email.data

            db_sess.merge(user)
            db_sess.commit()
            return redirect('/account')
        else:
            abort(404)
    # рендер страницы личного кабинета
    return render_template(
        'account.html',
        title='Guitar House / Личный кабинет',
        css=url_for('static', filename='css/account.css'),
        js=url_for('static', filename='js/main.js'),
        form=form,
        info=current_user,
        products=products,
        sum_price=summary
    )


# удаление аккаунта
@app.route('/del-account/<int:id>', methods=['GET', 'POST'])
def del_account(id):
    # действия удаления аккаунта
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
        return redirect('/')
    else:
        abort(404)


# страница информации о товаре
@app.route('/info_product/<int:id>', methods=['GET', 'POST'])
def info_product(id):
    db_sess = db_session.create_session()
    # получаем и суммируем товаров в корзине
    summary = 0
    try:
        sum_price = db_sess.query(Cart.price).filter(Cart.user_id == current_user.id)
        for i in sum_price:
            summary += i[0]
    except AttributeError:
        summary = 0
    """ Если товар не найден, то возвращаем ошибку 404, 
    иначе рендер страницы информации о товаре"""
    product = db_sess.query(Product).filter(Product.id == id).first()
    if product:
        return render_template(
            'info_product.html',
            title='Guitar House / Инфорация о товаре',
            css=url_for('static', filename='css/info_product.css'),
            js=url_for('static', filename='js/app.js'),
            product=product,
            sum_price=summary
        )
    else:
        abort(404)


# страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # форма авторизации
    form = LoginForm()
    # действия при авторизации
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        """ Если введенные логин и пароль совпадают,
        то переходим в личный кабинет, инваче возвразаем 
        страницу аторизации с ошибкой"""
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/account')
        return render_template(
            'login.html',
            title='Guitar House / Авторизация',
            css=url_for('static', filename='css/form.css'),
            js=url_for('static', filename='js/main.js'),
            form=form,
            message="Неправильно введен логин или пароль"
        )
    return render_template(
        'login.html',
        title='Guitar House / Авторизация',
        css=url_for('static', filename='css/form.css'),
        js=url_for('static', filename='js/main.js'),
        form=form
    )


# страницы восстановления пароля
@app.route('/check-email', methods=['GET', 'POST'])
def check_email():
    # форма для проверки создан ли аккаунт
    form = CheckEmailForm()
    """Если пользователь с такой почтой найден, 
    то переходим на страницу смены пароля, 
    иначе позвращаем эту же страницу с ошибкой"""
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return redirect(f'/change-password/{form.email.data}')
        else:
            return render_template(
                'check-email.html',
                title='Guitar House / Проверка почты',
                css=url_for('static', filename='css/form.css'),
                js=url_for('static', filename='js/main.js'),
                form=form,
                message="Пользователь с такой почтой не зарегистрирован"
            )
    return render_template(
        'check-email.html',
        title='Guitar House / Восстановление пароля',
        css=url_for('static', filename='css/form.css'),
        js=url_for('static', filename='js/main.js'),
        form=form
    )


@app.route('/change-password/<string:email>', methods=['GET', 'POST'])
def change_password(email):
    #  форма для изменения пароля
    form = ChangePasswordForm()
    """Если пароли совпвадают, то переходим на страницу 
    входа в аккаунт, иначе возвращаем эту же страницу
    с ошибкой"""
    if form.validate_on_submit():
        if form.new_password.data == form.new_password_again.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == email).first()
            if user:
                user.set_password(form.new_password.data)
                db_sess.merge(user)
                db_sess.commit()
                return redirect('/login')
        else:
            return render_template(
                'change-password.html',
                title='Guitar House / Восстановление пароля',
                css=url_for('static', filename='css/form.css'),
                js=url_for('static', filename='js/main.js'),
                form=form,
                email=email,
                message="Пароли не совпадают"
            )
    return render_template(
        'change-password.html',
        title='Guitar House / Восстановление пароля',
        css=url_for('static', filename='css/form.css'),
        js=url_for('static', filename='js/main.js'),
        form=form,
        email=email
    )


# удаление товара
@app.route('/del_product/<int:id>', methods=['GET', 'POST'])
@login_required
def del_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
        return redirect('/account')
    else:
        abort(404)


# редактирование товара
@app.route('/redact_product/<int:id>', methods=['GET', 'POST'])
@login_required
def redact_product(id):
    # форма для редактирования товара
    form = UpdateProductForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        products = db_sess.query(Product).filter(Product.id == id,
                                                 Product.user == current_user
                                                 ).first()
        if products:
            form.name.data = products.title
            form.description.data = products.content
            form.price.data = products.price
        else:
            abort(404)
    """Получаем товар по его id, если такой есть,
    то редактируем его, иначе возвращаем ошибку 404"""
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = db_sess.query(Product).filter(Product.id == id,
                                                 Product.user == current_user
                                                 ).first()
        if products:
            products.title = form.name.data
            products.content = form.description.data
            products.price = form.price.data
            products.category_id = form.category.data
            db_sess.commit()
            return redirect('/account')
        else:
            abort(404)
    return render_template('redact_product.html',
                           css=url_for("static", filename="css/form.css"),
                           js=url_for("static", filename="js/main.js"),
                           title='Guitar House / Редактирование товара',
                           form=form
                           )


# регистрация пользователя
@app.route('/registr', methods=['GET', 'POST'])
def registr():
    # форма регистрации
    form = RegisterForm()
    """Если пароли не совпадают, то переходим на эту же страницу
    и выдаем ошибку, иначе если аккаунт с такой почтой уже существует,
    то переходим на эту же страницу и выдаем ошибку, иначе создаем аккаунт
    и переходим на страницу авторизации"""
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'registr.html',
                title='Guitar House / Регистрация',
                css=url_for('static', filename='css/form.css'),
                js=url_for('static', filename='js/main.js'),
                form=form,
                message='Пароли не совпадают'
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'registr.html',
                title='Guitar House / Регистрация',
                css=url_for('static', filename='css/form.css'),
                js=url_for('static', filename='js/main.js'),
                form=form,
                message='Пользователь с таким email уже существует'
            )
        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            age=form.age.data,
            birthday=form.birthday.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template(
        'registr.html',
        title='Guitar House / Регистрация',
        css=url_for('static', filename='css/form.css'),
        js=url_for('static', filename='js/main.js'),
        form=form
    )


# страница ошибки 404
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html',
                           error=error.code,
                           message="Страница не найдена",
                           title="404 Not Found",
                           css=url_for("static", filename="css/error.css")), 404


# страница ошибки 401
@app.errorhandler(401)
def not_found(error):
    return render_template('error.html',
                           error=error.code,
                           message="У вас нет доступа к этой странице, либо вы не авторизованы",
                           title="401 Unauthorized",
                           css=url_for("static", filename="css/error.css")), 401


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


# запуск приложения
if __name__ == '__main__':
    db_session.global_init("db/gs.db")
    app.register_blueprint(feedbacks_api.blueprint)
    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UserResource, '/api/users/<int:user_id>')
    app.run(port=8080, host='127.0.0.1', debug=True)