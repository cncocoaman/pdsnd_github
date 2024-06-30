import time
import pandas as pd

# Define the dictionary that maps cities to their corresponding data files
CITY_FILES = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Function to validate user input
def validate_input(prompt, valid_options):
    error_message = "Invalid input, please try again:"
    while True:
        user_input = input(prompt).lower().strip()
        if ',' in user_input:
            user_input = [item.strip().lower() for item in user_input.split(',')]
            if all(option in valid_options for option in user_input):
                break
        else:
            if user_input in valid_options:
                break
        prompt = error_message
    return user_input

# Function to get user input for city, month, and day
def gather_filters():
    print('Welcome! Let\'s examine some US bikeshare data!')
    
    city = ["chicago", "new york city", "washington"]
    month = ["all", "january", "february", "march", "april", "may", "june"]
    day = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    while True:
        city = validate_input("Choose a city (chicago, new york city, washington): ", city)
        month = validate_input("Choose a month (all, january, february, ..., june): ", month)
        day = validate_input("Choose a day of the week (all, monday, tuesday, ..., sunday): ", day)
        
        confirm = validate_input(f"Confirm your choices - City: {city}, Month: {month}, Day: {day}. (y/n): ", ('y', 'n'))
        if confirm == 'y':
            break
        else:
            print("Let's try again.")

    print('*' * 70)
    return city, month, day

# Function to load data based on user input
def load_city_data(city, month, day):
    try:
        df = pd.read_csv(CITY_FILES[city])
    except FileNotFoundError:
        print(f"Error: Data file for {city} not found.")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = month.index(month) + 1
        df = df[df['Month'] == month_index]

    if day != 'all':
        df = df[df['Day of Week'].str.lower() == day.lower()]

    return df

# Function to display most common statistics
def display_common_stats(df, column, label):
    if not df.empty:
        common_value = df[column].mode()[0]
        print(f'Most Common {label}: {common_value}')

# Function to calculate and display travel time statistics
def calculate_time_stats(df):
    print('\nCalculating Frequent Travel Times...\n')
    start = time.time()

    display_common_stats(df, 'Month', 'Month')
    display_common_stats(df, 'Day of Week', 'Day of the Week')
    display_common_stats(df, 'Hour', 'Start Hour')

    print(f"\nThis took {time.time() - start} seconds.")
    print('*' * 70)

# Function to calculate and display station statistics
def calculate_station_stats(df):
    print('\nCalculating Popular Stations and Trips...\n')
    start = time.time()

    display_common_stats(df, 'Start Station', 'Start Station')
    display_common_stats(df, 'End Station', 'End Station')

    if not df.empty:
        df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
        display_common_stats(df, 'Trip', 'Trip Combination')

    print(f"\nThis took {time.time() - start} seconds.")
    print('*' * 70)

# Function to calculate and display trip duration statistics
def calculate_trip_duration_stats(df):
    print('\nCalculating Trip Durations...\n')
    start = time.time()

    if not df.empty:
        total_duration = df['Trip Duration'].sum()
        mean_duration = df['Trip Duration'].mean()
        print(f'Total Travel Time: {total_duration}')
        print(f'Average Travel Time: {mean_duration}')

    print(f"\nThis took {time.time() - start} seconds.")
    print('*' * 70)

# Function to calculate and display user statistics
def calculate_user_stats(df, city):
    print('\nCalculating User Stats...\n')
    start = time.time()

    if not df.empty:
        user_types = df['User Type'].value_counts()
        print(f'User Types:\n{user_types}')

        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            print(f'Gender Counts:\n{gender_counts}')
        else:
            print(f'Gender data not available for {city}.')

        if 'Birth Year' in df.columns:
            earliest_birth = int(df['Birth Year'].min())
            latest_birth = int(df['Birth Year'].max())
            common_birth = int(df['Birth Year'].mode()[0])
            print(f'Earliest Birth Year: {earliest_birth}')
            print(f'Latest Birth Year: {latest_birth}')
            print(f'Most Common Birth Year: {common_birth}')
        else:
            print(f'Birth year data not available for {city}.')

    print(f"\nThis took {time.time() - start} seconds.")
    print('*' * 70)

# Function to display data based on user request
def display_raw_data(df):
    start_loc = 0
    view_data = validate_input("Would you like to see 5 rows of individual trip data? (y/n): ", ('y', 'n'))
    while view_data == 'y' and start_loc < len(df):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = validate_input("Do you want to continue viewing data? (y/n): ", ('y', 'n'))

# Main function to run the program
def main():
    while True:
        city, month, day = gather_filters()
        df = load_city_data(city, month, day)

        if df.empty:
            print("No data available for the selected filters. Please try again.")
            continue

        calculate_time_stats(df)
        display_raw_data(df)
        calculate_station_stats(df)
        calculate_trip_duration_stats(df)
        calculate_user_stats(df, city)

        restart = validate_input("Would you like to restart? (y/n): ", ('y', 'n'))
        if restart != 'y':
            break
        else:
            print("Thanks for searching~")

if __name__ == "__main__":
    main()
