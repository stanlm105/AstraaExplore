# not able to find a free API for this, so providing a convenient link for the user to check

import requests

def clearoutside_link(lat, lon):
    return f"https://clearoutside.com/forecast/{float(lat):.5f}/{float(lon):.5f}"