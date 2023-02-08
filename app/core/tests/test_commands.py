"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command  # call commands with name for testing
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch("core.management.commands.wait_for_db.Command.check")  # mock db behaviour, BaseCommand içerisinde yer alan check method'unu mockluyoruz.
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True  # patched_check burada özel bir isim komudun dönüşünü her türlü True yapıyor.

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])  # doğru db'yi çağırıyor muyuz aslında bunu test ediyor.

    # Bu testte bir exception oluşmasını istiyoruz.
    @patch("time.sleep")  # db'ye istek attığımızda bir süre bekleyip ardından ikinci isteği göndermek istediğimiz bu beklemyi de mockluyoruz.
    def test_wait_for_db_delay(self, patched_sleep, patched_check): # patched_sleep ve patched_check sırası önemli aşağıdan yukarıya giden decorator sırası ile eklenmeli
        """Test waiting for database when getting OperationalError"""
        # Exception oluşurken mock bu şekilde çalışmaktadır. 5 defa exception üretecek bu sayıyı gerçekçi olması için kendimiz 2 ve 3 şeklinde verdik, ardından 6. True dönecektir.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)  # 6 defa çağıracağız ve sonunda bağlantıyı sağlamış yani True değerini almış olacağız.
        patched_check.assert_called_with(databases=["default"])
