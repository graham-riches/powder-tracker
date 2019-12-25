# -*- coding: utf-8 -*-
"""
@brief unit tests for the NRCS service class/api
@author: Graham Riches
@date: Sun Dec  8 09:15:14 2019
@description
"""

import unittest
import logging
from datetime import datetime
from nrcs_service import NRCSService


class NRCSTests(unittest.TestCase):
    def setUp(self):
        """ setup method """
        self._service = NRCSService('test.log')

    def test_get_station_query(self):
        pass

    def test_init_logger(self):
        self.assertIsInstance(self._service._logger, logging.Logger)

    def test_get_api_methods(self):
        """ returns a dict """
        ops = self._service.get_methods_dict()
        self.assertIsInstance(ops, dict)

    def test_get_stations(self):
        """ should return a list of stations """
        request_data = {'stateCds': 'MT', 'networkCds': 'SNTL',
                        'minElevation': '4500', 'countyNames': 'Lincoln',
                        'logicalAnd': 'true'}
        stations = self._service.get_stations(request_data)
        self.assertIsInstance(stations, list)

    def test_get_station_metadata(self):
        """ should return a dict """
        meta = self._service.get_station_metadata('787:MT:SNTL')
        self.assertIsInstance(meta['name'], str)
    
    def test_get_station_data(self):
        request_data = {'stationTriplets': '787:MT:SNTL', 'elementCd': 'SNWD',
                        'ordinal': '1', 'duration': 'DAILY',
                        'getFlags': 'False', 'beginDate': '2019-12-01',
                        'endDate': '2019-12-08',
                        'alwaysReturnDailyFeb29': 'true'}
        dates, station_data = self._service.get_station_data(request_data)
        self.assertIsInstance(dates, list)
        self.assertIsInstance(station_data, list)
        self.assertIsInstance(station_data[0], float)

    def test_get_station_hourly_data(self):
        request_data = {'stationTriplets': '787:MT:SNTL', 'elementCd': 'SNWD',
                        'ordinal': '1', 'beginDate': '2019-12-06',
                        'endDate': '2019-12-08'}
        timestamps, station_data = self._service.get_station_hourly_data(request_data)
        self.assertIsInstance(timestamps, list)
        self.assertIsInstance(station_data, list)
        self.assertIsInstance(station_data[0], float)

if __name__ == '__main__':
    unittest.main()
