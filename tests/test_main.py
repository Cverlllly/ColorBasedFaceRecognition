import unittest
import numpy as np
import cv2 as cv
from main import zmanjsaj_sliko, nared_skatle_na_sliki, prestej_piklse_z_barvo_koze


class TestFunkcije(unittest.TestCase):

    def test_zmanjsaj_sliko(self):
        slika = np.ones((100, 100, 3), dtype=np.uint8) * 255
        nova = zmanjsaj_sliko(slika, 50, 50)
        self.assertEqual(nova.shape, (50, 50, 3))

    def test_nared_skatle_na_sliki(self):
        slika = np.zeros((100, 100, 3), dtype=np.uint8)
        skatle = nared_skatle_na_sliki(slika, 50, 50)
        self.assertEqual(len(skatle), 4)

    def test_prestej_piklse_z_barvo_koze(self):
        slika = np.full((10, 10, 3), (100, 150, 200), dtype=np.uint8)
        barva = (100, 150, 200)
        rezultat = prestej_piklse_z_barvo_koze(slika, barva)
        self.assertEqual(rezultat, 100)


if __name__ == '__main__':
    unittest.main()
