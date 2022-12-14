import pikepdf
import os
import shutil
from progress.bar import Bar


class PasswordRemover:
    def __init__(self) -> None:
        self.pdf_path = None
        self.pdf_pass = None

    @staticmethod
    def decision_from_user_about_directory():
        print("\nDo you want to decrypt a single PDF file ?")
        print("Or do you want to decrypt all the files in directory ?")
        print("1. Only one PDF.")
        print("2. All PDF in a directory.")
        print("99. Halt The Process.\n")
        user_choice = input('Enter your choice from above options - ')
        return user_choice

    @staticmethod
    def decrypt_pdf(my_pdf_location, my_pdf_password, my_save_location):
        exception = None
        try:
            my_pdf = pikepdf.open(my_pdf_location, password=my_pdf_password)
            my_pdf.save(my_save_location)
            print("Current PDF decrypted and saved to " + my_save_location)
        except pikepdf._qpdf.PasswordError as error:
            exception = error
            print("Wrong password given.")
        except pikepdf._qpdf.PdfError as damage:
            exception = damage
            print("This PDF is damaged.")
        return exception

    def validate_pdf_password(self, pdf_path, pdf_password):
        if pdf_path is None or pdf_password is None:
            return False

        try:
            with pikepdf.open(pdf_path, password=pdf_password) as p:
                is_valid = True
        except pikepdf._qpdf.PasswordError as e:
            is_valid = False
        return is_valid

    def decrypt_a_single_pdf(self, pdf_location, pdf_password):
        original_file_directory = os.path.dirname(pdf_location)
        original_file_name = os.path.basename(pdf_location)

        decrypted_directory = os.path.join(original_file_directory, 'decrypted')
        if os.path.exists(decrypted_directory):
            shutil.rmtree(decrypted_directory, ignore_errors=True)
        os.mkdir(decrypted_directory)

        save_location = os.path.join(decrypted_directory, "decrypted_" + original_file_name)
        return save_location, PasswordRemover.decrypt_pdf(pdf_location, pdf_password, save_location)

    def decrypt_multiple_pdfs_in_a_directory(self, pdf_location, pdf_password):
        decrypted_directory = os.path.join(pdf_location, 'decrypted')
        if os.path.exists(decrypted_directory):
            shutil.rmtree(decrypted_directory, ignore_errors=True)
        os.mkdir(decrypted_directory)

        any_exception = None
        all_pdfs = os.listdir(pdf_location)
        with Bar('Processing', max=len(all_pdfs), fill='*', suffix='%(percent)d%%') as bar:
            for file in all_pdfs:
                if file.endswith(".pdf"):
                    file_location = os.path.join(pdf_location, file)
                    save_location = os.path.join(decrypted_directory, file)
                    returned_status = PasswordRemover.decrypt_pdf(file_location, pdf_password, save_location)
                    if returned_status is not None:
                        any_exception = returned_status
                    bar.next()

        return any_exception

    def decrypt_pdf_and_save_into_a_directory(self, user_choice, pdf_location, pdf_password):
        saved_location = None
        got_any_exception = None
        if user_choice == '1':
            saved_location, got_any_exception = self.decrypt_a_single_pdf(pdf_location=pdf_location, pdf_password=pdf_password)
        if user_choice == '2':
            got_any_exception = self.decrypt_multiple_pdfs_in_a_directory(pdf_location=pdf_location,
                                                                          pdf_password=pdf_password)

        if got_any_exception is None:
            print("Done Decrypting PDF(s)")
        else:
            print("There are some issues with decrypting PDF(s)")
        return saved_location, got_any_exception is None

    def decrypt_my_pdf(self):
        user_choice = PasswordRemover.decision_from_user_about_directory()
        if user_choice != '1' and user_choice != '2':
            if user_choice != '99':
                print('Wrong Input Given.')
            print("Halting the Process..... ")
            return

        if user_choice == '1':
            self.pdf_path = input('Insert the PDF Path: ')

        if user_choice == '2':
            self.pdf_path = input(
                'Insert the PDF Directory. Press ENTER if you want to decrypt PDFs of current directory : ')
            if not self.pdf_path:
                self.pdf_path = os.getcwd()

        self.pdf_pass = input('Insert the PDF password correctly : ')
        self.decrypt_pdf_and_save_into_a_directory(user_choice, self.pdf_path, self.pdf_pass)


if __name__ == "__main__":
    p_remover = PasswordRemover()
    p_remover.decrypt_my_pdf()
