import unittest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '/Users/simonvhardy/Documents/Recherche/python_workspace/TP3 solution/pymafia/tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
