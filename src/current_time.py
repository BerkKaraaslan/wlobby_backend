import datetime

def curr_time(): # this function returns the current time as string. By this way we can compare times by <,>,== operators and easily insert into our db
    return str(datetime.datetime.now())
