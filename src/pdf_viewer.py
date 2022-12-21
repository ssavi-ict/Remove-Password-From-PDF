import subprocess


class PDFViewer:
    def __init__(self):
        pass

    def show_specific_pdf(self, pdf_path):
        print("Launching PDF in PDF Viewer .... ")
        subprocess.Popen(pdf_path, shell=True)


if __name__ == "__main__":
    inst = PDFViewer()
    inst.show_specific_pdf(
        pdf_path='C:\\Users\\user\Documents\\GitHubRepo\\Remove-Password-From-PDF\\test\\decrypted\\decrypted_test_pdf_password_123456-protected - Copy.pdf')
