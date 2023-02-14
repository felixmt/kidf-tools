"""modules imports
"""
from datetime import date, datetime

class date_helper:
    """various tools to interact with dates
    """
    def first_dow_in_a_month(self, year: int, month: int, dow: int):
        """get date of the first given day of the week in a month
        0 = Monday, 6 = Sunday
        @returns: date
        """
        # Monday = 0, Sunday = 6
        day: int = ((8 + dow) - date(year, month, 1).weekday()) % 7

        return date(year, month, day if day > 0 else 7)

    def validate_date_format(self, date_text: str, date_format: str = "%Y-%m-%d %H:%M:%S"):
        """validate_date_format
        """
        try:
            datetime.strptime(date_text, date_format)
        except ValueError:
            raise ValueError(
                "date should be at the following format : " + date_format
            ) from None
