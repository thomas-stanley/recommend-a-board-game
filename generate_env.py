import secrets
from pathlib import Path

def generate_env(environment):
    secret_key = secrets.token_urlsafe()
    content = f"""
SECRET_KEY={secret_key}
FLASK_ENV={environment}"""
    Path(".env").write_text(content)

if __name__ == "__main__":
    generate_env("production")

