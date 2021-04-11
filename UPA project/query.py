import numpy as np
import matplotlib.pyplot as plt
import os

# python3 -m pip install influxdb
from influxdb import InfluxDBClient

import matplotlib.dates as mdates
from datetime import datetime

# NUTS
nuts_Prague = 'CZ010'
nuts_Stredocesky = 'CZ020'
nuts_Jihocesky = 'CZ031'
nuts_Plzensky = 'CZ032'
nuts_Karlovarsky = 'CZ041'
nuts_Ustecky = 'CZ042'
nuts_Liberecky = 'CZ051'
nuts_Kralovehradecky = 'CZ052'
nuts_Pardubicky = 'CZ053'
nuts_Vysocina = 'CZ063'
nuts_Jihomoravsky = 'CZ064'
nuts_Olomoucky = 'CZ071'
nuts_Zlinsky = 'CZ072'
nuts_Moravskoslezsky = 'CZ080'


def plot_graph(dates, values, label, graphKind):
    days = mdates.DayLocator()  # every day
    months = mdates.MonthLocator()  # every month
    dates_fmt = mdates.DateFormatter('%d-%m-%Y')

    fig, ax = plt.subplots()
    if graphKind == 'line':
        ax.plot(dates, values)
    elif graphKind == 'bar':
        ax.bar(dates, values)

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(dates_fmt)
    ax.xaxis.set_minor_locator(days)

    datemin = np.datetime64(dates[0], 'D')
    datemax = np.datetime64(dates[-1], 'D') + np.timedelta64(1, 'D')
    ax.set_xlim(datemin.astype('float'), datemax.astype('float'))

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)

    fig.autofmt_xdate()

    fig.set_size_inches(8, 6)

    # query number 1
    if label == 'abs':
        ax.set(title='Absolútny prírastok nakazených')
        plt.xlabel('Dátum')
        plt.ylabel('Absolútny prírastok nakazených')
        plt.savefig('graphs/absolutny_prirastok.svg')
    elif label == 'per':
        ax.set(title='Percentuálny prírastok nakazených')
        plt.xlabel('Dátum')
        plt.ylabel('Percentuálny prírastok nakazených')
        plt.savefig('graphs/percentualny_prirastok.svg')
    elif label == 'klz7':
        ax.set(title='Kĺzavý priemer nakazených - dĺžka 7')
        plt.xlabel('Dátum')
        plt.ylabel('Kĺzavý priemer')
        plt.savefig('graphs/klzavy_priemer_7.svg')
    elif label == 'klz30':
        ax.set(title='Kĺzavý priemer nakazených - dĺžka 30')
        plt.xlabel('Dátum')
        plt.ylabel('Kĺzavý priemer')
        plt.savefig('graphs/klzavy_priemer_30.svg')
    elif label == 'klz3':
        ax.set(title='Kĺzavý priemer nakazených - dĺžka 3')
        plt.xlabel('Dátum')
        plt.ylabel('Kĺzavý priemer')
        plt.savefig('graphs/klzavy_priemer_3.svg')

    # query number 2
    elif label == 'umrtnost_covid':
        ax.set(title='Percentuálna úmrtnosť na Covid-19 z nakazených')
        plt.xlabel('Dátum')
        plt.ylabel('Percento úmrtí z nakazených')
        plt.savefig('graphs/umrtnost_covid.svg')
    elif label == 'percento_smrti_covid_z_celku':
        ax.set(title='Percentuálna úmrtnosť na Covid-19 z celkových úmrtí')
        plt.xlabel('Dátum')
        plt.ylabel('Percento úmrtí na Covid-19')
        plt.savefig('graphs/umrtnost_covid_total.svg')

    # query number 3
    elif label == 'prague':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Hlavní Město Praha')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_praha.svg')
    elif label == 'stredocesky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Středočeský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_stredocesky.svg')
    elif label == 'jihocesky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Jihočeský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_jihocesky.svg')
    elif label == 'plzensky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Plzeňský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_plzensky.svg')
    elif label == 'karlovarsky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Karlovarský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_karlovarsky.svg')
    elif label == 'ustecky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Ústecký kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_ustecky.svg')
    elif label == 'liberecky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Liberecký kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_liberecky.svg')
    elif label == 'kralovehradecky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Královéhradecký kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_kralovehradecky.svg')
    elif label == 'pardubicky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Pardubický kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_pardubicky.svg')
    elif label == 'vysocina':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - kraj Vysočina')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_vysocina.svg')
    elif label == 'jihomoravsky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Jihomoravský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_jihomoravsky.svg')
    elif label == 'olomoucky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Olomoucký kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_olomoucky.svg')
    elif label == 'zlinsky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Zlínsky kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_zlinsky.svg')
    elif label == 'moravskoslezsky':
        plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
        ax.set(title='Vývoj nákazy - Moravskoslezský kraj')
        plt.xlabel('Dátum')
        plt.ylabel('Počet aktuálne nakazených')
        plt.savefig('graphs/vyvoj_moravskoslezsky.svg')

    # plt.show()
    plt.close()


def main():
    # connect
    client = InfluxDBClient(host='localhost', port=8086)

    # select db
    client.switch_database('covid_19_db')

    # if the directory graphs used for saving graphs doesn't exist create it
    if not os.path.exists('graphs'):
        os.makedirs('graphs')

    # ----------------------------------------- query number 1 -----------------------------------------------

    graphKind = 'line'

    # query - absolute count of infected
    results = client.query('select difference("count") from "cumulative" where "status"=\'infected\'')

    dates = []
    values = []

    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['difference'])

    plot_graph(dates, values, 'abs', graphKind)

    # --------------------------------------------------------------------------------------------------------

    # query - percentage increase
    i = 1
    percentList = []
    numOfDays = len(dates)
    while i < numOfDays:
        # cuts the beginning where there are zero increments
        if values[i-1] == 0:
            i += 1
            pass
        else:
            percent = ((values[i] / values[i-1]) - 1) * 100
            percentList.append(percent)
            i += 1

    numOfNonZeroDays = len(percentList)
    x = numOfDays - numOfNonZeroDays
    dates = dates[x::]

    plot_graph(dates, percentList, 'per', graphKind)

    # --------------------------------------------------------------------------------------------------------

    # query - moving average - length 7
    results = client.query('select moving_average("difference",7) from'
                           ' (SELECT difference("count") FROM "cumulative"  where "status"=\'infected\')')

    dates = []
    values = []

    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['moving_average'])

    plot_graph(dates, values, 'klz7', graphKind)

    # --------------------------------------------------------------------------------------------------------

    # query - moving average - length 30
    results = client.query('select moving_average("difference",30) from'
                           ' (SELECT difference("count") FROM "cumulative"  where "status"=\'infected\')')

    dates = []
    values = []

    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['moving_average'])

    plot_graph(dates, values, 'klz30', graphKind)

    # --------------------------------------------------------------------------------------------------------

    # query - moving average - length 3
    results = client.query('select moving_average("difference",3) from'
                           ' (SELECT difference("count") FROM "cumulative"  where "status"=\'infected\')')

    dates = []
    values = []

    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['moving_average'])

    plot_graph(dates, values, 'klz3', graphKind)

    # ----------------------------------------- query number 3 -----------------------------------------------

    graphKind = 'bar'

    # query - count of infected per region

    dates = []
    values = []
    values1 = []
    values2 = []
    values3 = []
    values4 = []
    values5 = []
    values6 = []
    values7 = []
    values8 = []
    values9 = []
    values10 = []
    values11 = []
    values12 = []
    values13 = []

    results = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Prague + '\'')
    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['cnt'])

    plot_graph(dates, values, 'prague', graphKind)

    results1 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Stredocesky + '\'')
    for point in results1.get_points():
        values1.append(point['cnt'])

    plot_graph(dates, values1, 'stredocesky', graphKind)

    results2 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Jihocesky + '\'')
    for point in results2.get_points():
        values2.append(point['cnt'])

    plot_graph(dates, values2, 'jihocesky', graphKind)

    results3 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Plzensky + '\'')
    for point in results3.get_points():
        values3.append(point['cnt'])

    plot_graph(dates, values3, 'plzensky', graphKind)

    results4 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Karlovarsky + '\'')
    for point in results4.get_points():
        values4.append(point['cnt'])

    plot_graph(dates, values4, 'karlovarsky', graphKind)

    results5 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Ustecky + '\'')
    for point in results5.get_points():
        values5.append(point['cnt'])

    plot_graph(dates, values5, 'ustecky', graphKind)

    results6 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Liberecky + '\'')
    for point in results6.get_points():
        values6.append(point['cnt'])

    plot_graph(dates, values6, 'liberecky', graphKind)

    results7 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Kralovehradecky + '\'')
    for point in results7.get_points():
        values7.append(point['cnt'])

    plot_graph(dates, values7, 'kralovehradecky', graphKind)

    results8 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Pardubicky + '\'')
    for point in results8.get_points():
        values8.append(point['cnt'])

    plot_graph(dates, values8, 'pardubicky', graphKind)

    results9 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Vysocina + '\'')
    for point in results9.get_points():
        values9.append(point['cnt'])

    plot_graph(dates, values9, 'vysocina', graphKind)

    results10 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Jihomoravsky + '\'')
    for point in results10.get_points():
        values10.append(point['cnt'])

    plot_graph(dates, values10, 'jihomoravsky', graphKind)

    results11 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Olomoucky + '\'')
    for point in results11.get_points():
        values11.append(point['cnt'])

    plot_graph(dates, values11, 'olomoucky', graphKind)

    results12 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Zlinsky + '\'')
    for point in results12.get_points():
        values12.append(point['cnt'])

    plot_graph(dates, values12, 'zlinsky', graphKind)

    results13 = client.query(
        'select infected-recovered-deceased as "cnt" from "regional" where "nuts"=\'' + nuts_Moravskoslezsky + '\'')
    for point in results13.get_points():
        values13.append(point['cnt'])

    plot_graph(dates, values13, 'moravskoslezsky', graphKind)

    # line graph for all regions together ------------------------------------------
    days = mdates.DayLocator()  # every day
    months = mdates.MonthLocator()  # every month
    dates_fmt = mdates.DateFormatter('%d-%m-%Y')

    fig, ax = plt.subplots()
    ax.plot(dates, values, label='Praha')
    ax.plot(dates, values1, label='Středočeský')
    ax.plot(dates, values2, label='Jihočeský')
    ax.plot(dates, values3, label='Plzeňský')
    ax.plot(dates, values4, label='Karlovarský')
    ax.plot(dates, values5, label='Ústecký')
    ax.plot(dates, values6, label='Liberecký')
    ax.plot(dates, values7, label='Královéhradecký')
    ax.plot(dates, values8, label='Pardubický')
    ax.plot(dates, values9, label='Vysočina')
    ax.plot(dates, values10, label='Jihomoravský')
    ax.plot(dates, values11, label='Olomoucký')
    ax.plot(dates, values12, label='Zlínsky')
    ax.plot(dates, values13, label='Moravskoslezský')

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(dates_fmt)
    ax.xaxis.set_minor_locator(days)

    datemin = np.datetime64(dates[0], 'D')
    datemax = np.datetime64(dates[-1], 'D') + np.timedelta64(1, 'D')
    ax.set_xlim(datemin.astype('float'), datemax.astype('float'))

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)

    fig.autofmt_xdate()

    ax.set(title='Vývoj epidémie podla regiónov')
    plt.xlabel('Dátum')
    plt.ylabel('Počet aktuálne nakazených')

    fig.set_size_inches(8, 6)
    plt.legend()

    # plt.show()

    plt.savefig('graphs/vyvoj_podla_regionov.svg')
    plt.close()

    # ----------------------------------------- query number 2 -----------------------------------------------

    graphKind = 'bar'

    # yearly deaths
    values = []
    values1 = []
    values2 = []
    values3 = []
    values4 = []

    results = client.query('select count as "cnt" from "total_deaths" where time >='
                           '\'2016-01-01T00:00:00Z\' and time <\'2017-01-01T00:00:00Z\'')

    for point in results.get_points():
        values.append(point['cnt'])

    results = client.query('select count as "cnt" from "total_deaths" where time >='
                           '\'2017-01-01T00:00:00Z\' and time <\'2018-01-01T00:00:00Z\'')
    for point in results.get_points():
        values1.append(point['cnt'])

    results = client.query('select count as "cnt" from "total_deaths" where time >='
                           '\'2018-01-01T00:00:00Z\' and time <\'2019-01-01T00:00:00Z\'')
    for point in results.get_points():
        values2.append(point['cnt'])

    results = client.query('select count as "cnt" from "total_deaths" where time >='
                           '\'2019-01-01T00:00:00Z\' and time <\'2020-01-01T00:00:00Z\'')
    for point in results.get_points():
        values3.append(point['cnt'])

    results = client.query('select count as "cnt" from "total_deaths" where time >='
                           '\'2020-01-01T00:00:00Z\' and time <\'2021-01-01T00:00:00Z\'')
    for point in results.get_points():
        values4.append(point['cnt'])

    fig, ax = plt.subplots()

    ax.plot(range(1, 51), values[0:50], label='2016')
    ax.plot(range(1, 51), values1[0:50], label='2017')
    ax.plot(range(1, 51), values2[0:50], label='2018')
    ax.plot(range(1, 51), values3[0:50], label='2019')
    ax.plot(range(1, 44), values4[0:43], label='2020')

    fig.set_size_inches(8, 6)
    plt.xticks(range(1, 51, 4))
    ax.set(title='Porovnanie ročných úmrtí')
    plt.xlabel('Týždeň')
    plt.ylabel('Počet úmrtí')
    plt.legend()

    # plt.show()
    plt.savefig('graphs/umrtia_rocne.svg')
    plt.close()

    # percent of death from the infected
    dates = []
    values = []
    dates1 = []
    values1 = []

    dates2 = []
    values2 = []

    results = client.query('select count as "cnt" from "cumulative" where status=\'infected\'')
    results2 = client.query('select count as "cnt" from "cumulative" where status=\'deceased\'')

    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['cnt'])
    for point in results2.get_points():
        dates1.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values1.append(point['cnt'])

    for i in range(0, 299):
        if dates[i] == dates1[i] and values[i] != 0:
            dates2.append(dates[i])
            values2.append((values1[i] / values[i]) * 100)

    plot_graph(dates2, values2, "umrtnost_covid", graphKind)

    # percentage of deaths caused by covid-19 from total deaths
    dates = []
    values = []

    results = client.query('select count as "cnt" from "total_deaths" where time>=\'2020-01-01T00:00:00Z\' '
                           'and time <\'2021-01-01T00:00:00Z\'')


    for point in results.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        values.append(point['cnt'])

    values2 = [0]
    i = 0
    for point in dates:
        if i != 0:
            results = client.query(
                'select sum(difference) as "cnt" from (select difference("count") from "cumulative" '
                'where status=\'deceased\' and time>\''+ str(dates[i-1]) +'\' and time <=\''+ str(dates[i]) +'\')')
            val = 0
            for point in results.get_points():
                values2.append(point['cnt'])
                val = 1
            if val == 0:
                values2.append(0)
        i = i + 1

    i = 0
    values3 = []
    for point in values2:
        values3.append((values2[i] / values[i]) * 100)
        i = i + 1

    plot_graph(dates, values3, 'percento_smrti_covid_z_celku', 'line')


if __name__ == "__main__":
    main()
