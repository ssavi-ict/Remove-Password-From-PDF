import json
import os
import sys
import src.hashcheck as hcheck
from constant import Constants


class PasswordAction:
    def __init__(self):
        self.cwd = os.path.abspath(__file__)
        self.parent_dir = os.path.dirname(os.path.dirname(self.cwd))
        self.password_storage_dir = os.path.join(self.parent_dir, "res", "secured")
        sys.path.append(self.password_storage_dir)
        self.read_pw_file = open(self.password_storage_dir + os.path.sep + Constants().password_file_name, "r+")
        self.passwords = json.load(self.read_pw_file)
        self.hash_checker = hcheck.CheckHash()

    def password_exist_for_this_pdf_by_hash(self, pdf_path):
        pdf_hash = self.hash_checker.get_hash_binary_content(pdf_file=pdf_path)
        if pdf_hash in self.passwords:
            return True, self.passwords[pdf_hash]
        return False, None

    def save_password_for_this_pdf_by_hash(self, pdf_path, password, pass_found):
        pdf_hash = self.hash_checker.get_hash_binary_content(pdf_file=pdf_path)
        if pass_found:
            print("Updating password for - " + pdf_path)
            self.passwords[pdf_hash] = password
            print("Password Updated ... ")
        else:
            print("Saving password for " + pdf_path)
            new_json_item = {pdf_hash: password}
            self.passwords.update(new_json_item)
            print("Password Saved ... ")
        self.read_pw_file.seek(0)
        json.dump(self.passwords, self.read_pw_file, indent=4)

    '''def password_exist_for_this_pdf_by_path(self, pdf_path):
            pdf_path = pdf_path.replace('\\', '|')
            if pdf_path in self.passwords:
                return True, self.passwords[pdf_path]
            return False, None
    '''
    '''def save_password_for_this_pdf_by_path(self, pdf_path, password, pass_found):
            pdf_path = pdf_path.replace('\\', '|')
            if pass_found:
                print("Updating password for - " + pdf_path)
                self.passwords[pdf_path] = password
                print("Password Updated ... ")
            else:
                print("Saving password for " + pdf_path)
                new_json_item = {pdf_path: password}
                self.passwords.update(new_json_item)
                print("Password Saved ... ")
            self.read_pw_file.seek(0)
            json.dump(self.passwords, self.read_pw_file, indent=4)
            
    '''


if __name__ == "__main__":
    inst = PasswordAction()
    print(inst.cwd)
    print(inst.parent_dir)
    print(inst.password_storage_dir)
    print(inst.passwords)
    print(inst.password_exist_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copyhh.pdf"))

    inst.save_password_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copyhh.pdf",
        password="1234560",
        pass_found=False
    )

    pass_found, password = inst.password_exist_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copyhh.pdf"
    )

    print(pass_found, password)

    pass_found, password = inst.password_exist_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copy12.pdf"
    )

    print(pass_found, password)

    inst.save_password_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copy12.pdf",
        password="1234560",
        pass_found=True
    )

    print(pass_found, password)

    pass_found, password = inst.password_exist_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copy22.pdf"
    )

    print(pass_found, password)

    inst.save_password_for_this_pdf_by_hash(
        pdf_path="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copy22.pdf",
        password="1234569",
        pass_found=True
    )
    print(inst.passwords)
