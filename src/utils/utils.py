from datetime import datetime


def create_temp_value_text(selected_temp_unit, temp_value):
    """
    Seçilen sıcaklık birimine göre sıcaklık değerini metin olarak oluşturur.

    Args:
        selected_temp_unit (str): Seçilen sıcaklık birimi ("Santigrat" veya "Fahrenheit").
        temp_value (int): Sıcaklık değeri.

    Returns:
        str: Oluşturulan sıcaklık metni.
    """
    converted_temp_value = convert_temp_value(selected_temp_unit, temp_value)
    if selected_temp_unit == "Santigrat":
        return f"{converted_temp_value}°C"
    else:
        return f"{converted_temp_value}°F"


def convert_temp_value(selected_temp_unit, temp_value):
    """
    Sıcaklık birimini dönüştürür.

    Args:
        selected_temp_unit (str): Seçilen sıcaklık birimi ("Santigrat" veya "Fahrenheit").
        temp_value (int): Sıcaklık değeri.

    Returns:
        int: Dönüştürülmüş sıcaklık değeri.
    """
    temp_value = int(temp_value)
    if selected_temp_unit == "Santigrat":
        return temp_value
    else:
        return int(temp_value * 9 / 5) + 32


def create_wind_value_text(wind_dict):
    """
    Rüzgar bilgisini metin olarak oluşturur.

    Args:
        wind_dict (dict): Rüzgar bilgisi içeren sözlük.

    Returns:
        str: Oluşturulan rüzgar metni.
    """
    speed = wind_dict["speed"]
    degree = wind_dict["deg"]
    return f"{speed} m/s, {degree}°"


def timestamp_to_date(timestamp):
    """
    Timestamp'ı tarihe çevirir.

    Args:
        timestamp (int): Unix timestamp değeri.

    Returns:
        str: Oluşturulan tarih metni (gün/ay/yıl).
    """
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_date = dt_object.strftime("%d/%m/%Y")
    return formatted_date


def capitalize_first_letter(input_string):
    """
    String'in ilk harfini büyütür.

    Args:
        input_string (str): İşlem yapılacak string.

    Returns:
        str: İlk harfi büyütülmüş string.
    """
    if not input_string:
        return input_string

    return input_string[0].upper() + input_string[1:]


def switch_page(hide_function, switched_frame_show, event_skip_function):
    """
    Sayfa değiştirme işlemini gerçekleştirir.

    Args:
        hide_function (function): Mevcut pencereyi gizlemek için kullanılan fonksiyon.
        switched_frame_show (function): Yeni pencereyi göstermek için kullanılan fonksiyon.
        event_skip_function (function): Olayı atlamak için kullanılan fonksiyon.
    """
    hide_function()
    switched_frame_show()
    event_skip_function()
