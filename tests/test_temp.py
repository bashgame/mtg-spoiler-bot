"""
Template Test Cases, please update
"""
import aiohttp
from unittest import IsolatedAsyncioTestCase as TestCase
from modules import mtgSpoilers

class TestSpoilers(TestCase):
    """ Tests for methods to scrape mtg-spoilers """

    @classmethod
    def setUpClass(cls):
        """ Setup some variables """
        cls.expected_sets = {'ltc','ltr','cmm','mat','mul','moc','mom','sis','sir'}
        cls.expected_cards = {
            "8dc1b381-fbc4-451c-a468-2beaa344a581",
            "601402f4-8647-4c41-9a0f-63d10ce89d02",
            "5805f64c-dd88-4e94-8f0a-a01dae67e3ba"
        }

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

    async def test_get_sets(self):
        """ It should return a dictionary of sets that aren't released yet """
        session = aiohttp.ClientSession()
        set_codes = set()
        result = await mtgSpoilers.get_latest_sets(session)
        set_codes |= {key for key in result.keys()}
        self.assertEqual(self.expected_sets, set_codes)


    async def test_get_spoilers(self):
        """ It should return a list of cards in a set """
        session = aiohttp.ClientSession()
        card_codes = set()
        result = await mtgSpoilers.get_new_spoilers(session, 'ltc')
        card_codes |= {card_data['id'] for card_data in result}
        self.assertLessEqual(self.expected_cards, card_codes)
