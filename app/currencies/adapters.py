import csv

from abc import abstractmethod
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class AbstractFileResponseAdapter:

    def __init__(self, type):
        self.default_filename = f'result.{type}'
        self.response = HttpResponse(content_type=f'{self.get_mime_type()}')

    @abstractmethod
    def get_mime_type(self):
        pass

    def get_filename(self, filename):
        if filename: return filename
        return self.default_filename

    @abstractmethod
    def create_file(self, filename=None):
        self.response['Content-Disposition'] = f'attachment; filename="{self.get_filename(filename)}"'
        pass

    @abstractmethod
    def write_header(self, header_row):
        pass

    @abstractmethod
    def write_content(self, content):
        pass

    @abstractmethod
    def get_response(self):
        pass


class CsvFileResponseAdapter(AbstractFileResponseAdapter):

    def get_mime_type(self):
        return 'text/csv'

    def create_file(self, filename=None):
        self.writer = csv.writer(self.response)

    def write_row(self, content):
        self.writer.writerow(content)

    def write_header(self, header_row):
        self.write_row(header_row)

    def write_content(self, content):
        self.write_row(content)

    def get_response(self):
        return self.response

class PdfFileResponseAdapter(AbstractFileResponseAdapter):

    def get_mime_type(self):
        return 'application/pdf'

    def create_file(self, filename=None):
        self.canvas = canvas.Canvas(self.response)

    def write_row(self, x, y, content):
        self.canvas.drawString(x, y, content)

    def write_header(self, header_row):
        y = 700
        for header in header_row:
            self.write_row(50, y, header)
            y -= 50

    def write_content(self, content):
        y = 700
        for c in content:
            self.write_row(200, y, str(c))
            y -= 50

    def get_response(self):
        self.close_document()
        return self.response

    def close_document(self):
        self.canvas.showPage()
        self.canvas.save()