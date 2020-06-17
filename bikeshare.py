import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


monthslist = ['january', 'feburary', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
dayslist =  ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
     
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - month to filter by as an int where 0= Jan.. 11 = Dec. "All" given special assignment of 999.
        (int) day - day to filter by as an int where 0= Monday.. 6 = Friday. "All" given special assignment of 999.
    """
    
    #intro
    print('Hello! Let\'s explore some US bikeshare data!')
   
    #requesting user city of interest   
    need_city = True
    while need_city:

        isny = False
        city = input("Please enter the name of the city you are interested in (available cities are: Chicago, New york City and Washington): ").lower()
        
        if CITY_DATA.get(city) is not None:
            need_city = False

        if city == "new york":
            userinput = input("Did you mean New York City?: ").lower()
            if userinput == "yes" or userinput == "y":
                city = "new york city"
                need_city = False
                isny = True

        if CITY_DATA.get(city.lower()) is None and isny == False:
            print("Sorry, we're not sure which City you want data for, please check the spelling and try again")

    print("Great, you've chosen " + city.title() + " as your City of interest.")

    #Requesting month of interest
    need_month = True
    
    while need_month:
      try:
        print("Please tell us which month of data you would like to see statistics for. Please type in the full month name (i.e. 'January'). Type 'all' to get unfiltered data. ")
        month = input("Month: ").lower()
        if month != "all":
            if monthslist.index(month) >= 0:
                month_index = monthslist.index(month) 
                need_month = False
            break
        if month == "all":
            month_index = 999 
            break
            
      except:
          print("Sorry we don't recognise that month, please check the spelling and try again.")  



    #Requesting day of interest
    need_day = True

    while need_day:
      try: 
        print("Please tell us which day of the week you would like to aggregate statistics for. Please type in the full day name (i.e. 'Monday'). Type 'all' to get unfiltered data. ")
        day = input("Day: ").lower()
        if day != "all":
            if dayslist.index(day) >= 0:
                day_index = dayslist.index(day) 
                need_day = False
            break
        if day == "all":
            day_index = 999 
            break
      except:
        print("Sorry we don't recognise that day, please check the spelling and try again") 

        
    print('-'*40)
    return city, month_index, day_index



def load_data(city, month_index, day_index):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - month to filter by as an int where 0= Jan.. 11 = Dec. "All" given special assignment of 999.
        (int) day - day to filter by as an int where 0= Monday.. 6 = Friday. "All" given special assignment of 999.
    Returns:
        filtereddata - Pandas DataFrame containing city data filtered by month and day
    """
    
    # get user input for month (all, january, february, ... , june)
    filtereddata = pd.read_csv(CITY_DATA[city])
    filtereddata['start_month'] = pd.to_datetime(filtereddata['Start Time']).dt.month
    filtereddata['start_day'] = pd.to_datetime(filtereddata['Start Time']).dt.weekday

    if month_index != 999:
        filtereddata = filtereddata[filtereddata['start_month'] == month_index]
    if day_index != 999:
        filtereddata = filtereddata[filtereddata['start_day'] == day_index]
    
#     print(filtereddata.head())
    return filtereddata

  

def time_stats(filtereddata):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = filtereddata['start_month'].mode().iloc[0]
    print("The most common month to start a trip in is: " + monthslist[month_mode].title())
    
    
    # display the most common day of week
    day_mode = filtereddata['start_day'].mode().iloc[0]
    print("The most common day to start a trip in is: " + dayslist[day_mode].title())

    # display the most common start hour
    filtereddata['start_hour'] = pd.to_datetime(filtereddata['Start Time']).dt.hour
    hour_mode = filtereddata['start_hour'].mode().iloc[0]
    print("The most common hour to start a trip in is: " + str(hour_mode) + ":00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(filtereddata):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    sstation_mode = filtereddata['Start Station'].mode().iloc[0]
    print("The most common station to **start** a trip at is: " + sstation_mode)


    # display most commonly used end station
    estation_mode = filtereddata['End Station'].mode().iloc[0]
    print("The most common station to **end** a trip in is: " + estation_mode)

    # TO DO: display most frequent combination of start station and end station trip
    filtereddata['trip'] = filtereddata['Start Station'] + " (to) " + filtereddata['End Station']
    trip_mode = filtereddata['trip'].mode().iloc[0]
    print("The most common journey (start station and end station combination) is: " + trip_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(filtereddata):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # getting diff between start and end times
    filtereddata["total_time"] = pd.to_datetime(filtereddata['End Time']) - pd.to_datetime(filtereddata['Start Time'])
    filtereddata["seconds"] = filtereddata["total_time"].dt.seconds
    
    # display total travel time
    sum_seconds = filtereddata["total_time"].dt.seconds.sum()
    sum_mins = sum_seconds//60
    sum_remain_seconds = sum_seconds%60
    print("Sum of all travel times {} mins and {} seconds".format(sum_mins, sum_remain_seconds))
    
    #getting mean trip duration
    mean_seconds = filtereddata["total_time"].dt.seconds.mean()
    mean_mins = mean_seconds//60
    mean_remain_seconds = mean_seconds%60
    
    print("Mean of all travel times {} mins and {} seconds".format(mean_mins, mean_remain_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def user_stats(filtereddata):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of users by user type: ")
    print(filtereddata["User Type"].value_counts())
  
    # TO DO: Display counts of gender
    if "Gender" in filtereddata:
      print("Number of users by gender: ")
      print(filtereddata["Gender"].value_counts())
    else:
      print("Sorry, no Gender information is available")  

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in filtereddata:
      min_birth = int(filtereddata["Birth Year"].min())
      max_birth = int(filtereddata["Birth Year"].max())
      mode_birth = int(filtereddata["Birth Year"].mode())
      print("The youngest user was born in {}, the oldest user {}, and the most common year of birth was {}".format(max_birth, min_birth, mode_birth))
    else: 
      print("Sorry, no Birth Year information is available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        filtereddata = load_data(city, month, day)
        
        if len(filtereddata) == 0:
            print("There is no data for these filters!")
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                main()
            return None
            

        time_stats(filtereddata)
        station_stats(filtereddata)
        trip_duration_stats(filtereddata)
        user_stats(filtereddata)
        
        need_response = True

        while need_response:
          
            answer = input("would you like to see some raw data for this dataset?: ").lower()
          

            if answer == "yes" or answer =="y":
                
                for i in range(len(filtereddata.head())):
                    row = filtereddata.iloc[i]
                    print(row)
                    print('\n')
                    
                    
                need_response = False


            elif answer == "no" or answer =="n":
                need_response = False

            else:
                print("Sorry, we didn't get that..")
                    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
    main()













