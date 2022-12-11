import os
from src.prgui import PasswordRemoverGUI
from constant import Constants


class Runner:
    def __init__(self):
        self.cwd = os.getcwd()
        self.password_storage_dir = os.path.join(self.cwd, "res", "secured")
        self.password_storage_file_name = Constants().password_file_name
        self.password_file_path = os.path.join(self.password_storage_dir, self.password_storage_file_name)
        if not os.path.exists(self.password_file_path):
            with open(self.password_file_path, "w") as file:
                file.write('{\n}')
            file.close()


if __name__ == "__main__":
    Runner()
    pr_instance = PasswordRemoverGUI()
    pr_instance.decrypt_pdf_gui()
