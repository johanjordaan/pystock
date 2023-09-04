import field_names


def avg_filter(day_end_data, companies_data, isin_data, type, min_avg, max_avg):
    mean = day_end_data.groupby(field_names.TKR)[type].mean().reset_index()

    if min_avg is not None and max_avg is None:
        mean = mean[mean[type] >= min_avg]
    elif min_avg is None and max_avg is not None:
        mean = mean[mean[type] <= max_avg]
    elif min_avg is not None and max_avg is not None:
        mean = mean[(mean[type] >= min_avg) & (mean[type] <= max_avg)]

    valid_tkrs = mean[field_names.TKR].to_list()

    return tkr_filter(day_end_data, companies_data, isin_data, valid_tkrs)


def isin_type_filter(day_end_data, companies_data, isin_data, isin_types):
    if not isinstance(isin_types,list):
        isin_types = [isin_types]
    ordinary_fully_paid_tkrs = isin_data[isin_data[field_names.ISIN_TYPE].isin(isin_types)][field_names.TKR].to_list()
    return tkr_filter(day_end_data, companies_data, isin_data, ordinary_fully_paid_tkrs)


def tkr_filter(day_end_data, companies_data, isin_data, tkrs):
    if not isinstance(tkrs, list):
        tkrs = [tkrs]
    filtered_data = day_end_data[day_end_data[field_names.TKR].isin(tkrs)].copy()
    return filtered_data


def equal_data_by_tkr_filter(day_end_data, companies_data, isin_data):
    counts = day_end_data.groupby(field_names.TKR).count()
    max_count = counts.max()

    valid_tkrs = counts[counts[field_names.DATE] == max_count[field_names.DATE]].index

    return tkr_filter(day_end_data, companies_data, isin_data, valid_tkrs.to_list())