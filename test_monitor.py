import os
import tempfile
import unittest

from monitor import esta_no_ar, ler_sites


class TestMonitor(unittest.TestCase):
    def test_status_ok(self):
        self.assertTrue(esta_no_ar(200))
        self.assertTrue(esta_no_ar(301))

    def test_status_erro(self):
        self.assertFalse(esta_no_ar(404))
        self.assertFalse(esta_no_ar(500))
        self.assertFalse(esta_no_ar(None))

    def test_ler_sites_ignora_comentarios_e_vazios(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
            f.write("# comentario\n\nhttps://exemplo.com\n")
            caminho = f.name
        try:
            self.assertEqual(ler_sites(caminho), ["https://exemplo.com"])
        finally:
            os.remove(caminho)


if __name__ == "__main__":
    unittest.main()
