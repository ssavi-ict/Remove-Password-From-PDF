import hashlib


class CheckHash:
    def __init__(self, pdf_file=None):
        self.pdf_file = pdf_file

    def get_binary_content_in_str(self, pdf_file):
        open_pdf_as_binary = open(pdf_file, "rb")
        binary_content = list(open_pdf_as_binary)
        binary_content_str = ' '.join([str(elem) for elem in binary_content])
        return binary_content_str

    def get_hash_binary_content(self, pdf_file):
        binary_content_str = self.get_binary_content_in_str(pdf_file=pdf_file)
        hash_id = hashlib.sha256(binary_content_str.encode('utf-8')).hexdigest()
        return hash_id


if __name__ == "__main__":
    inst = CheckHash()
    hash_value = inst.get_hash_binary_content(pdf_file="C:\\Users\\user\Documents\Remove-Password-From-PDF\\test\\test_pdf_password_123456-protected - Copyhh.pdf")
    print(hash_value)


