import secrets
import sys
from pathlib import Path

def generate_env(environment):
    secret_key = secrets.token_urlsafe()
    content = f"""
SECRET_KEY={secret_key}
FLASK_ENV={environment}"""
    Path(".env").write_text(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        env = sys.argv[1]
        valid_env = ["default", "production", "development", "testing"]
        if env in valid_env:
            generate_env(env)

