# -*- coding: utf-8 -*-
"""
@brief class for interfacing with the NRCS web service for gathering
       general station data. External classes handle getting the data required
       for an application.
@author: Graham Riches
@date: Sun Dec  8 09:09:36 2019
@description
    Queries the NRCS SOAP API and pulls station data (i.e. snotel info, etc.).
    Functions handle all the required info IO into the service for easy queries

    NOTE: not all methods are implemented yet!!! Currently only basic snotel
          functionality exists
"""

from zeep import Client
from zeep.transports import Transport
from requests import Session
from datetime import datetime, timedelta
import time
import urllib3
import logging

from nrcs_logging_utilities import attach_logger, AppLogger

# disable the annoying messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NRCSService:
    """ class to interface with NRCS station data """
    def __init__(self, _logfile):
        """ initialize an object of the NRCS service handler with a logfile"""
        self._url = 'https://wcc.sc.egov.usda.gov/awdbWebService/services?WSDL'
        self._logfile = _logfile
        self._logger = None
        self.create_logger()
        self.connect_service()

    def connect_service(self):
        """ set up the connection session (no auth) """
        try:
            _session = Session()
            _session.verify = False
            _transport = Transport(session=_session)
            self._client = Client(self._url, transport=_transport)
            self._logger.info('Connected to NRCS SOAP Service')
        except Exception as caught_exception:
            logging.exception(caught_exception)

    def create_logger(self):
        self._logger = attach_logger(self._logfile, 'NRCS_Query     ',
                                     logging.INFO)

    def get_methods_dict(self):
        """ get a dict of the available SOAP methods """
        try:
            ops = self._client.service._operations
            return ops
        except Exception as caught_exception:
            logging.exception(caught_exception)
            return None

    def get_stations(self, request_data):
        """
        get NRCS stations satisfying search criteria
            request_data --> dict of search parameters,
                             must satisfy the required args in the NRCS API
                             (See the NRCS API docs)
            returns a list of station dicts with metadata
        WARNING: Could be a massive query if not enough filter ops are added
        """
        try:
            stations = self._client.service.getStations(**request_data)
            station_metadata_list = []
            self._logger.info('getting station metadata ...')
            for station in stations:
                request_data = {'stationTriplet': station}
                metadata = self._client.service.getStationMetadata(**request_data)
                station_metadata_list.append(metadata)
            return station_metadata_list
        except Exception as caught_exception:
            logging.exception(caught_exception)

    def get_station_metadata(self, station_triplet):
        """
        Get metadata given a station triplet
        """
        try:
            self._logger.info('querying station metadata for {}'.format(station_triplet))
            request_data = {'stationTriplet': station_triplet}
            meta = self._client.service.getStationMetadata(**request_data)
            return meta
        except Exception as caught_exception:
            logging.exception(caught_exception)

    def get_station_data(self, request_data):
        """
        getData query to get specific data from a site
            request_data --> dict of search params must meet reqs in getData
                             from the NRCS API doc.
            returns --> list of dates, and list of float values
        """
        try:
            self._logger.info('querying station data for {}'.format(request_data['stationTriplets']))
            station_data = self._client.service.getData(**request_data)
            start_date = datetime.strptime(station_data[0]['beginDate'], '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(station_data[0]['endDate'], '%Y-%m-%d %H:%M:%S')
            date_delta = end_date - start_date
            date_list = []
            for i in range(date_delta.days + 1):
                date_list.append(start_date + timedelta(days=i))
            data = station_data[0]['values']
            requested_data = []
            for value in data:
                if value is None:
                    requested_data.append(None)
                else:
                    requested_data.append(float(value))
            return date_list, requested_data
        except Exception as caught_exception:
            logging.exception(caught_exception)

    def get_station_hourly_data(self, request_data):
        """
        getHourlyData query to get station hourly results
            request_data --> dict of search params must meet reqs in
                             getHourlyData from NRCS API doc.
            returns --> list of datetime timestamps, and list of float values
        """
        try:
            self._logger.info('querying hourly station data for {}'.format(request_data['stationTriplets']))
            station_data = self._client.service.getHourlyData(**request_data)
            data = station_data[0]['values']
            timestamps = []
            requested_data = []
            for item in data:
                if item['dateTime'] is None:
                    timestamps.append(None)
                else:
                    timestamps.append(datetime.strptime(item['dateTime'], '%Y-%m-%d %H:%M'))
                if item['value'] is None:
                    requested_data.append(None)
                else:
                    requested_data.append(float(item['value']))
            return timestamps, requested_data
        except Exception as caught_exception:
            logging.exception(caught_exception)


if __name__ == '__main__':
    logpath = 'test.log'
    app_logger = AppLogger(logpath)
    service = NRCSService(logpath)
    request_data = {'stateCds': 'MT', 'networkCds': 'SNTL',
                    'minElevation': '6000', 'countyNames': 'Lincoln',
                    'logicalAnd': 'true'}
    stations = service.get_stations(request_data)
    meta = service.get_station_metadata('787:MT:SNTL')
    
