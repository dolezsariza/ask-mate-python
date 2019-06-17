def unix_to_utc(list_of_dict):
    for dict_ in list_of_dict:
        dict_["submission_time"] = datetime.utcfromtimestamp(int(dict_["submission_time"])).strftime('%Y.%m.%d. %H:%M:%S')
    return list_of_dict