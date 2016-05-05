from mock import patch
from unittest import TestCase
import urlparse
import responses

from stathat import StatHat


class TestStatHat(TestCase):

    @patch('stathat.requests')
    def test_init(self, m_requests):
        """
        - Take email
        - Start request sessions
        """

        instance = StatHat('test@example.com')

        m_requests.session.assert_called_with()
        self.assertEqual(instance.email, 'test@example.com')

    @patch('stathat.StatHat.STATHAT_URL', 'http://stathatapi.example')
    @responses.activate
    def test_value(self):
        """
        Send value request to StatHat API
        """
        responses.add(
            responses.POST,
            'http://stathatapi.example/ez',
            body='',
            status=200,
            content_type='application/json'
        )
        instance = StatHat('test@example.com')

        instance.value('a_stat', 'a_value')

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            urlparse.parse_qs(responses.calls[0].request.body),
            {
                'ezkey': ['test@example.com'],
                'stat': ['a_stat'],
                'value': ['a_value']
            }
        )

    @patch('stathat.StatHat.STATHAT_URL', 'http://stathatapi.example')
    @responses.activate
    def test_value_timestamp(self):
        """
        Send value request to StatHat API with timestamp
        """
        responses.add(
            responses.POST,
            'http://stathatapi.example/ez',
            body='',
            status=200,
            content_type='application/json'
        )
        instance = StatHat('test@example.com')

        instance.value('a_stat', 'a_value', 10000)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            urlparse.parse_qs(responses.calls[0].request.body),
            {
                'ezkey': ['test@example.com'],
                'stat': ['a_stat'],
                'value': ['a_value'],
                't': ['10000']
            }
        )

    @patch('stathat.StatHat.STATHAT_URL', 'http://stathatapi.example')
    @responses.activate
    def test_count(self):
        """
        Send value request to StatHat API
        """
        responses.add(
            responses.POST,
            'http://stathatapi.example/ez',
            body='',
            status=200,
            content_type='application/json'
        )
        instance = StatHat('test@example.com')

        instance.count('a_stat', 10)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            urlparse.parse_qs(responses.calls[0].request.body),
            {
                'ezkey': ['test@example.com'],
                'stat': ['a_stat'],
                'count': ['10']
            }
        )

    @patch('stathat.StatHat.STATHAT_URL', 'http://stathatapi.example')
    @responses.activate
    def test_count_timestamp(self):
        """
        Send value request to StatHat API with timestamp
        """
        responses.add(
            responses.POST,
            'http://stathatapi.example/ez',
            body='',
            status=200,
            content_type='application/json'
        )
        instance = StatHat('test@example.com')

        instance.count('a_stat', 10, 10000)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            urlparse.parse_qs(responses.calls[0].request.body),
            {
                'ezkey': ['test@example.com'],
                'stat': ['a_stat'],
                'count': ['10'],
                't': ['10000']
            }
        )
