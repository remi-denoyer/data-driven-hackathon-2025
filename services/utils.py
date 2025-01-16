def field_selector(data_array: list, fields: list) -> list:
    """
    Filter JSON objects to only include specified fields.

    Args:
        data_array (list): List of dictionaries containing data
        fields (list): List of field names to keep

    Returns:
        list: List of filtered dictionaries containing only specified fields
    """
    return [{key: item[key] for key in fields if key in item} for item in data_array]
