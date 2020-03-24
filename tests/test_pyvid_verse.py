import unittest
from vid import __version__, Vid

def test_version():
    assert __version__ == '0.1.0'

TestVids = [
    {
        'vid': Vid([0x15, 0x17, 0x7a, 0x77, 0x83, 0x4f, 0x70, 0x52, 0x31, 0x5d, 0x47, 0x96]),
        'ts': 1519818052.9835212,
        'counter': 123498317825942
    },
    {
        'vid': Vid([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]),
        'ts': 0,
        'counter': 1
    }
]

class TestVid(unittest.TestCase):
    def test_no_duplicates(self):
        collect = []
        for i in range(0, 1000):
            collect.append(Vid())

        ids = [i.string() for i in collect]
        self.assertEqual(len(set(ids)), 1000)

    def test_from_string(self):
        for i in range(0, 1000):
            x = Vid()
            y = Vid.from_string(x.string())

            self.assertEqual(x.value, y.value)
            self.assertEqual(x.bytes(), y.bytes())
            self.assertEqual(x.string(), y.string())

    def test_timestamp(self):
        for x in TestVids:
            self.assertEqual(x.get('vid').time(), x.get('ts'))

    def test_counter(self):
        for x in TestVids:
            self.assertEqual(x.get('vid').counter(), x.get('counter'))

    def test_copy_array_from_golang(self):
        x = Vid([0x15, 0x17, 0x7a, 0x77, 0x83, 0x4f,
                 0x70, 0x52, 0x31, 0x5d, 0x47, 0x96])
        self.assertEqual('2kbnkts39to54cat8ub0', x.string())

    def test_copy_string_from_golang(self):
        x = Vid.from_string('2kbnkts39to54cat8ub0')
        self.assertEqual(x.value, [0x15, 0x17, 0x7a, 0x77, 0x83, 0x4f,
                                   0x70, 0x52, 0x31, 0x5d, 0x47, 0x96])
