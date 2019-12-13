import datetime


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Test
if __name__ == '__main__':
    print(validate_date("2015-05-13"))
    print(validate_date("2015-05-132"))
