import unittest

from tmVhdlProducer.algodist import Payload

class PayloadTest(unittest.TestCase):

    def test_payload(self):
        a = Payload()
        self.assertEqual(Payload(slice_luts=0, processors=0, brams=0), a)
        a = Payload(slice_luts=1, processors=2, brams=3)
        self.assertEqual(Payload(slice_luts=1, processors=2, brams=3), a)
        a = Payload(processors=1)
        self.assertEqual(Payload(slice_luts=0, processors=1, brams=0), a)

    def test_add(self):
        a = Payload(slice_luts=3, processors=2, brams=1)
        b = Payload(slice_luts=1, processors=3, brams=5)
        c = a + b
        self.assertEqual(Payload(slice_luts=4, processors=5, brams=6), c)
        c += a
        self.assertEqual(Payload(slice_luts=7, processors=7, brams=7), c)
        c += Payload(slice_luts=1)
        self.assertEqual(Payload(slice_luts=8, processors=7, brams=7), c)
        c += Payload(processors=2)
        self.assertEqual(Payload(slice_luts=8, processors=9, brams=7), c)
        c += Payload(brams=1)
        self.assertEqual(Payload(slice_luts=8, processors=9, brams=8), c)

    def test_equal(self):
        a = Payload(slice_luts=1, processors=2, brams=1)
        b = Payload(slice_luts=1, processors=2, brams=3)
        self.assertEqual(False, a == b)
        a = Payload(slice_luts=1, processors=2, brams=3)
        self.assertEqual(True, a == b)
        self.assertEqual(False, 42 == b)
