from django.test import TestCase

import os

from surface import processor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProcessorTest(TestCase):

    def test_xlsx_processing(self):
        xlsx_file = os.path.join(BASE_DIR, '../tests/testdata/dataset_fjveqerc.xlsx')
        
        document = processor.Document()
        document.load_from_file(xlsx_file)
        self.assertEqual(document.x, 6.79572540487971e+18)
        self.assertEqual(document.status, 'removed')


