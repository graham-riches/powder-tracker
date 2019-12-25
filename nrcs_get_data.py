# -*- coding: utf-8 -*-
"""
@brief data exploration script for seeing what we can get out of the site
       data
@author: Graham Riches
@date: Sun Dec  8 12:02:22 2019
@description
"""


import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime, timedelta
from nrcs_service import NRCSService


def get_yearly_snotel_data(year, site_triplet, elements):
    """ get yearly snotel data for a year (string)
        with a specific station triplet (string)
        NOTE: this takes the calendar year given in year plus
        the preceeding winter months from year-1
    """
    # get a NRCS object
    nrcs_service = NRCSService('test.log')

    # gets data from nov 15 to may 15 for winter 'year'
    start_date = datetime(year=int(year)-1, month=11, day=1)
    end_date = datetime(year=int(year), month=5, day=15)
    raw_data = []
    for element in elements:
        request_data = {'stationTriplets': site_triplet, 'elementCd': element,
                        'ordinal': '1', 'duration': 'DAILY',
                        'getFlags': 'False',
                        'beginDate': datetime.strftime(start_date, '%Y-%m-%d'),
                        'endDate': datetime.strftime(end_date, '%Y-%m-%d'),
                        'alwaysReturnDailyFeb29': 'false'}
        datelist, data = nrcs_service.get_station_data(request_data)
        raw_data.append(data)
    df = pd.DataFrame(data=raw_data).transpose()
    df.columns = elements
    df['date'] = datelist
    df['year'] = [value.year for value in df['date']]
    df['month'] = [value.month for value in df['date']]
    df['day'] = [value.day for value in df['date']]
    return df


def get_hourly_snotel_data(start_date, end_date, station_triplet, elements):
    """
    get hourly snotel data from a site
    """
    # get a NRCS object
    nrcs_service = NRCSService('test.log')
    raw_data = []
    for element in elements:
        request_data = {'stationTriplets': station_triplet, 'elementCd': element,
                        'ordinal': '1', 'beginDate': start_date,
                        'endDate': end_date}
        timestamps, data = nrcs_service.get_station_hourly_data(request_data)
        raw_data.append(data)        
    df = pd.DataFrame(data=raw_data).transpose()
    df.columns = elements
    df['date'] = timestamps
    return df

def get_hourly_snotel_temps(start_date, end_date, station_triplet):
    """
    separate function for temperature data because it's weird
    """
    # get a NRCS object
    nrcs_service = NRCSService('test.log')
    request_data = {'stationTriplets': station_triplet, 'elementCd': 'TOBS',
                    'ordinal': '1', 'beginDate': start_date,
                    'endDate': end_date}
    timestamps, data = nrcs_service.get_station_hourly_data(request_data)
    df = pd.DataFrame(data=data).transpose()
    df.columns = ['TOBS']
    df['date'] = timestamps
    df.drop_duplicates('date', keep='first', inplace=True)
    df = df.sort_values(by='date', ascending=True)
    return df


if __name__ == '__main__':
    site = '787:MT:SNTL'
    year = '2019'
    years = list(range(2005, 2019))
    data = []
    for idx, year in enumerate(years):
        elements = ['SNWD', 'WTEQ']
        df = get_yearly_snotel_data(year, site, elements)
        # drop leap year
        try:
            leap = df.loc[(df['month'] == 2) & (df['day'] == 29)]
            df.drop(leap.index)
        except:
            print('could not drop leap year')
        df['date'] = pd.to_datetime(df['date'])
        data.append(go.Scatter(x=df.index, y=df['SNWD'],
                               mode='lines', name=year, hovertext=df['date']))
        df.to_csv(path_or_buf='data/snow_data_{}.csv'.format(year))
    layout = go.Layout(title='Stahl Peak Yearly Snow Depth'.format(year),
                       xaxis=dict(title='Season Date Index'),
                       yaxis=dict(title='Snow Depth (in)'),
                       hovermode='closest')
    figure = go.Figure(data=data, layout=layout)
    pyo.plot(figure, filename='Stahl_yearly_depth.html')
    
    # try hourly data
    elements = ['SNWD', 'WTEQ']
    hourly = get_hourly_snotel_data('2019-12-19', '2019-12-21', '787:MT:SNTL',
                                    elements)
    data = [go.Scatter(x=hourly['date'], y=hourly['SNWD'], mode='lines')]
    layout = go.Layout(title='Hourly Snotel Data',
                       xaxis={'title': 'Time'},
                       yaxis={'title': 'Snow Depth (in)'})
    figure = go.Figure(data=data, layout=layout)
    pyo.plot(figure, filename='Stahl_hourly.html')
    
    temperature = get_hourly_snotel_temps('2019-12-19', '2019-12-21',
                                          '787:MT:SNTL')
    data = [go.Scatter(x=temperature['date'], y=temperature['TOBS'], mode='lines')]
    layout = go.Layout(title='Hourly Snotel Temperature',
                       xaxis={'title': 'Time'},
                       yaxis={'title': 'Temperature (F)'})
    figure = go.Figure(data=data, layout=layout)
    pyo.plot(figure, filename='Stahl_hourly_temp.html')
    
