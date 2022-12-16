import PySimpleGUI as sg
from src.password_remover import PasswordRemover as pr
from src.password import PasswordAction


class PasswordRemoverGUI:
    def __int__(self):
        # self.pw_action = PasswordAction()
        pass

    def select_a_pdf_file(self):
        sg.theme("DarkTeal2")
        select_file = [[sg.T("")], [sg.Text("Choose a pdf file and click SUBMIT: "), sg.Input(), sg.FileBrowse(key="-IN-")],
                  [sg.Button("SUBMIT")]]

        pdf_path = None
        window = sg.Window('Choose a PDF File to Decrypt', select_file, size=(700, 150))
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            sg.popup_auto_close("No File Selected", auto_close_duration=1)
        elif event == "SUBMIT":
            pdf_path = values["-IN-"]
        window.close()
        return pdf_path

    def select_a_directory(self):
        sg.theme("DarkTeal2")
        select_directory = [[sg.T("")], [sg.Text("Choose a directory and click SUBMIT: "), sg.Input(),
                               sg.FolderBrowse(key="-IN-")], [sg.Button("SUBMIT")]]
        window = sg.Window('Choose a directory', select_directory, size=(700, 150))

        # while True:
        pdf_path = None
        event, values = window.read()
        # print(values["-IN2-"])
        if event == sg.WIN_CLOSED or event == "Exit":
            sg.popup_auto_close("No Directory Selected", auto_close_duration=5)
        elif event == "SUBMIT":
            pdf_path = values["-IN-"]
        window.close()
        return pdf_path

    def ask_for_password(self, additional_message):
        password_layout = [
            [sg.Text(additional_message + 'Please enter correct PDF password to decrypt')],
            [sg.Text('Password', size=(15, 1)), sg.InputText(key='-password-', password_char='*')],
            [sg.Checkbox('Remember Password ?',
                         key='save_pass', default=True,
                         tooltip="By ticking on Remember Password, system will not ask you for password for this PDF in future.")
            ],
            [sg.Button('SUBMIT')]
        ]
        window = sg.Window('Enter Password', password_layout, size=(700, 150))

        pdf_pass = None
        remember_password = None
        event, values = window.read()
        # print(values["-IN2-"])
        if event == sg.WIN_CLOSED or event == "Exit":
            sg.popup_auto_close("No Password Given", auto_close_duration=5)
        elif event == "SUBMIT":
            pdf_pass = values["-password-"]
            remember_password = values["save_pass"]
        window.close()
        return pdf_pass, remember_password

    def get_the_pdf_path(self):
        sg.theme("DarkTeal2")
        choice_box = [
            [sg.Text('Do you want to decrypt - ', justification='left')],
            [sg.Radio(text='Only one PDF', group_id='type_dec', key='one_pdf', default=True)
             # ,sg.Radio(text='All PDF in a directory', group_id='type_dec', key='all_pdf')
            ],
            [sg.Button('NEXT'), sg.Button('CANCEL')]
        ]

        users_choice = '99'
        pdf_path = None

        window = sg.Window('Choose your option', choice_box, resizable=True, size=(700, 150))
        event, values = window.read()
        if event == 'NEXT':
            if values['one_pdf']:
                # print(values['one_pdf'])
                pdf_path = self.select_a_pdf_file()
                users_choice = '1'
                # print(users_choice, pdf_path)
            elif values['all_pdf']:
                print('All PDF', values['all_pdf'])
                users_choice = '2'
                pdf_path = self.select_a_directory()
                # print(users_choice, pdf_path)
            window.close()
        else:
            sg.popup_auto_close("CANCEL or [X] Button Clicked", auto_close_duration=5)
        return users_choice, pdf_path

    def get_the_pdf_password(self, pdf_path):
        pw_action = PasswordAction()
        pdf_password = None
        remember_password = None
        if pdf_path:
            pass_found, current_password = pw_action.password_exist_for_this_pdf_by_hash(pdf_path=pdf_path)
            if pass_found:
                pdf_password = current_password
                if not pr().validate_pdf_password(pdf_path=pdf_path, pdf_password=pdf_password):
                    pdf_password, remember_password = self.ask_for_password(
                        additional_message="\nFound an already used password for this PDF. "
                                           "Although the saved password is incorrect.\n"
                    )
            else:
                pdf_password, remember_password = self.ask_for_password(additional_message="")

        '''if remember_password:
            pw_action.save_password_for_this_pdf_by_hash(pdf_path=pdf_path, password=pdf_password, pass_found=False)'''
        return pdf_password, remember_password

    def choose_from_option(self):
        users_choice, pdf_path = self.get_the_pdf_path()
        pdf_password, remember_password = self.get_the_pdf_password(pdf_path=pdf_path)
        return users_choice, pdf_path, pdf_password, remember_password

    def decrypt_pdf_gui(self):
        user_choice, pdf_path, pdf_password, remember_password = self.choose_from_option()
        # print(pdf_path, pdf_password)
        if pdf_path and pdf_password:
            pr_instance = pr()
            if pr_instance.decrypt_pdf_and_save_into_a_directory(user_choice=user_choice, pdf_location=pdf_path, pdf_password=pdf_password) is True :
                sg.popup_auto_close("PDF decryption successful", auto_close_duration=5)
                if remember_password:
                    PasswordAction().save_password_for_this_pdf_by_hash(pdf_path=pdf_path, password=pdf_password, pass_found=False)
            else:
                sg.popup_auto_close("All/Some PDF has some issues in decrypting.", auto_close_duration=5)
        else:
            print("Either PDF path and/or PDF password is not given.")


if __name__ == "__main__":
    inst = PasswordRemoverGUI()
    # inst.select_a_pdf_file()
    inst.decrypt_pdf_gui()
