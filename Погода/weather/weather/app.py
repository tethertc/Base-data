from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from datetime import datetime, date, timedelta # <-- ИЗМЕНЕНИЕ
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# --- Конфигурация Flask и SQLAlchemy ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Настройки БД (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Секретный ключ (ОБЯЗАТЕЛЕН для сессий, аутентификации и flash-сообщений)
app.secret_key = 'ваш_очень_секретный_и_длинный_ключ' 

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Куда перенаправлять неавторизованных пользователей
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ к этой странице."

# --- Константы API ---
# ВНИМАНИЕ: Замените этот ключ своим собственным, если он не работает!
API_KEY = 'b2aa940a64be17f4b1794704226fcc82' 

# --- Модель базы данных (User) ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    password_hash = db.Column(db.String(128), nullable=False) 
    preferred_city = db.Column(db.String(100), nullable=True, default='Алматы') # Город по умолчанию

    def set_password(self, password):
        """Хеширование пароля для безопасного хранения."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверка введенного пароля с хешем из БД."""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    """Callback для Flask-Login: загрузка пользователя по ID."""
    # Используем db.session.get() для SQLAlchemy >= 2.0
    return db.session.get(User, int(user_id)) 

# --- Вспомогательная функция для погоды (Обновлено) ---
def get_weather_forecast(city, selected_days):
    """Получает прогноз погоды из OpenWeatherMap, группируя почасовые данные по дням."""
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url_forecast)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != "200":
            return None, f'Такого города "{city}" не существует. Попробуйте еще раз.'

        # Определяем даты для меток 'Сегодня' и 'Завтра' в формате YYYY-MM-DD
        today_date_str = date.today().strftime("%Y-%m-%d")
        tomorrow_date_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        daily_grouped_data = defaultdict(list)
        # Группируем 3-часовые записи по дате
        for entry in data['list']:
            date_str = entry['dt_txt'].split(' ')[0]
            daily_grouped_data[date_str].append(entry)

        weather_data_by_day = []
        dates = list(daily_grouped_data.keys())
        dates = dates[:selected_days] # Ограничиваем выбранным количеством дней

        for date_str in dates: # ИЗМЕНЕНИЕ: используем date_str
            entries = daily_grouped_data[date_str]
            
            # Определяем метку для дня
            day_label = ""
            if date_str == today_date_str:
                day_label = " (Сегодня)"
            elif date_str == tomorrow_date_str:
                day_label = " (Завтра)"
            
            # Агрегированные данные за день
            temps = [e['main']['temp'] for e in entries]
            descriptions = [e['weather'][0]['description'] for e in entries]
            icons = [e['weather'][0]['icon'] for e in entries]

            # Список почасовых (3-часовых) данных для детализации
            hourly_details = []
            for entry in entries:
                # Преобразование времени в более читаемый формат ЧЧ:ММ
                time_str = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime('%H:%M')
                hourly_details.append({
                    'time': time_str,
                    'temp': round(entry['main']['temp'], 1),
                    'description': entry['weather'][0]['description'],
                    'icon': entry['weather'][0]['icon'],
                    'humidity': entry['main']['humidity']
                })


            day_forecast = {
                # --- ИЗМЕНЕНИЕ: Форматируем дату как ДД.ММ.ГГГГ ---
                'date': datetime.strptime(date_str, "%Y-%m-%d").strftime('%d.%m.%Y'),
                'day_label': day_label, # <-- НОВОЕ ПОЛЕ
                'temp_max': round(max(temps), 1), 
                'temp_min': round(min(temps), 1),
                'main_description': max(set(descriptions), key=descriptions.count),
                'main_icon': max(set(icons), key=icons.count),
                'hourly_details': hourly_details 
            }
            weather_data_by_day.append(day_forecast)

        return weather_data_by_day, None

    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            return None, f'Такого города "{city}" не существует. Попробуйте еще раз.'
        else:
            return None, f"Ошибка HTTP: {http_err}"
    except requests.exceptions.RequestException as e:
        return None, f"Ошибка при получении данных: {e}"

# --- Маршруты аутентификации ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Проверка, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Пользователь с таким логином уже существует.', 'error')
            return redirect(url_for('register'))

        # Создание нового пользователя
        new_user = User(username=username)
        new_user.set_password(password) # <-- Хеширование пароля
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Вы успешно зарегистрированы! Пожалуйста, войдите.', 'success')
        return redirect(url_for('login')) # Перенаправление на страницу входа
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Проверка логина и пароля
        if user is None or not user.check_password(password):
            flash('Неверный логин или пароль.', 'error')
            return redirect(url_for('login'))
            
        login_user(user) # Вход пользователя
        flash(f'Добро пожаловать, {user.username}!', 'success')
        
        # Перенаправление на страницу, с которой был запрос (если была), или на главную
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required # Требует авторизации для доступа
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

# --- Основной маршрут ---
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None
    selected_days = 5
    city = None
    city_to_check = None

    if request.method == 'POST':
        # 1. Обработка данных из формы
        city = request.form.get('city')
        days = request.form.get('days', '5')
        selected_days = int(days) if days in ['1', '5'] else 5

        if not city:
            error_message = "Пожалуйста, введите название города."
        else:
            city_to_check = city
            
            # 2. Обновление предпочтительного города (если авторизован)
            if current_user.is_authenticated and city_to_check != current_user.preferred_city:
                # Сначала проверяем, что город существует
                temp_weather, temp_err = get_weather_forecast(city_to_check, selected_days)
                if not temp_err:
                    current_user.preferred_city = city_to_check
                    db.session.commit()
                    flash(f'Ваш предпочитаемый город обновлён на: {city_to_check}', 'info')
                # Если город не существует, error_message будет установлен ниже

    # 3. Если GET-запрос или не POST-запрос с городом
    if not city_to_check:
        if current_user.is_authenticated and current_user.preferred_city:
            # Используем город из профиля
            city_to_check = current_user.preferred_city
        else:
            # Город по умолчанию для неавторизованных
            city_to_check = 'Алматы' 
            
    # 4. Получение погоды
    if city_to_check:
        weather_data, current_error = get_weather_forecast(city_to_check, selected_days)
        
        # Если POST был с ошибкой, сохраняем ошибку POST. Иначе используем ошибку погоды.
        if not error_message: 
            error_message = current_error
            
        city = city_to_check # Устанавливаем город для отображения в поле ввода

    return render_template('index.html', 
                           weather=weather_data, 
                           error=error_message, 
                           selected_days=selected_days, 
                           city=city)

# --- Инициализация базы данных ---
if __name__ == '__main__':
    with app.app_context():
        # Создаст файл app.db, если его нет, с обновленной схемой.
        db.create_all() 
    app.run(debug=True)