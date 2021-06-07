from aiohttp.test_utils import unittest_run_loop
from asynctest import TestCase, MagicMock, CoroutineMock

from app.models.exchange_rate import ExchangeRateModel
from app.services.mongo import ExchangeRateService


# from freezegun import freeze_time

# @freeze_time("2019-04-02")

class ExchangeRateServiceTest(TestCase):

    def setUp(self):
        self.collection = MagicMock()
        self.service = ExchangeRateService(self.collection)

    @unittest_run_loop
    async def test_find_one(self):
        exchange_from = 'BRL'
        exchange_to = 'USD'
        exchange_tax = 5
        self.collection.find_one = CoroutineMock(return_value={
            'exchange_from': exchange_from,
            'exchange_to': exchange_to,
            'exchange_tax': exchange_tax,
        })

        exchange_rate = await self.service.find_one(exchange_from, exchange_to)

        self.assertIsNotNone(exchange_rate)
        self.assertEqual(exchange_from, exchange_rate.exchange_from)
        self.assertEqual(exchange_to, exchange_rate.exchange_to)
        self.assertEqual(exchange_tax, exchange_rate.exchange_tax)
        self.collection.find_one.assert_awaited_once({
            'exchange_from': exchange_from,
            'exchange_to': exchange_to
        })

    @unittest_run_loop
    async def test_find(self):
        exchange_from = 'BRL'
        exchange_to = 'USD'
        exchange_tax = 5
        to_list = CoroutineMock(return_value=[{
            'exchange_from': exchange_from,
            'exchange_to': exchange_to,
            'exchange_tax': exchange_tax,
        }])

        self.collection.find.return_value = MagicMock(to_list=to_list)

        result = await self.service.find()

        self.assertNotEqual(result.exchange_rates, [])
        self.assertEqual(exchange_from, result.exchange_rates[0].exchange_from)
        self.assertEqual(exchange_to, result.exchange_rates[0].exchange_to)
        self.assertEqual(exchange_tax, result.exchange_rates[0].exchange_tax)
        self.collection.find.assert_called_once_with({})
        to_list.assert_awaited_once(None)

    @unittest_run_loop
    async def test_find_one_returns_none(self):
        exchange_from = 'BRL'
        exchange_to = 'USD'
        self.collection.find_one = CoroutineMock(return_value={})

        exchange_rate = await self.service.find_one(exchange_from, exchange_to)

        self.assertIsNone(exchange_rate)
        self.collection.find_one.assert_awaited_once({
            'exchange_from': exchange_from,
            'exchange_to': exchange_to
        })

    @unittest_run_loop
    async def test_insert(self):
        exchange_rate = ExchangeRateModel(**{
            'exchange_from': 'BRL',
            'exchange_to': 'USD',
            'exchange_tax': 5,
        })
        self.collection.insert_one = CoroutineMock()

        await self.service.insert(exchange_rate)

        self.collection.insert_one.assert_awaited_once_with(exchange_rate.dict())

    @unittest_run_loop
    async def test_update(self):
        exchange_rate = ExchangeRateModel(**{
            'exchange_from': 'BRL',
            'exchange_to': 'USD',
            'exchange_tax': 5,
        })
        self.collection.update_one = CoroutineMock()

        await self.service.update(exchange_rate)

        self.collection.update_one.assert_awaited_once_with({
            'exchange_from': exchange_rate.exchange_from,
            'exchange_to': exchange_rate.exchange_to
        }, {
            "$set": exchange_rate.dict()
        })
