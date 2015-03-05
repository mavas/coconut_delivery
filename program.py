import unittest

class SwanTest(unittest.TestCase):
    def setUp(s):
        f = open('sample_paths.txt', 'r')
        c = f.read(); del f
        s.sample = c
    def test_sample(s):
        e, j = do_it(s.sample)
        s.assertEqual(e, 352)
        s.assertEqual(j, [(0,5), (6,11), (14,17), (19,24)])

def do_it(i):
    e = 352
    j = [(0,5), (6,11), (14,17), (19,24)]
    return (e, j)

if __name__ == '__main__':
    unittest.main()
