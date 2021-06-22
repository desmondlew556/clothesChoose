from datetime import datetime
from datetime import timezone
import pytz

def convert_date(date_time_str):
    ''' 
    Converts datetime with format "May 17 04:47:50 2021 GMT" to python datetime object and finds difference between the two.
    Works only for GMT time
    Args:
        date_time_str(string): date with format MMM DD HH:MM:SS YYYY ZZZ where HH is in 24 hours format
    Returns:
        date_time_fields(str[5]): [date_time_str in datetime format, datetime difference ("current time is more recent than given time " or "given time is more recent than current time"), days, hours, minutes] 
    '''
    #convert date_time_str to python datetime object
    date_time_obj = datetime.strptime(date_time_str, '%b %d %H:%M:%S %Y %Z')
    #get current GMT time
    current_gmt_time = datetime.utcnow()
    if(current_gmt_time>date_time_obj):
        datetime_difference_in_timedelta = current_gmt_time-date_time_obj
        datetime_difference = "Current time is more recent than given time "
    else:
        datetime_difference_in_timedelta = date_time_obj-current_gmt_time
        datetime_difference = "Given time is more recent than current time"
    #print(datetime_difference_in_timedelta)
    days_diff = datetime_difference_in_timedelta.days
    hours_diff = datetime_difference_in_timedelta.seconds//3600
    minutes_diff = datetime_difference_in_timedelta.seconds%3600//60
    return [date_time_obj,datetime_difference,days_diff,hours_diff,minutes_diff]

def convert_date_any_timezone(date_time_str):
    ''' 
    Converts datetime with format "May 17 04:47:50 2021 GMT" to python datetime object and finds difference between the two.
    works for timezones in pytz (pytz.all_timezones gives list of all timezones accounted for)
    Args:
        date_time_str(string): date with format MMM DD HH:MM:SS YYYY ZZZ where HH is in 24 hours format
    Returns:
        date_time_fields(str[5]): [date_time_str in datetime format, datetime difference ("current time is more recent than given time " or "given time is more recent than current time"), days, hours, minutes] 
    '''
    #convert date_time_str to python datetime object
    date_time_obj = datetime.strptime(date_time_str[:-4], '%b %d %H:%M:%S %Y')
    time_zone_str = date_time_str.split(" ")[4]
    time_zone = pytz.timezone(time_zone_str)
    #include time zone infomration in given datetime
    date_time_obj = date_time_obj.replace(tzinfo = time_zone)
    #get current local time
    current_local_time = datetime.now()
    #converts local time to given time zone
    current_time_in_given_time_zone = current_local_time.astimezone(time_zone)
    print(current_local_time)
    print(current_time_in_given_time_zone)
    if(current_time_in_given_time_zone>date_time_obj):
        datetime_difference_in_timedelta = current_time_in_given_time_zone-date_time_obj
        datetime_difference = "Current time is more recent than given time "
    else:
        datetime_difference_in_timedelta = date_time_obj-current_time_in_given_time_zone
        datetime_difference = "Given time is more recent than current time"
    #print(datetime_difference_in_timedelta)
    days_diff = datetime_difference_in_timedelta.days
    hours_diff = datetime_difference_in_timedelta.seconds//3600
    minutes_diff = datetime_difference_in_timedelta.seconds%3600//60
    return [date_time_obj,datetime_difference,days_diff,hours_diff,minutes_diff]

date_time_str = "Jun 09 21:19:00 2021 HST"
date_time_fields = convert_date_any_timezone(date_time_str)
print("date_time_str in datetime format: " + date_time_fields[0].strftime("%Y/%m/%d, %H:%M:%S"))
print(date_time_fields[1]+" by "+str(date_time_fields[2])+" days "+str(date_time_fields[3])+" hours "+ str(date_time_fields[4])+" minutes.")