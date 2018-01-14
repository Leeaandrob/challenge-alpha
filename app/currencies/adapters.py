import csv

from abc import abstractmethod
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class AbstractFileResponseAdapter:
    """
    Classe que define os comportamentos necessários para criar e manipular
    os arquivos que são enviados na response.
    """

    def __init__(self, type):
        """
        Inicializa os atributos do objeto com valores padrão.
        :param type: tipo do arquivo
        """
        self.default_filename = f'result.{type}'
        self.response = HttpResponse(content_type=f'{self.get_mime_type()}')

    @abstractmethod
    def get_mime_type(self):
        """
        Retorna o mime type do arquivo.
        :return mime_type:
        """
        pass

    def get_filename(self, filename):
        """
        Retorna o nome para o arquivo que será enviado como response.
        :param filename: nome do arquivo
        :return filename: nome do arquivo especificado ou nome do arquivo padrão
        """
        if filename: return filename
        return self.default_filename

    @abstractmethod
    def create_file(self, filename=None):
        """
        Executa os procedimentos necessários para criar um arquivo.
        :param filename: nome do arquivo
        """
        self.response['Content-Disposition'] = f'attachment; filename="{self.get_filename(filename)}"'
        pass

    @abstractmethod
    def write_header(self, header_row):
        """
        Escreve cada item da lista header_row como cabeçalho do arquivo.
        :param header_row: lista de strings, onde cada string representa um
        item do cabeçalho.
        """
        pass

    @abstractmethod
    def write_content(self, content):
        """
        Escreve cada item da lista content como um item do arquivo.
        :param content: lista de strings, onde cada string representa um
        item do conteúdo.
        """
        pass

    @abstractmethod
    def get_response(self):
        """
        Retorna o objeto response configurado.
        :return: self.response
        """
        pass


class CsvFileResponseAdapter(AbstractFileResponseAdapter):
    """
    Classe que implementa os métodos necessários para enviar um csv como response.
    """

    def __init__(self):
        AbstractFileResponseAdapter.__init__(self, 'csv')

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
    """
    Classe que implementa os métodos necessários para enviar um pdf como response.
    """

    def __init__(self):
        AbstractFileResponseAdapter.__init__(self, 'pdf')

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
        """
        Fecha o documento e finaliza a edição.
        """
        self.canvas.showPage()
        self.canvas.save()