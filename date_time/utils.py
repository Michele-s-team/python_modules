from datetime import datetime, timedelta

import constants.utils as const

'''
substract a time span expressed in seconds to a date
Input values: 
    * Mandatory:
        - `date`: the date, expressed as a string, such as '2014-01-01 00:00:00.000000'
        -  `seconds`: a float, the number of seconds to be substracted
    * Optional:
        - `date_format` (const.default_date_format): the format in which the output date will be returned
Return values: 
    - `date` - `seconds` expressed in format `date_format`

'''
def subtract_seconds(date, seconds, date_format=const.default_date_format):

    date_formatted = datetime.strptime(date, date_format)
    return (date_formatted - timedelta(seconds=seconds)).strftime(date_format)