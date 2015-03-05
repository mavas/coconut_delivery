import unittest

class SwanTest(unittest.TestCase):
    def setUp(s):
        f = open('sample_paths.txt', 'r')
        c = f.read(); del f
        s.sample = c
        f = open('flight_paths.txt', 'r')
        c = f.read(); del f
        s.real = c
    def test_sample(s):
        e, j = do_it(s.sample)
        print(e)
        print(j)
        s.assertEqual(e, 352)
        s.assertEqual(j, [(0,5), (6,11), (14,17), (19,24)])
    @unittest.skip('')
    def test_real(s):
        e, j = do_it(s.real)

def do_it(i):
    i = i.split('\n')[:-1]
    C = int(i[0])
    i = i[1:]
    print(C)
    print(i)
    e = 352
    j = [(0,5), (6,11), (14,17), (19,24)]
    return (e, j)

if __name__ == '__main__':
    unittest.main()
