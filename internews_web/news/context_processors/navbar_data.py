from news.services import get_serialized_countries


def navbar_data(request) -> dict:
    navbar_countries_data = get_serialized_countries()
    return {'navbar_countries_data': navbar_countries_data}
