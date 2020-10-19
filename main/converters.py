class YearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:04}"

class MonthConverter:
    regex = "([0][0-9])|([1][012])"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:02}"

class DayConverter:
    regex = "([0-2][0-9])|([3][01])"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:02}"

    
