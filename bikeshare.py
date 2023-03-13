import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    All the inputs are case insensitive.
    
	Only the following cites are accepted:
        - Chicago
        - New York City
        - Washington

	For month filter the following values are accepted:
        - All
        - January
        - February
        - March
        - April
        - May
        - June

	For day filter the following values are accepted:
        - All
        - Monday
        - Tuesday
        - Wednesday
        - Thursday
        - Friday
        - Saturday
        - Sunday

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to indicate that no filter will be applied
        (str) day - name of the day of week to filter by, or "all" to indicate that no filter will be applied
        All return values are in lowercase
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    month = ''
    day = ''
    input_ok = False

    while not input_ok:
        city = input('Please enter the city you want to explore from the following cities: Chicago, New York City, Washington\n')
        input_ok = city.lower() in CITY_DATA.keys()
        if not input_ok:
            print('Please check input : {}'.format(city))
        else:
            print('Exploring city {}'.format(city.title()))

    # Resetting input_ok to False
    input_ok = False
    while not input_ok:
        month = input('Please enter the month you want to filter (all, january, february, ... , june).\nEnter all for no filter, enter month to apply filter for that specific month\n')
        input_ok = month.lower() in ('all','january','february','march','april','may','june')
        if not input_ok:
            print('Please check input : {}\n'.format(month))
        elif month.lower() != 'all':
            print('The filter will be applied for month {}\n'.format(month.title()))
        else:
            print('No filter will be applied for month\n')

    # Resetting input_ok to False
    input_ok = False
    while not input_ok:
        day = input('Please enter the day of the week you want to filter (all, monday, tuesday, ... sunday).\nEnter all for no filter, enter day to apply filter for that specific day\n')
        input_ok = day.lower() in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
        if not input_ok:
            print('Please check input: {}\n'.format(day))
        elif day.lower() != 'all':
            print('The filter will be applied day {}\n'.format(day.title()))
        else:
            print('No filter will applied for day\n')
            
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze in lower case
        (str) month - name of the month to filter by in lower case, or "all" to apply no month filter
        (str) day - name of the day of week to filter by in lower case, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    print('Loaded data shape :',df.shape)

    if month != 'all':
        print('Applying filter for month {} \n'.format(month.title()))
        # since df['month'] is an integer starting from 1, the index is checked from months and incremented by 1
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        print('Applying filter for day {} \n'.format(day.title()))
        df = df[(df['day_of_week'] == day.title())]
    
    print('\nFiltered data shape :',df.shape)
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (Pandas DataFrame) df - Pandas DataFrame containing city data to calculate time statistics
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # since df['month'] is an integer starting from 1, the month is converted to string from months
    months = ['january','february','march','april','may','june']
    print('The mostly used month is {}\n'.format(months[df['month'].mode()[0] - 1].title()))

    print('The mostly used day is {}\n'.format(df['day_of_week'].mode()[0]))

    print('The mostly used hour is {}\n'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (Pandas DataFrame) df - Pandas DataFrame containing city data to calculate station and trip statistics
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    trip_count = df[df['Start Station'] == start_station]['Start Station'].count()
    print('The most used station to start a trip is {} with {} trips.\n'.format(start_station,trip_count))

    end_station = df['End Station'].mode()[0]
    trip_count = df[df['End Station'] == end_station]['End Station'].count()
    print('The most used station to end a trip is {} with {} trips\n'.format(end_station,trip_count))

    # Concatenating start station and end station to find the most used pair
    df['Station Pair'] = df['Start Station'] + '_' + df['End Station']
    station_pair = df['Station Pair'].mode()[0]
    start_station, end_station = station_pair.split('_')
    trip_count = df[df['Station Pair'] == station_pair]['Station Pair'].count()

    print('The most common trip is from {} to {} with {} trips.\n'.format(start_station,end_station,trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (Pandas DataFrame) df - Pandas DataFrame containing city data to calculate trip duration statistics
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('The total travel time is {} seconds.\n'.format(df['Trip Duration'].sum()))

    print('The mean travel time is {} seconds.\n'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """
    Displays statistics on bikeshare users. If the city is washington skipping gender and age statistics
    
    Args:
        (Pandas DataFrame) df - Pandas DataFrame containing city data to calculate user statistics
        (str) city - The name of the city in lower case that the statistics is displayed 
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User Type statistics : \n')
    print(df['User Type'].value_counts())

    if city != 'washington' :
        print('\nGender  statistics : \n')
        print(df['Gender'].value_counts())

        print('The oldest person who took a trip was born in {} \n'.format(int(df['Birth Year'].min())))
        print('The youngest person who took a trip was born in {} \n'.format(int(df['Birth Year'].max())))
        print('Most of the people who took a trip was born in {} \n'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('\nSkipping gender and age statistics for Washington, because Washington does not have any related data.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        view_data = input('\nWould you like to view {} rows of individual trip data? Enter yes or no\n'.format(5)).lower()
        start_loc = 0
        while (view_data == 'yes' and start_loc < df.shape[0]):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if(start_loc >= df.shape[0]) :
                print('Reached the end of all data.')
                break
            else :
                view_data = input("Do you wish to continue?: Enter yes to continue.\n").lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
