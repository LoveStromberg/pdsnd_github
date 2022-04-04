import calendar
import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ''

    for i in CITY_DATA.keys():
        cities = cities + ', ' + i

    available_cities = cities[2:].title()

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = input(
        'Select one of these available cities (' + available_cities + '): ').lower()

    # only accept a valid city as input
    while city not in CITY_DATA:
        city = input(
            'You can only select one of these available cities (' + available_cities + '): ').lower()

    # get unique months and weekdays in the selected file
    city_file_name = CITY_DATA[city]
    city_df = pd.read_csv(city_file_name)
    city_df['Month'] = pd.DatetimeIndex(city_df['Start Time']).month
    city_df['Weekday'] = pd.DatetimeIndex(city_df['Start Time']).weekday
    available_months = city_df['Month'].unique()
    available_months.sort()
    available_months = np.array2string(available_months)
    available_wd = city_df['Weekday'].unique()
    available_wd.sort()
    available_wd = np.array2string(available_wd)

    # get user input for month (all, january, february, ... , june)
    month = input('Select one of these months ' +
                  available_months + ', or \'All\' for no filter: ').lower()

    # only accept a valid month as input
    while month not in available_months and month != 'all':
        month = input(
            'You can only select one of these available months ' + available_months + ', or \'All\': ').lower()

    # get month name
    if month != 'all':
        month_name_selection = calendar.month_name[int(month)]
    else:
        month_name_selection = 'All'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Select one of these weekdays ' + available_wd +
                ', or \'All\' for no filter: ').lower()

    # only accept a valid month as input
    while day not in available_wd and day != 'all':
        day = input(
            'You can only select one of these available weekdays ' + available_wd + ', or \'All\': ').lower()

    # get name of weekday
    if day != 'all':
        day_name_selection = calendar.day_name[int(day)]
    else:
        day_name_selection = 'All'

    print('-'*80)
    return city, month, day, city_file_name, month_name_selection, day_name_selection


def load_data(month, day, city_file_name):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # add new fields to df for month, weekday and hour
    df_full = pd.read_csv(city_file_name)
    df_full['Month'] = pd.DatetimeIndex(df_full['Start Time']).month
    df_full['Weekday'] = pd.DatetimeIndex(df_full['Start Time']).weekday
    df_full['StartHour'] = pd.DatetimeIndex(df_full['Start Time']).hour

    # Filter df according to user selections
    if month == 'all' and day == 'all':
        df = df_full
    elif month == 'all' and day != 'all':
        df = df_full[(df_full.Weekday == int(day))]
    elif month != 'all' and day == 'all':
        df = df_full[(df_full.Month == int(month))]
    else:
        df = df_full[(df_full.Month == int(month)) &
                     (df_full.Weekday == int(day))]

    return df


def time_stats(df, city, month, day, month_name_selection, day_name_selection):
    """Displays statistics on the most frequent times of travel."""

    # print result header
    print('*'*80)
    print('Query Result\n\nFilters applied - City: ' + city.title() + ' / Month: ' +
          month_name_selection+' / Weekday: ' + day_name_selection)
    print('*'*80)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        month_count = int(df['Month'].value_counts().idxmax())
        month_name_all = calendar.month_name[month_count]
        print('The most common month to travel is: ' + month_name_all)
    else:
        month_count = len(df.index)
        print('You selected a single month (' + month_name_selection +
              ') so most common month is not calculated!')
        print('Number of trips in ' + month_name_selection +
              ' is ' + str(month_count))

    # display the most common day of week
    if day == 'all':
        day_count = int(df['Weekday'].value_counts().idxmax())
        day_name_all = calendar.day_name[day_count]
        print('\nThe most common weekday to travel is: ' + day_name_all)
    else:
        day_count = len(df.index)
        print('\nYou selected a single weekday (' + day_name_selection +
              ') so most common weekday is not calculated!')
        print('Number of trips on a ' +
              day_name_selection + ' is ' + str(day_count))

    # display the most common start hour
    hour_count = str(df['StartHour'].value_counts().idxmax())
    print('\nThe most common hour to start a trip is: ' + hour_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_count = str(
        df['Start Station'].value_counts().nlargest(1).values[0])
    station_name = str(df['Start Station'].value_counts().idxmax())
    print('The most used start station is ' +
          station_name + ' with ' + station_count + ' trips starting here.')

    # display most commonly used end station
    station_count = str(
        df['End Station'].value_counts().nlargest(1).values[0])
    station_name = str(df['End Station'].value_counts().idxmax())
    print('The most used end station is ' +
          station_name + ' with ' + station_count + ' trips ending here.')

    # display most frequent combination of start station and end station trip
    station_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    start_station, end_station = station_combination
    print('The most common combination of Start and End station is: ' +
          start_station + ' to ' + end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = int(df['Trip Duration'].sum())
    total_time_format = str(dt.timedelta(seconds=total_time_sec))
    print('Total travel time was: ' + total_time_format)

    # display mean travel time
    mean_travel_time_sec = int(df['Trip Duration'].mean())
    mean_travel_time_format = str(dt.timedelta(seconds=mean_travel_time_sec))
    print('Mean travel time was: ' + mean_travel_time_format)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nGender:')

    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('There is no gender data available for ' + city + '!')

    # Display earliest, most recent, and most common year of birth
    print('\nYear of birth:')

    if 'Birth Year' in df.columns:
        min_year = str(df['Birth Year'].min())
        max_year = str(df['Birth Year'].max())
        count_year = str(df['Birth Year'].value_counts().idxmax())
        print('Oldest user was born: ' + min_year[:4])
        print('Youngest user was born: ' + max_year[:4])
        print('Most common year of birth is: ' + count_year[:4])
    else:
        print('There is no birth year available for ' + city + '!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    view_data = input(
        '\nDo you want to scroll through the raw data? (Yes/No): \n')

    index = df.index
    rows = len(index)
    frow = 0
    lrow = 5

    while view_data.lower() == 'yes':
        if lrow <= rows:
            print('Displaying rows ' + str(frow) + '-' +
                  str(lrow) + ' of ' + str(rows) + ':')
            print(df[frow:lrow])
            view_data = input(
                '\nDo you want to see five more rows? (Yes/No): \n')
            frow += 5
            lrow += 5
        elif lrow > rows:
            print('Displaying rows ' + str(frow) + '-' +
                  str(rows) + ' of ' + str(rows) + ':')
            print(df[frow:rows])
            print('\nYou have reaced the end of the dataset!')
            break


def main():
    while True:
        city, month, day, city_file_name, month_name_selection, day_name_selection = get_filters()
        df = load_data(month, day, city_file_name)

        time_stats(df, city, month, day,
                   month_name_selection, day_name_selection)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() = 'no':
            break


if __name__ == "__main__":
    main()
