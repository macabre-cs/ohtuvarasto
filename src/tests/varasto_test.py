import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_ota_varastosta_liikaa(self):
        self.varasto.lisaa_varastoon(5)
        saatu = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu, 5)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)

    def test_ota_varastosta_negatiivinen_maara(self):
        alku_saldo = self.varasto.saldo
        saatu = self.varasto.ota_varastosta(-3)
        self.assertAlmostEqual(saatu, 0.0)
        self.assertAlmostEqual(self.varasto.saldo, alku_saldo)

    def test_lisaa_varastoon_liikaa(self):
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_lisaa_varastoon_negatiivinen_maara(self):
        alku_saldo = self.varasto.saldo
        self.varasto.lisaa_varastoon(-5)
        self.assertAlmostEqual(self.varasto.saldo, alku_saldo)

    def test_negatiivinen_tilavuus(self):
        v = Varasto(-5)
        self.assertAlmostEqual(v.tilavuus, 0.0)

    def test_negatiivinen_alku_saldo(self):
        v = Varasto(10, -3)
        self.assertAlmostEqual(v.saldo, 0.0)

    def test_alku_saldo_suurempi_kuin_tilavuus(self):
        v = Varasto(10, 15)
        self.assertAlmostEqual(v.saldo, 10.0)
    
    def test_str_palauttaa_oikean_merkkijonon(self):
        self.varasto.lisaa_varastoon(5)
        merkkijono = str(self.varasto)
        self.assertEqual(merkkijono, "saldo = 5, vielä tilaa 5")
