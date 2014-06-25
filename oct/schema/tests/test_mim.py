from ming import mim
import unittest


class TestMim(unittest.TestCase):

    def setUp(self):
        # self.connection = Connection()
        self.connection = mim.Connection()
