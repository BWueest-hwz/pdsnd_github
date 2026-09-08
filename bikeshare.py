import time
import pandas as pd
import numpy as np

city_dat = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    aliases = {'nyc': 'new york city', 'chi': 'chicago', 'dc': 'washington'}
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('-'*60)
    print('\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("For which city do you like to inspect the data? Please enter 'Chicago' or 'chi', 'New York City' or 'nyc', 'Washington' or 'dc': ").strip().lower()
        city = aliases.get(city, city)
        if city in city_dat:
            break
        print("\nSorry, invalid city name. Please try it again: ")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nFor which month do you like to inspect the data? Please enter 'all' for all months, 'January', 'February', 'March', 'April', 'May', or 'June': ").strip().lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        print("\nSorry, invalid month name. Please try it again: ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nFor which day of the week do you like to inspect the data? Please enter 'all' for all days, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', or 'Sunday': ").strip().lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        print("\nSorry, invalid day name. Please try it again: ")

    print('-'*80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city_dat[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def raw_data(df):
    """Shows 5 rows of raw data at a time while the user asks for more."""
    
    start = 0
    while start < len(df):
        answer = input("\nWould you like to see 5 lines of the data set? Please enter 'yes' or 'no': ").strip().lower()
        if answer != 'yes':
            break
        print(df.iloc[start:start + 5])
        start += 5
    
    if start >= len(df):
        print('\nNo more data to display.')
    
    print('-'*80)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nTimes of travel\n')
    start_time = time.time()
    
    # convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    popular_month = df['Start Time'].dt.month.mode()[0]
    print("  Most common month: ", popular_month)
    
    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    popular_day = days[df['Start Time'].dt.dayofweek.mode()[0]]
    print("  Most common day of week: ", popular_day)
    
    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print("  Most common start hour: ", popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nPopular stations\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("  Most common start station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("  Most common end station: ", popular_end_station)
    
    # display most frequent combination of start station and end station trip
    trips = df['Start Station'] + " -> " + df['End Station']
    popular_trip = trips.mode()[0]
    print("  Most frequent trip: ", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip duration stats\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"  Total travel time in minutes: {total_travel_time / 60:>7,.2f}")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"  Average travel time in minutes: {mean_travel_time / 60:>7,.2f}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nUser stats\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    counts = df['User Type'].value_counts()
    width = max(len(str(i)) for i in counts.index)
    for user_type, count in counts.items():
        print(f"  {user_type:<{width}}:  {count:>7,}")

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of gender:\n")
        counts = df['Gender'].value_counts()
        width = max(len(str(i)) for i in counts.index)
        for gender, count in counts.items():
            print(f"  {gender:<{width}}:  {count:>7,}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBirth year stats:\n")
        print(f"  Earliest year of birth: {int(df['Birth Year'].min()):>7,}")
        print(f"  Most recent year of birth: {int(df['Birth Year'].max()):>7,}")
        print(f"  Most common year of birth: {int(df['Birth Year'].mode()[0]):>7,}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
