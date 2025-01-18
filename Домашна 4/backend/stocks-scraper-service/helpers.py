from datetime import datetime, timedelta

def split_date_range(start_date, end_date, max_days=365):
    date_ranges = []

    while start_date < end_date:
        next_date = min(start_date + timedelta(days=max_days), end_date)

        formatted_start = f"{start_date.month}/{start_date.day}/{start_date.year}"
        formatted_end = f"{next_date.month}/{next_date.day}/{next_date.year}"

        date_ranges.append((formatted_start, formatted_end))
        start_date = next_date + timedelta(days=1)

    return date_ranges

def eu_format_to_iso_format(custom_date_str):
    dt = datetime.strptime(custom_date_str, '%d.%m.%Y')
    return dt.date().isoformat()

def iso_format_to_eu_format(date_str):
    dt = datetime.fromisoformat(date_str)
    return dt.strftime('%d.%m.%Y')

def eu_format_to_datetime(custom_date_str):
    return datetime.strptime(custom_date_str, '%d.%m.%Y').date()

def datetime_to_eu_format(dt):
    return dt.strftime('%d.%m.%Y')

def us_format_to_iso_format(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    return date_obj.strftime('%Y-%m-%d')

def us_format_to_datetime(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
    return date_obj

def us_format_to_eu_format(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    formatted_date = date_obj.strftime('%d.%m.%Y')
    return formatted_date


def convert_en_to_mk_number_format(input_str, to_dot=True):
    transformed = input_str.replace(',', '.')

    if to_dot:
        transformed = transformed.rsplit('.', 1)
        if len(transformed) > 1:
            transformed = f"{transformed[0]},{transformed[1]}"
        else:
            transformed = transformed[0]

    return transformed

def standardize_mk_number_format(value):
    return value.replace(",", ".") + ",00"