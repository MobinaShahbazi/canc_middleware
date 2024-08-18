class APINotAvailableError(Exception):
    """
    General Exception when attempting to get data from an API

    """


class JsonError(Exception):
    """Exception raised for errors envolving json."""

    def __init__(self, expression=None, type=False, empty=False):
        if type:
            self.message_en = f'{expression} is not a valid json'
            self.message_fa = f'{expression} جیسون معتبری نیست'
        elif not empty:
            self.message_en = f"{expression} can't be jsonified"
            self.message_fa = f'امکان تبدیل {expression} به جیسون نیست'
        else:
            self.message_en = 'json is empty'
            self.message_fa = 'جیسون خالی است'