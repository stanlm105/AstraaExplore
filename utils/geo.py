"""
Geocoding utilities with database caching to reduce API calls.
"""

import os
import requests
from typing import Tuple, Optional
from services.target_guidance_computer.db import SessionLocal
from services.target_guidance_computer.models import GeocodeCache
from sqlalchemy import select

def lookup_latlon(country: str, zipcode: str) -> tuple[float, float]:
    """
    Look up latitude and longitude for a given country and zipcode.
    Uses database cache first, then falls back to Nominatim API.
    
    Args:
        country (str): 2-letter country code (e.g., 'US').
        zipcode (str): Postal/zip code.
        
    Returns:
        tuple: (lat, lon) as floats, or (None, None) if not found.
    """
    # Normalize inputs
    country = country.strip().upper()
    zipcode = zipcode.strip()
    
    if not country or not zipcode:
        return None, None
    
    # Check cache first
    with SessionLocal() as db:
        cached = db.execute(
            select(GeocodeCache).where(
                GeocodeCache.country == country,
                GeocodeCache.zipcode == zipcode
            )
        ).scalar_one_or_none()
        
        if cached:
            print(f"Using cached coordinates for {country}, {zipcode}")
            return cached.latitude, cached.longitude
    
    # Cache miss - call API
    print(f"Geocoding {country}, {zipcode} via API")
    lat, lon = _geocode_via_api(country, zipcode)
    
    # Store result in cache (even if None/None for failed lookups)
    with SessionLocal() as db:
        cache_entry = GeocodeCache(
            country=country,
            zipcode=zipcode,
            latitude=lat,
            longitude=lon
        )
        db.add(cache_entry)
        try:
            db.commit()
            print(f"Cached result for {country}, {zipcode}")
        except Exception as e:
            print(f"Failed to cache geocoding result: {e}")
            db.rollback()
    
    return lat, lon

def _geocode_via_api(country: str, zipcode: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Perform actual geocoding via Nominatim API.
    
    Args:
        country (str): Country code.
        zipcode (str): Postal code.
        
    Returns:
        tuple: (lat, lon) or (None, None) if failed.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "country": country,
        "postalcode": zipcode,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": f"MessierTargetGuidanceComputer/1.0 ({os.environ.get('GEONAMES_USERNAME', 'demo')})"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            print(f"No geocoding results for {country}, {zipcode}")
            return None, None
            
    except requests.exceptions.Timeout:
        print(f"Geocoding timeout for {country}, {zipcode}")
        return None, None
    except requests.exceptions.ConnectionError:
        print(f"Geocoding connection error for {country}, {zipcode}")
        return None, None
    except Exception as e:
        print(f"Geocoding error for {country}, {zipcode}: {e}")
        return None, None

def clear_geocode_cache(country: str = None, zipcode: str = None) -> int:
    """
    Clear geocoding cache entries. Useful for maintenance.
    
    Args:
        country (str, optional): If provided, only clear entries for this country.
        zipcode (str, optional): If provided, only clear entries for this zipcode.
        
    Returns:
        int: Number of entries deleted.
    """
    with SessionLocal() as db:
        query = select(GeocodeCache)
        if country:
            query = query.where(GeocodeCache.country == country.upper())
        if zipcode:
            query = query.where(GeocodeCache.zipcode == zipcode)
            
        entries = db.execute(query).scalars().all()
        count = len(entries)
        
        for entry in entries:
            db.delete(entry)
        db.commit()
        
        return count