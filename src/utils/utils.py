from datetime import datetime


def create_temp_value_text(selected_temp_unit, temp_value):
    converted_temp_value = convert_temp_value(selected_temp_unit, temp_value)
    if selected_temp_unit == "Santigrat":
        return f"{converted_temp_value}°C"
    else:
        return f"{converted_temp_value}°F"


def convert_temp_value(selected_temp_unit, temp_value):
    temp_value = int(temp_value)
    if selected_temp_unit == "Santigrat":
        return temp_value
    else:
        return int(temp_value * 9 / 5) + 32


def create_wind_value_text(wind_dict):
    speed = wind_dict["speed"]
    degree = wind_dict["deg"]
    return f"{speed} m/s, {degree}°"


def timestamp_to_date(timestamp):
    # Timestamp'ı datetime nesnesine çevirir.
    dt_object = datetime.fromtimestamp(timestamp)

    # datetime nesnesini "gün/ay/yıl" olacak şekilde tarihe çevirir.
    formatted_date = dt_object.strftime("%d/%m/%Y")

    return formatted_date


def capitalize_first_letter(input_string):
    # Küçük harfler ile yazılmış string'imizin ilk harfini büyültür.
    if not input_string:
        return input_string

    return input_string[0].upper() + input_string[1:]


def switch_page(hide_function, switched_frame_show, event_skip_function):
    hide_function()
    switched_frame_show()
    event_skip_function()
