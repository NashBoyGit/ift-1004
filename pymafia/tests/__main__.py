import unittest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '/Users/steve.levesque/Desktop/ULaval/TP3/ift-2004/pymafia/tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)