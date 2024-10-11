import itertools
import threading
import time

from InquirerPy import inquirer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings
from userfetchapi.models.user_model import SessionLocal
from userfetchapi.services.user_service import fetch_and_store_users, verify_database

stop_loading = False


def loading_animation() -> None:
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_loading:
            break
        print(f"\rPopulando banco de dados... {char}", end="")
        time.sleep(0.1)


def populate_database(db: Session, user_count: int) -> None:
    global stop_loading
    stop_loading = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    fetch_and_store_users(db, int(user_count))

    stop_loading = True
    loading_thread.join()

    print(f"{user_count} usuários foram populados no banco de dados!")


def install() -> None:
    db_choice = inquirer.select(
        message="Escolha o banco de dados:",
        choices=["SQLite", "MySQL"],
    ).execute()

    if db_choice == "SQLite":
        env = "SQLITE"
    else:
        db_user = inquirer.text(message="Digite o usuário do MySQL:").execute()
        db_pass = inquirer.secret(message="Digite a senha do MySQL:").execute()
        db_host = inquirer.text(
            message="Digite o host do MySQL:", default="localhost"
        ).execute()
        db_name = inquirer.text(message="Digite o nome do banco de dados:").execute()
        env = "MYSQL"

        with open(".env", "w") as env_file:
            env_file.write(f"""
            DB_USER={db_user}\n
            DB_PASS={db_pass}\n
            DB_HOST={db_host}\n
            DB_NAME={db_name}\n
            """)
    settings.env = env
    print("Configuração do banco de dados salva!")

    user_count = inquirer.text(
        message="Quantos usuários você quer popular no banco de dados?", default="100"
    ).execute()
    engine = create_engine(settings.DATABASE_URL)

    db = SessionLocal(bind=engine)

    print(f"O banco de dados já possui {verify_database(db)} usuário(s)?")

    confirm = inquirer.confirm(
        message=f"O banco de dados já possui {verify_database(db)} usuário(s). Continuar?",
        default=True,
    ).execute()

    if confirm:
        populate_database(db, user_count)

    print(
        "Fim da configuração. Para rodar a API, execute 'uvicorn userfetchapi.main:app --reload'."
    )


if __name__ == "__main__":
    install()
