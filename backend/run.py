# использовать только при разработке и отладке
# в продакшен среде используется:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
