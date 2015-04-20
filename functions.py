__author__ = "Roman Gorilyi"
__version__ = "1.0.0"
__maintainer__ = "Roman Gorilyi"
__email__ = "rom4ik-007@yandex.ua"

import pandas as pd
import urllib2
import os
import glob
from time import gmtime, strftime


def download(index, region):
    url = "http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R%s.txt" % index
    vhi_url = urllib2.urlopen(url)
    time = strftime("%Y-%m-%d.%H-%M-%S", gmtime())
    out = open('Downloads/%s.csv' % (index + ' ' + region + ' ' + time), 'wb')
    out.write(vhi_url.read())
    out.close()
    return time


def read_in_frame(file_name):
    df = pd.read_csv( "Downloads/%s"%file_name ,index_col=False, header=1)
    return df


def max_value(file_name, year):
    df = read_in_frame(file_name)
    yr = df[df['year'] == year]
    print "A max value VHI in this region was in: %s" % year
    maximum = max(yr.VHI)
    return maximum


def min_value(file_name, year):
    df = read_in_frame(file_name)
    yr = df[df['year'] == year]
    print "A min value VHI in this region was in: %s" % year
    minimum = min(yr.VHI)
    return minimum


def drought(file_name, percent1, percent2):
    df = read_in_frame(file_name)
    period = df[(df['VHI'] > percent1) & (df['VHI'] < percent2)]
    return period


def extreme_drought(file_name):
    extr_dr = drought(file_name, 0, 15)
    print "Extreme drought was in:"
    return extr_dr


def moderate_drought(file_name):
    mod_dr = drought(file_name, 15, 35)
    print "Moderate drought was in:"
    return mod_dr


def delete():
    for files in glob.glob('Downloads/*.csv'):
        os.remove(files)


def years_drought_more_than_third_year(file_name):
    df = read_in_frame(file_name)
    print ("Years when there was a moderate drought more than third of the year (15% < VHI < 35%) "
           "in this region was in:")
    year = 1982
    while year < 2016:
        yr = df[df['year'] == year]
        test = yr[(yr['VHI'] > 15) & (yr['VHI'] < 35)]
        check = len(test.index)
        if check > 17:
            print (year)
        year += 1