import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITY_LIST = ['chicago','new york city','washington','all']
MONTH_LIST = ['january','february','march','april','may','june','all']
DAY_LIST = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def timedelta_to_str(td):
    """
    Returns Days,Hours,Minutes and Seconds for a given Timedelta input.

    Args:
        (timedelta) td - input timedelta datatype for conversion
    Returns:
        (int)td_days  - Number of days for the input timedelta
        (int)td_hours - Number of hours post days for the input timedelta
        (int)td_mins  - Number of minutes post day and hour for the input timedelta
        (int)td_sec   - Number of seconds post day,hour and minutes for the input timedelta
    """ 
    td_days = td.days
    td_hours = int(math.floor(td.seconds/60/60))
    td_mins = int(math.floor(td.seconds/60) - math.floor(td.seconds/60/60)*60)
    td_sec = int(round(td.seconds%60,0))
    return td_days,td_hours,td_mins,td_sec

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Select a city to explore.Please enter a number corresponding to the option you want to select.\n1 - Chicago\n2 - New York City\n3 - Washington\n4 - All 3 Cities\n9 - Exit program\n')
        try:
            #Check if the input values are between 1 and 4 and assign one of the values in city_list to city.
            if int(city) in range(1,5):
                city = CITY_LIST[int(city) -1]
                break
            #If the user selects 9 - Exit the program
            elif int(city) == 9:
                return None,None,None
            else:
                print('You Entered - {} .Please enter a valid input'.format(day))
        #If there was any problem assigning city - repeat the input process again
        except Exception as ex:
            print('You Entered - {} .Please enter a valid input'.format(city if city else 'Nothing'))

    # TO DO: get user input for month (all, january, february, ... , june)
    print('-'*85)
    while True:
        month = input('Select a Month.Please enter a number corresponding to the option you want to select.\n1 - January\n2 - Februrary\n3 - March\n4 - April\n5 - May\n6 - June\n7 - All 6 months\n9 - Exit program\n')
        try:
            #Check if the input values are between 1 and 7.
            if int(month) in range(1,8):
                month = MONTH_LIST[int(month) -1]
                break
            #If the user selects 9 - Exit the program
            elif int(month) == 9:
                return None,None,None
            else:
                print('You Entered - {} .Please enter a valid input'.format(month))
        #If there was any problem assigning month - repeat the input process again
        except Exception as ex:
            print('You Entered - {} .Please enter a valid input'.format(month if month else 'Nothing'))
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'monday'
    print('-'*85)
    while True:
        day = input('Select a Day.Please enter a number corresponding to the option you want to select.\n1 - Monday\n2 - Tuesday\n3 - Wednesday\n4 - Thursday\n5 - Friday\n6 - Saturday\n7 - Sunday\n8 - All 7 days\n9 - Exit program\n')
        try:
            #Check if the input values are between 1 and 8.
            if int(day) in range(1,9):
                day = DAY_LIST[int(day) - 1]
                break
            #If the user selects 9 - Exit the program
            elif int(day) == 9:
                return None,None,None
            else:
                print('You Entered - {} .Please enter a valid input'.format(day))
        #If there was any problem assigning day - repeat the input process again
        except Exception as ex:
            print('You Entered - {} .Please enter a valid input'.format(day if day else 'Nothing'))

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

    # load data file into a dataframe
    if city != 'all':   
        df = pd.read_csv(CITY_DATA[city])
    else:
        for key,val in CITY_DATA.items():
            if key == 'chicago':
                df = pd.read_csv(CITY_DATA[key])
                continue
            else:
                df_tmp = pd.read_csv(CITY_DATA[key])
                df = df.append(df_tmp)
                
    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_LIST.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    #2018-12-09 - Start - Updated code post review to Handle records where Birth Year is completely missing from Dataframe
    if 'Gender' not in df.columns:
        df['Gender'] = np.nan
    if 'Birth Year' not in df.columns:
        df['Birth Year'] = np.nan
    #2018-12-09 - End - Updated code post review to Handle records where Birth Year is completely missing from Dataframe
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['month'].value_counts().size == 1:
        print('For the Month - {},'.format(MONTH_LIST[int(df['month'].value_counts().index[0]) - 1]).title())
    else:
        print('Most Common Month      : {}'.format(MONTH_LIST[int(df['month'].mode()[0]) - 1].title()))

    # TO DO: display the most common day of week
    if df['day_of_week'].value_counts().size == 1:
        print('For Weekday   - {},'.format(df['day_of_week'].value_counts().index[0].title()))
    else:
        print('Most Common Day of Week: {}'.format(df['day_of_week'].mode()[0]))
        
    # TO DO: display the most common start hour
    print('Most Common Start Hour  : {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station : {} with {} rentals started.'.format(df['Start Station'].mode()[0],df[df['Start Station'] == df['Start Station'].mode()[0]].count()['Start Station']))

    # TO DO: display most commonly used end station
    print('Most commonly used end station   : {} with {} rentals ended.'.format(df['End Station'].mode()[0],df[df['End Station'] == df['End Station'].mode()[0]].count()['End Station']))

    # TO DO: display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station  : {} with {} trips.'.format(df.groupby(['Start Station','End Station'])['Start Time'].count().idxmax(),df.groupby(['Start Station','End Station'])['Start Time'].count().max()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    td = df['End Time'] - df['Start Time']
    
    td_days,td_hours,td_mins,td_sec = timedelta_to_str(td.sum())
    print('Total travel time for all the rentals - {} days {} hours {} mins {} seconds'.format(td_days,td_hours,td_mins,td_sec))
    # TO DO: display mean travel time
    td_days,td_hours,td_mins,td_sec = timedelta_to_str(td.mean())
    print('Mean travel time for all the rentals  - {} days {} hours {} mins {} seconds'.format(td_days,td_hours,td_mins,td_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df['User Type'] = df['User Type'].fillna('Unknown')
    usr_typ = df.groupby(['User Type'])['Start Time'].count()
    print('"User Type" wise Counts as below:')
    for key,val in usr_typ.iteritems():
        print('{} : {}({}%)'.format(key.ljust(10,' '),str(val).ljust(7,' '),round(val*100/df['User Type'].size,2)))
                    
    # TO DO: Display counts of gender
    df['Gender'] = df['Gender'].fillna('Unknown')
    gdr = df.groupby(['Gender'])['Start Time'].count()
    print('\n"Gender" wise Counts as below:')
    for key,val in gdr.iteritems():
        print('{} : {}({}%)'.format(key.ljust(10,' '),str(val).ljust(7,' '),round(val*100/df['User Type'].size,2)))

    # TO DO: Display earliest, most recent, and most common year of birth
    #2018-12-09 - Start - Updated code post review to Handle records where Birth Year is completely missing from Dataframe
    if (df['Birth Year'].size - df['Birth Year'].count() != 0) and df['Birth Year'].count() != 0:
        print('\nThere are {}({}%) records out of {} where Birth Year is missing.'.format(df['Birth Year'].size - df['Birth Year'].count(),round((df['Birth Year'].size - df['Birth Year'].count())*100/df['Birth Year'].size,2),df['Birth Year'].size)) 
        print('For the {}({}%) records where Birth Year is present - below are some "Birth Year" related metrics.\n'.format(df['Birth Year'].count(),round(df['Birth Year'].count()*100/df['Birth Year'].size,2)))
    elif df['Birth Year'].count() != 0:
        print('\n"Birth Year" related metrics:')
    else:
        print('\n"Birth Year" is always Unkown for the filtered dataset. No metrics to Display.')
    
    if df['Birth Year'].count() != 0:
        print('Oldest person\'s birth year   - {}'.format(int(df['Birth Year'].min())))
        print('Youngest person\'s birth year - {}'.format(int(df['Birth Year'].max())))
        print('Most common birth year       - {}'.format(int(df['Birth Year'].mode()[0])))
    #2018-12-09 - End - Updated code post review to Handle records where Birth Year is completely missing from Dataframe
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        if not city:
            print('Bye!')
            break
        print('*'*90)
        print('You will be exploring the data for {}, with data for {} and {}.'.format(city.title()+' cities' if city == 'all' else city.title(),month.title() + ' months' if month =='all' else month.title() + ' month',day.title() + ' days' if day == 'all' else day.title()))
        print('*'*90)
        if input('Please Press Enter to continue. Press anything else to select options again\n'):
            continue
        
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data = input('\nWould you like to see raw data? Enter yes to proceed.\n')
        if raw_data.lower() == 'yes':
            i = 0
            df_tmp = df.fillna('Unknown')
            while i < df_tmp['Start Time'].count() - 1:
                print("-"*90)
                print('Start Time    : {}'.format(df_tmp.iloc[i]['Start Time']))
                print('End Time      : {}'.format(df_tmp.iloc[i]['End Time']))
                print('Trip Duration : {}'.format(df_tmp.iloc[i]['Trip Duration']))
                print('Start Station : {}'.format(df_tmp.iloc[i]['Start Station']))
                print('End Station   : {}'.format(df_tmp.iloc[i]['End Station']))
                print('User Type     : {}'.format(df_tmp.iloc[i]['User Type']))
                print('Gender        : {}'.format(df_tmp.iloc[i]['Gender']))
                print('Birth Year    : {}'.format(df_tmp.iloc[i]['Birth Year'] if df_tmp.iloc[i]['Birth Year'] == 'Unknown' else int(df_tmp.iloc[i]['Birth Year'])))
                if (i+1)%3  == 0:
                    if input('-'*90 + '\nPlease Press Enter to see more records. Press anything else to exit.\n'):
                        break
                i += 1

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
