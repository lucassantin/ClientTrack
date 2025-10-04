from controllers.main_controller import MainController
from data.init_db import initialize_database


if __name__ == "__main__":
    initialize_database()
    MainController().iniciar()