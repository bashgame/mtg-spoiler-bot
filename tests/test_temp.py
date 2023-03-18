"""
Template Test Cases, please update
"""
import aiohttp
from unittest import TestCase
from modules import mtgSpoilers

class TestSpoilers(TestCase):
    """ Tests for methods to scrape mtg-spoilers """

    @classmethod
    def setUpClass(cls):
        """ Setup some variables """
        cls.expected_sets = {'ltc','ltr','cmm','mat','mul','moc','mom','sis','sir'}

    @classmethod
    def tearDownClass(cls):
        """ Do something to clean up tests, please update """

    def setUp(self):
        """ Ensure each test runs clean, please update """

    def tearDown(self):
        """ Ensure each test runs clean, please update """

    ###########################################################################
    #   T E S T  C A S E S
    ###########################################################################

    def test_get_sets(self):
        """ It should return a dictionary of sets that aren't released yet """
        session = aiohttp.ClientSession()
        set_codes = set()
        result = mtgSpoilers.get_latest_sets(session)
        set_codes |= {result.keys()}
        self.assertEqual(self.expected_sets, set_codes)
        
