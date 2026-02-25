#!/usr/bin/env python3
"""
✈  Airport Routing Code Lookup CLI
Supports IATA (e.g. LAX) and ICAO (e.g. KLAX) code lookups.
Returns: name, city, country, timezone, coordinates, and both codes.

Usage:
  python airport_lookup.py LAX
  python airport_lookup.py EGLL
  python airport_lookup.py --search london
  python airport_lookup.py --list-country US
  python airport_lookup.py LAX JFK NRT          # multiple lookups
"""

import sys
import argparse
import json
from math import radians, sin, cos, sqrt, atan2

# ─────────────────────────────────────────────────────────────────────────────
# AIRPORT DATABASE
# Fields: name, city, country, iata, icao, lat, lon, altitude_ft, timezone
# ─────────────────────────────────────────────────────────────────────────────
AIRPORTS = [
    # ── United States (35) ────────────────────────────────────────────────────
    {"name": "Los Angeles International Airport",        "city": "Los Angeles",     "country": "United States", "iata": "LAX", "icao": "KLAX", "lat": 33.9425,  "lon": -118.4081, "alt": 125,  "tz": "America/Los_Angeles"},
    {"name": "John F. Kennedy International Airport",    "city": "New York",        "country": "United States", "iata": "JFK", "icao": "KJFK", "lat": 40.6413,  "lon": -73.7781,  "alt": 13,   "tz": "America/New_York"},
    {"name": "O'Hare International Airport",             "city": "Chicago",         "country": "United States", "iata": "ORD", "icao": "KORD", "lat": 41.9742,  "lon": -87.9073,  "alt": 672,  "tz": "America/Chicago"},
    {"name": "Hartsfield-Jackson Atlanta Intl Airport",  "city": "Atlanta",         "country": "United States", "iata": "ATL", "icao": "KATL", "lat": 33.6407,  "lon": -84.4277,  "alt": 1026, "tz": "America/New_York"},
    {"name": "Dallas/Fort Worth International Airport",  "city": "Dallas",          "country": "United States", "iata": "DFW", "icao": "KDFW", "lat": 32.8998,  "lon": -97.0403,  "alt": 607,  "tz": "America/Chicago"},
    {"name": "Denver International Airport",             "city": "Denver",          "country": "United States", "iata": "DEN", "icao": "KDEN", "lat": 39.8561,  "lon": -104.6737, "alt": 5433, "tz": "America/Denver"},
    {"name": "San Francisco International Airport",      "city": "San Francisco",   "country": "United States", "iata": "SFO", "icao": "KSFO", "lat": 37.6213,  "lon": -122.3790, "alt": 13,   "tz": "America/Los_Angeles"},
    {"name": "Seattle-Tacoma International Airport",     "city": "Seattle",         "country": "United States", "iata": "SEA", "icao": "KSEA", "lat": 47.4502,  "lon": -122.3088, "alt": 433,  "tz": "America/Los_Angeles"},
    {"name": "Miami International Airport",              "city": "Miami",           "country": "United States", "iata": "MIA", "icao": "KMIA", "lat": 25.7959,  "lon": -80.2870,  "alt": 8,    "tz": "America/New_York"},
    {"name": "Newark Liberty International Airport",     "city": "Newark",          "country": "United States", "iata": "EWR", "icao": "KEWR", "lat": 40.6895,  "lon": -74.1745,  "alt": 18,   "tz": "America/New_York"},
    {"name": "Minneapolis–Saint Paul Intl Airport",      "city": "Minneapolis",     "country": "United States", "iata": "MSP", "icao": "KMSP", "lat": 44.8848,  "lon": -93.2223,  "alt": 841,  "tz": "America/Chicago"},
    {"name": "Phoenix Sky Harbor International Airport", "city": "Phoenix",         "country": "United States", "iata": "PHX", "icao": "KPHX", "lat": 33.4373,  "lon": -112.0078, "alt": 1135, "tz": "America/Phoenix"},
    {"name": "Boston Logan International Airport",       "city": "Boston",          "country": "United States", "iata": "BOS", "icao": "KBOS", "lat": 42.3656,  "lon": -71.0096,  "alt": 20,   "tz": "America/New_York"},
    {"name": "Las Vegas Harry Reid Intl Airport",        "city": "Las Vegas",       "country": "United States", "iata": "LAS", "icao": "KLAS", "lat": 36.0840,  "lon": -115.1537, "alt": 2181, "tz": "America/Los_Angeles"},
    {"name": "Charlotte Douglas International Airport",  "city": "Charlotte",       "country": "United States", "iata": "CLT", "icao": "KCLT", "lat": 35.2140,  "lon": -80.9431,  "alt": 748,  "tz": "America/New_York"},
    {"name": "George Bush Intercontinental Airport",     "city": "Houston",         "country": "United States", "iata": "IAH", "icao": "KIAH", "lat": 29.9902,  "lon": -95.3368,  "alt": 97,   "tz": "America/Chicago"},
    {"name": "Orlando International Airport",            "city": "Orlando",         "country": "United States", "iata": "MCO", "icao": "KMCO", "lat": 28.4294,  "lon": -81.3089,  "alt": 96,   "tz": "America/New_York"},
    {"name": "Washington Dulles International Airport",  "city": "Washington D.C.", "country": "United States", "iata": "IAD", "icao": "KIAD", "lat": 38.9531,  "lon": -77.4565,  "alt": 313,  "tz": "America/New_York"},
    {"name": "Ronald Reagan Washington National Airport","city": "Washington D.C.", "country": "United States", "iata": "DCA", "icao": "KDCA", "lat": 38.8512,  "lon": -77.0402,  "alt": 15,   "tz": "America/New_York"},
    {"name": "Honolulu Daniel K. Inouye Intl Airport",   "city": "Honolulu",        "country": "United States", "iata": "HNL", "icao": "PHNL", "lat": 21.3187,  "lon": -157.9225, "alt": 13,   "tz": "Pacific/Honolulu"},
    {"name": "Ted Stevens Anchorage Intl Airport",       "city": "Anchorage",       "country": "United States", "iata": "ANC", "icao": "PANC", "lat": 61.1743,  "lon": -149.9963, "alt": 152,  "tz": "America/Anchorage"},
    {"name": "San Diego International Airport",          "city": "San Diego",       "country": "United States", "iata": "SAN", "icao": "KSAN", "lat": 32.7336,  "lon": -117.1897, "alt": 17,   "tz": "America/Los_Angeles"},
    {"name": "Tampa International Airport",              "city": "Tampa",           "country": "United States", "iata": "TPA", "icao": "KTPA", "lat": 27.9755,  "lon": -82.5332,  "alt": 26,   "tz": "America/New_York"},
    {"name": "Portland International Airport",           "city": "Portland",        "country": "United States", "iata": "PDX", "icao": "KPDX", "lat": 45.5887,  "lon": -122.5975, "alt": 31,   "tz": "America/Los_Angeles"},
    {"name": "Detroit Metropolitan Wayne County Airport","city": "Detroit",         "country": "United States", "iata": "DTW", "icao": "KDTW", "lat": 42.2124,  "lon": -83.3534,  "alt": 645,  "tz": "America/Detroit"},
    {"name": "Philadelphia International Airport",       "city": "Philadelphia",    "country": "United States", "iata": "PHL", "icao": "KPHL", "lat": 39.8719,  "lon": -75.2411,  "alt": 36,   "tz": "America/New_York"},
    {"name": "Salt Lake City International Airport",     "city": "Salt Lake City",  "country": "United States", "iata": "SLC", "icao": "KSLC", "lat": 40.7884,  "lon": -111.9778, "alt": 4227, "tz": "America/Denver"},
    {"name": "Baltimore/Washington Intl Airport",        "city": "Baltimore",       "country": "United States", "iata": "BWI", "icao": "KBWI", "lat": 39.1754,  "lon": -76.6683,  "alt": 146,  "tz": "America/New_York"},
    {"name": "Nashville International Airport",          "city": "Nashville",       "country": "United States", "iata": "BNA", "icao": "KBNA", "lat": 36.1245,  "lon": -86.6782,  "alt": 599,  "tz": "America/Chicago"},
    {"name": "Kansas City International Airport",        "city": "Kansas City",     "country": "United States", "iata": "MCI", "icao": "KMCI", "lat": 39.2976,  "lon": -94.7139,  "alt": 1026, "tz": "America/Chicago"},
    {"name": "Austin-Bergstrom International Airport",   "city": "Austin",          "country": "United States", "iata": "AUS", "icao": "KAUS", "lat": 30.1975,  "lon": -97.6664,  "alt": 542,  "tz": "America/Chicago"},
    {"name": "Raleigh-Durham International Airport",     "city": "Raleigh",         "country": "United States", "iata": "RDU", "icao": "KRDU", "lat": 35.8776,  "lon": -78.7875,  "alt": 435,  "tz": "America/New_York"},
    {"name": "Pittsburgh International Airport",         "city": "Pittsburgh",      "country": "United States", "iata": "PIT", "icao": "KPIT", "lat": 40.4915,  "lon": -80.2329,  "alt": 1203, "tz": "America/New_York"},
    {"name": "Louis Armstrong New Orleans Intl Airport", "city": "New Orleans",     "country": "United States", "iata": "MSY", "icao": "KMSY", "lat": 29.9934,  "lon": -90.2580,  "alt": 4,    "tz": "America/Chicago"},
    {"name": "Indianapolis International Airport",       "city": "Indianapolis",    "country": "United States", "iata": "IND", "icao": "KIND", "lat": 39.7173,  "lon": -86.2944,  "alt": 797,  "tz": "America/Indiana/Indianapolis"},
    # ── Canada (7) ────────────────────────────────────────────────────────────
    {"name": "Toronto Pearson International Airport",    "city": "Toronto",         "country": "Canada",        "iata": "YYZ", "icao": "CYYZ", "lat": 43.6777,  "lon": -79.6248,  "alt": 569,  "tz": "America/Toronto"},
    {"name": "Vancouver International Airport",          "city": "Vancouver",       "country": "Canada",        "iata": "YVR", "icao": "CYVR", "lat": 49.1967,  "lon": -123.1815, "alt": 14,   "tz": "America/Vancouver"},
    {"name": "Montréal-Trudeau International Airport",   "city": "Montreal",        "country": "Canada",        "iata": "YUL", "icao": "CYUL", "lat": 45.4706,  "lon": -73.7408,  "alt": 118,  "tz": "America/Toronto"},
    {"name": "Calgary International Airport",            "city": "Calgary",         "country": "Canada",        "iata": "YYC", "icao": "CYYC", "lat": 51.1315,  "lon": -114.0106, "alt": 3557, "tz": "America/Edmonton"},
    {"name": "Edmonton International Airport",           "city": "Edmonton",        "country": "Canada",        "iata": "YEG", "icao": "CYEG", "lat": 53.3097,  "lon": -113.5800, "alt": 2373, "tz": "America/Edmonton"},
    {"name": "Ottawa Macdonald-Cartier Intl Airport",    "city": "Ottawa",          "country": "Canada",        "iata": "YOW", "icao": "CYOW", "lat": 45.3225,  "lon": -75.6692,  "alt": 374,  "tz": "America/Toronto"},
    {"name": "Winnipeg James Armstrong Richardson Intl", "city": "Winnipeg",        "country": "Canada",        "iata": "YWG", "icao": "CYWG", "lat": 49.9100,  "lon": -97.2399,  "alt": 783,  "tz": "America/Winnipeg"},
    # ── Mexico & Central America (5) ──────────────────────────────────────────
    {"name": "Mexico City Felipe Angeles Intl Airport",  "city": "Mexico City",     "country": "Mexico",        "iata": "NLU", "icao": "MMSM", "lat": 19.7561,  "lon": -99.0150,  "alt": 7316, "tz": "America/Mexico_City"},
    {"name": "Mexico City International Airport",        "city": "Mexico City",     "country": "Mexico",        "iata": "MEX", "icao": "MMMX", "lat": 19.4363,  "lon": -99.0721,  "alt": 7316, "tz": "America/Mexico_City"},
    {"name": "Cancún International Airport",             "city": "Cancún",          "country": "Mexico",        "iata": "CUN", "icao": "MMUN", "lat": 21.0365,  "lon": -86.8770,  "alt": 22,   "tz": "America/Cancun"},
    {"name": "Guadalajara Don Miguel Hidalgo Intl",      "city": "Guadalajara",     "country": "Mexico",        "iata": "GDL", "icao": "MMGL", "lat": 20.5218,  "lon": -103.3107, "alt": 5016, "tz": "America/Mexico_City"},
    {"name": "Juan Santamaría International Airport",    "city": "San José",        "country": "Costa Rica",    "iata": "SJO", "icao": "MROC", "lat": 9.9939,   "lon": -84.2088,  "alt": 3021, "tz": "America/Costa_Rica"},
    # ── Caribbean (2) ─────────────────────────────────────────────────────────
    {"name": "Luis Muñoz Marín International Airport",   "city": "San Juan",        "country": "Puerto Rico",   "iata": "SJU", "icao": "TJSJ", "lat": 18.4394,  "lon": -66.0018,  "alt": 9,    "tz": "America/Puerto_Rico"},
    {"name": "Norman Manley International Airport",      "city": "Kingston",        "country": "Jamaica",       "iata": "KIN", "icao": "MKJP", "lat": 17.9357,  "lon": -76.7875,  "alt": 10,   "tz": "America/Jamaica"},
    # ── South America (10) ────────────────────────────────────────────────────
    {"name": "São Paulo–Guarulhos Intl Airport",         "city": "São Paulo",       "country": "Brazil",        "iata": "GRU", "icao": "SBGR", "lat": -23.4356, "lon": -46.4731,  "alt": 2459, "tz": "America/Sao_Paulo"},
    {"name": "São Paulo Congonhas Airport",               "city": "São Paulo",       "country": "Brazil",        "iata": "CGH", "icao": "SBSP", "lat": -23.6261, "lon": -46.6564,  "alt": 2631, "tz": "America/Sao_Paulo"},
    {"name": "Rio de Janeiro–Galeão Intl Airport",        "city": "Rio de Janeiro",  "country": "Brazil",        "iata": "GIG", "icao": "SBGL", "lat": -22.8099, "lon": -43.2505,  "alt": 28,   "tz": "America/Sao_Paulo"},
    {"name": "El Dorado International Airport",          "city": "Bogotá",          "country": "Colombia",      "iata": "BOG", "icao": "SKBO", "lat": 4.7016,   "lon": -74.1469,  "alt": 8360, "tz": "America/Bogota"},
    {"name": "Jorge Chávez International Airport",       "city": "Lima",            "country": "Peru",          "iata": "LIM", "icao": "SPJC", "lat": -12.0219, "lon": -77.1143,  "alt": 113,  "tz": "America/Lima"},
    {"name": "Ministro Pistarini International Airport", "city": "Buenos Aires",    "country": "Argentina",     "iata": "EZE", "icao": "SAEZ", "lat": -34.8222, "lon": -58.5358,  "alt": 67,   "tz": "America/Argentina/Buenos_Aires"},
    {"name": "Arturo Merino Benítez Intl Airport",       "city": "Santiago",        "country": "Chile",         "iata": "SCL", "icao": "SCEL", "lat": -33.3930, "lon": -70.7858,  "alt": 1555, "tz": "America/Santiago"},
    {"name": "Simon Bolivar International Airport",      "city": "Caracas",         "country": "Venezuela",     "iata": "CCS", "icao": "SVMI", "lat": 10.6031,  "lon": -66.9906,  "alt": 235,  "tz": "America/Caracas"},
    {"name": "Mariscal Sucre International Airport",     "city": "Quito",           "country": "Ecuador",       "iata": "UIO", "icao": "SEQM", "lat": -0.1292,  "lon": -78.3575,  "alt": 7874, "tz": "America/Guayaquil"},
    {"name": "Viru Viru International Airport",          "city": "Santa Cruz",      "country": "Bolivia",       "iata": "VVI", "icao": "SLVR", "lat": -17.6448, "lon": -63.1354,  "alt": 1224, "tz": "America/La_Paz"},
    # ── United Kingdom (4) ────────────────────────────────────────────────────
    {"name": "Heathrow Airport",                         "city": "London",          "country": "United Kingdom","iata": "LHR", "icao": "EGLL", "lat": 51.4775,  "lon": -0.4614,   "alt": 83,   "tz": "Europe/London"},
    {"name": "Gatwick Airport",                          "city": "London",          "country": "United Kingdom","iata": "LGW", "icao": "EGKK", "lat": 51.1481,  "lon": -0.1903,   "alt": 202,  "tz": "Europe/London"},
    {"name": "Manchester Airport",                       "city": "Manchester",      "country": "United Kingdom","iata": "MAN", "icao": "EGCC", "lat": 53.3537,  "lon": -2.2750,   "alt": 257,  "tz": "Europe/London"},
    {"name": "Edinburgh Airport",                        "city": "Edinburgh",       "country": "United Kingdom","iata": "EDI", "icao": "EGPH", "lat": 55.9500,  "lon": -3.3725,   "alt": 135,  "tz": "Europe/London"},
    # ── Western Europe (25) ───────────────────────────────────────────────────
    {"name": "Charles de Gaulle Airport",                "city": "Paris",           "country": "France",        "iata": "CDG", "icao": "LFPG", "lat": 49.0097,  "lon": 2.5479,    "alt": 392,  "tz": "Europe/Paris"},
    {"name": "Paris Orly Airport",                       "city": "Paris",           "country": "France",        "iata": "ORY", "icao": "LFPO", "lat": 48.7253,  "lon": 2.3594,    "alt": 291,  "tz": "Europe/Paris"},
    {"name": "Nice Côte d'Azur Airport",                 "city": "Nice",            "country": "France",        "iata": "NCE", "icao": "LFMN", "lat": 43.6584,  "lon": 7.2159,    "alt": 12,   "tz": "Europe/Paris"},
    {"name": "Frankfurt Airport",                        "city": "Frankfurt",       "country": "Germany",       "iata": "FRA", "icao": "EDDF", "lat": 50.0379,  "lon": 8.5622,    "alt": 364,  "tz": "Europe/Berlin"},
    {"name": "Munich Airport",                           "city": "Munich",          "country": "Germany",       "iata": "MUC", "icao": "EDDM", "lat": 48.3538,  "lon": 11.7861,   "alt": 1487, "tz": "Europe/Berlin"},
    {"name": "Berlin Brandenburg Airport",               "city": "Berlin",          "country": "Germany",       "iata": "BER", "icao": "EDDB", "lat": 52.3667,  "lon": 13.5033,   "alt": 157,  "tz": "Europe/Berlin"},
    {"name": "Amsterdam Airport Schiphol",               "city": "Amsterdam",       "country": "Netherlands",   "iata": "AMS", "icao": "EHAM", "lat": 52.3105,  "lon": 4.7683,    "alt": -11,  "tz": "Europe/Amsterdam"},
    {"name": "Madrid Barajas International Airport",     "city": "Madrid",          "country": "Spain",         "iata": "MAD", "icao": "LEMD", "lat": 40.4719,  "lon": -3.5626,   "alt": 2000, "tz": "Europe/Madrid"},
    {"name": "Barcelona El Prat Airport",                "city": "Barcelona",       "country": "Spain",         "iata": "BCN", "icao": "LEBL", "lat": 41.2971,  "lon": 2.0785,    "alt": 12,   "tz": "Europe/Madrid"},
    {"name": "Palma de Mallorca Airport",                "city": "Palma",           "country": "Spain",         "iata": "PMI", "icao": "LEPA", "lat": 39.5517,  "lon": 2.7388,    "alt": 27,   "tz": "Europe/Madrid"},
    {"name": "Rome Fiumicino Airport",                   "city": "Rome",            "country": "Italy",         "iata": "FCO", "icao": "LIRF", "lat": 41.8003,  "lon": 12.2389,   "alt": 13,   "tz": "Europe/Rome"},
    {"name": "Milan Malpensa Airport",                   "city": "Milan",           "country": "Italy",         "iata": "MXP", "icao": "LIMC", "lat": 45.6306,  "lon": 8.7281,    "alt": 768,  "tz": "Europe/Rome"},
    {"name": "Zurich Airport",                           "city": "Zurich",          "country": "Switzerland",   "iata": "ZRH", "icao": "LSZH", "lat": 47.4647,  "lon": 8.5492,    "alt": 1416, "tz": "Europe/Zurich"},
    {"name": "Geneva Airport",                           "city": "Geneva",          "country": "Switzerland",   "iata": "GVA", "icao": "LSGG", "lat": 46.2381,  "lon": 6.1090,    "alt": 1411, "tz": "Europe/Zurich"},
    {"name": "Copenhagen Airport",                       "city": "Copenhagen",      "country": "Denmark",       "iata": "CPH", "icao": "EKCH", "lat": 55.6180,  "lon": 12.6560,   "alt": 17,   "tz": "Europe/Copenhagen"},
    {"name": "Stockholm Arlanda Airport",                "city": "Stockholm",       "country": "Sweden",        "iata": "ARN", "icao": "ESSA", "lat": 59.6519,  "lon": 17.9186,   "alt": 137,  "tz": "Europe/Stockholm"},
    {"name": "Helsinki-Vantaa Airport",                  "city": "Helsinki",        "country": "Finland",       "iata": "HEL", "icao": "EFHK", "lat": 60.3172,  "lon": 24.9633,   "alt": 179,  "tz": "Europe/Helsinki"},
    {"name": "Oslo Gardermoen Airport",                  "city": "Oslo",            "country": "Norway",        "iata": "OSL", "icao": "ENGM", "lat": 60.1939,  "lon": 11.1004,   "alt": 681,  "tz": "Europe/Oslo"},
    {"name": "Vienna International Airport",             "city": "Vienna",          "country": "Austria",       "iata": "VIE", "icao": "LOWW", "lat": 48.1103,  "lon": 16.5697,   "alt": 600,  "tz": "Europe/Vienna"},
    {"name": "Brussels Airport",                         "city": "Brussels",        "country": "Belgium",       "iata": "BRU", "icao": "EBBR", "lat": 50.9014,  "lon": 4.4844,    "alt": 184,  "tz": "Europe/Brussels"},
    {"name": "Lisbon Humberto Delgado Airport",          "city": "Lisbon",          "country": "Portugal",      "iata": "LIS", "icao": "LPPT", "lat": 38.7813,  "lon": -9.1359,   "alt": 374,  "tz": "Europe/Lisbon"},
    {"name": "Dublin Airport",                           "city": "Dublin",          "country": "Ireland",       "iata": "DUB", "icao": "EIDW", "lat": 53.4213,  "lon": -6.2701,   "alt": 242,  "tz": "Europe/Dublin"},
    {"name": "Athens International Airport",             "city": "Athens",          "country": "Greece",        "iata": "ATH", "icao": "LGAV", "lat": 37.9364,  "lon": 23.9445,   "alt": 308,  "tz": "Europe/Athens"},
    {"name": "Luxembourg Findel Airport",                "city": "Luxembourg City", "country": "Luxembourg",    "iata": "LUX", "icao": "ELLX", "lat": 49.6233,  "lon": 6.2044,    "alt": 1234, "tz": "Europe/Luxembourg"},
    {"name": "Reykjavik Keflavik International Airport", "city": "Reykjavik",       "country": "Iceland",       "iata": "KEF", "icao": "BIKF", "lat": 63.9850,  "lon": -22.6057,  "alt": 171,  "tz": "Atlantic/Reykjavik"},
    # ── Eastern & Central Europe (8) ──────────────────────────────────────────
    {"name": "Warsaw Chopin Airport",                    "city": "Warsaw",          "country": "Poland",        "iata": "WAW", "icao": "EPWA", "lat": 52.1657,  "lon": 20.9671,   "alt": 361,  "tz": "Europe/Warsaw"},
    {"name": "Prague Václav Havel Airport",              "city": "Prague",          "country": "Czech Republic","iata": "PRG", "icao": "LKPR", "lat": 50.1008,  "lon": 14.2600,   "alt": 1247, "tz": "Europe/Prague"},
    {"name": "Budapest Ferenc Liszt Intl Airport",       "city": "Budapest",        "country": "Hungary",       "iata": "BUD", "icao": "LHBP", "lat": 47.4298,  "lon": 19.2610,   "alt": 495,  "tz": "Europe/Budapest"},
    {"name": "Bucharest Henri Coandă Intl Airport",      "city": "Bucharest",       "country": "Romania",       "iata": "OTP", "icao": "LROP", "lat": 44.5711,  "lon": 26.0850,   "alt": 314,  "tz": "Europe/Bucharest"},
    {"name": "Sofia Airport",                            "city": "Sofia",           "country": "Bulgaria",      "iata": "SOF", "icao": "LBSF", "lat": 42.6967,  "lon": 23.4114,   "alt": 1742, "tz": "Europe/Sofia"},
    {"name": "Belgrade Nikola Tesla Airport",            "city": "Belgrade",        "country": "Serbia",        "iata": "BEG", "icao": "LYBE", "lat": 44.8184,  "lon": 20.3091,   "alt": 335,  "tz": "Europe/Belgrade"},
    {"name": "Zagreb Franjo Tuđman Airport",             "city": "Zagreb",          "country": "Croatia",       "iata": "ZAG", "icao": "LDZA", "lat": 45.7429,  "lon": 16.0688,   "alt": 353,  "tz": "Europe/Zagreb"},
    {"name": "Kyiv Boryspil International Airport",      "city": "Kyiv",            "country": "Ukraine",       "iata": "KBP", "icao": "UKBB", "lat": 50.3450,  "lon": 30.8947,   "alt": 427,  "tz": "Europe/Kyiv"},
    # ── Russia & CIS (3) ──────────────────────────────────────────────────────
    {"name": "Sheremetyevo International Airport",       "city": "Moscow",          "country": "Russia",        "iata": "SVO", "icao": "UUEE", "lat": 55.9726,  "lon": 37.4146,   "alt": 630,  "tz": "Europe/Moscow"},
    {"name": "Domodedovo International Airport",         "city": "Moscow",          "country": "Russia",        "iata": "DME", "icao": "UUDD", "lat": 55.4103,  "lon": 37.9026,   "alt": 588,  "tz": "Europe/Moscow"},
    {"name": "Pulkovo Airport",                          "city": "Saint Petersburg","country": "Russia",        "iata": "LED", "icao": "ULLI", "lat": 59.8003,  "lon": 30.2625,   "alt": 78,   "tz": "Europe/Moscow"},
    # ── Turkey (2) ────────────────────────────────────────────────────────────
    {"name": "Istanbul Airport",                         "city": "Istanbul",        "country": "Turkey",        "iata": "IST", "icao": "LTFM", "lat": 41.2753,  "lon": 28.7519,   "alt": 325,  "tz": "Europe/Istanbul"},
    {"name": "Sabiha Gökçen International Airport",      "city": "Istanbul",        "country": "Turkey",        "iata": "SAW", "icao": "LTFJ", "lat": 40.8986,  "lon": 29.3092,   "alt": 312,  "tz": "Europe/Istanbul"},
    # ── Middle East (10) ──────────────────────────────────────────────────────
    {"name": "Dubai International Airport",              "city": "Dubai",           "country": "UAE",           "iata": "DXB", "icao": "OMDB", "lat": 25.2532,  "lon": 55.3657,   "alt": 62,   "tz": "Asia/Dubai"},
    {"name": "Al Maktoum International Airport",         "city": "Dubai",           "country": "UAE",           "iata": "DWC", "icao": "OMDW", "lat": 24.8963,  "lon": 55.1611,   "alt": 171,  "tz": "Asia/Dubai"},
    {"name": "Abu Dhabi International Airport",          "city": "Abu Dhabi",       "country": "UAE",           "iata": "AUH", "icao": "OMAA", "lat": 24.4330,  "lon": 54.6511,   "alt": 88,   "tz": "Asia/Dubai"},
    {"name": "Hamad International Airport",              "city": "Doha",            "country": "Qatar",         "iata": "DOH", "icao": "OTHH", "lat": 25.2731,  "lon": 51.6080,   "alt": 13,   "tz": "Asia/Qatar"},
    {"name": "King Abdulaziz International Airport",     "city": "Jeddah",          "country": "Saudi Arabia",  "iata": "JED", "icao": "OEJN", "lat": 21.6796,  "lon": 39.1565,   "alt": 48,   "tz": "Asia/Riyadh"},
    {"name": "King Khalid International Airport",        "city": "Riyadh",          "country": "Saudi Arabia",  "iata": "RUH", "icao": "OERK", "lat": 24.9576,  "lon": 46.6988,   "alt": 2049, "tz": "Asia/Riyadh"},
    {"name": "Kuwait International Airport",             "city": "Kuwait City",     "country": "Kuwait",        "iata": "KWI", "icao": "OKBK", "lat": 29.2267,  "lon": 47.9689,   "alt": 206,  "tz": "Asia/Kuwait"},
    {"name": "Bahrain International Airport",            "city": "Manama",          "country": "Bahrain",       "iata": "BAH", "icao": "OBBI", "lat": 26.2708,  "lon": 50.6336,   "alt": 6,    "tz": "Asia/Bahrain"},
    {"name": "Muscat International Airport",             "city": "Muscat",          "country": "Oman",          "iata": "MCT", "icao": "OOMS", "lat": 23.5933,  "lon": 58.2844,   "alt": 48,   "tz": "Asia/Muscat"},
    {"name": "Ben Gurion International Airport",         "city": "Tel Aviv",        "country": "Israel",        "iata": "TLV", "icao": "LLBG", "lat": 32.0114,  "lon": 34.8867,   "alt": 135,  "tz": "Asia/Jerusalem"},
    # ── Africa (12) ───────────────────────────────────────────────────────────
    {"name": "Cairo International Airport",              "city": "Cairo",           "country": "Egypt",         "iata": "CAI", "icao": "HECA", "lat": 30.1219,  "lon": 31.4056,   "alt": 382,  "tz": "Africa/Cairo"},
    {"name": "Addis Ababa Bole International Airport",   "city": "Addis Ababa",     "country": "Ethiopia",      "iata": "ADD", "icao": "HAAB", "lat": 8.9779,   "lon": 38.7993,   "alt": 7625, "tz": "Africa/Addis_Ababa"},
    {"name": "OR Tambo International Airport",           "city": "Johannesburg",    "country": "South Africa",  "iata": "JNB", "icao": "FAOR", "lat": -26.1367, "lon": 28.2411,   "alt": 5558, "tz": "Africa/Johannesburg"},
    {"name": "Cape Town International Airport",          "city": "Cape Town",       "country": "South Africa",  "iata": "CPT", "icao": "FACT", "lat": -33.9648, "lon": 18.6017,   "alt": 151,  "tz": "Africa/Johannesburg"},
    {"name": "Murtala Muhammed International Airport",   "city": "Lagos",           "country": "Nigeria",       "iata": "LOS", "icao": "DNMM", "lat": 6.5774,   "lon": 3.3214,    "alt": 135,  "tz": "Africa/Lagos"},
    {"name": "Mohammed V International Airport",         "city": "Casablanca",      "country": "Morocco",       "iata": "CMN", "icao": "GMMN", "lat": 33.3675,  "lon": -7.5900,   "alt": 656,  "tz": "Africa/Casablanca"},
    {"name": "Jomo Kenyatta International Airport",      "city": "Nairobi",         "country": "Kenya",         "iata": "NBO", "icao": "HKJK", "lat": -1.3192,  "lon": 36.9275,   "alt": 5327, "tz": "Africa/Nairobi"},
    {"name": "Kotoka International Airport",             "city": "Accra",           "country": "Ghana",         "iata": "ACC", "icao": "DGAA", "lat": 5.6052,   "lon": -0.1668,   "alt": 205,  "tz": "Africa/Accra"},
    {"name": "Julius Nyerere International Airport",     "city": "Dar es Salaam",   "country": "Tanzania",      "iata": "DAR", "icao": "HTDA", "lat": -6.8780,  "lon": 39.2026,   "alt": 182,  "tz": "Africa/Dar_es_Salaam"},
    {"name": "Houari Boumediene Airport",                "city": "Algiers",         "country": "Algeria",       "iata": "ALG", "icao": "DAAG", "lat": 36.6910,  "lon": 3.2154,    "alt": 827,  "tz": "Africa/Algiers"},
    {"name": "Tunis-Carthage International Airport",     "city": "Tunis",           "country": "Tunisia",       "iata": "TUN", "icao": "DTTA", "lat": 36.8510,  "lon": 10.2272,   "alt": 22,   "tz": "Africa/Tunis"},
    {"name": "Seychelles International Airport",         "city": "Mahé",            "country": "Seychelles",    "iata": "SEZ", "icao": "FSIA", "lat": -4.6743,  "lon": 55.5218,   "alt": 10,   "tz": "Indian/Mahe"},
    # ── South Asia (8) ────────────────────────────────────────────────────────
    {"name": "Indira Gandhi International Airport",      "city": "New Delhi",       "country": "India",         "iata": "DEL", "icao": "VIDP", "lat": 28.5562,  "lon": 77.1000,   "alt": 777,  "tz": "Asia/Kolkata"},
    {"name": "Chhatrapati Shivaji Maharaj Intl Airport", "city": "Mumbai",          "country": "India",         "iata": "BOM", "icao": "VABB", "lat": 19.0896,  "lon": 72.8656,   "alt": 37,   "tz": "Asia/Kolkata"},
    {"name": "Kempegowda International Airport",         "city": "Bangalore",       "country": "India",         "iata": "BLR", "icao": "VOBL", "lat": 13.1979,  "lon": 77.7063,   "alt": 3000, "tz": "Asia/Kolkata"},
    {"name": "Chennai International Airport",            "city": "Chennai",         "country": "India",         "iata": "MAA", "icao": "VOMM", "lat": 12.9900,  "lon": 80.1693,   "alt": 52,   "tz": "Asia/Kolkata"},
    {"name": "Kolkata Netaji Subhas Chandra Bose Intl",  "city": "Kolkata",         "country": "India",         "iata": "CCU", "icao": "VECC", "lat": 22.6547,  "lon": 88.4467,   "alt": 17,   "tz": "Asia/Kolkata"},
    {"name": "Hyderabad Rajiv Gandhi Intl Airport",      "city": "Hyderabad",       "country": "India",         "iata": "HYD", "icao": "VOHS", "lat": 17.2313,  "lon": 78.4298,   "alt": 1741, "tz": "Asia/Kolkata"},
    {"name": "Tribhuvan International Airport",          "city": "Kathmandu",       "country": "Nepal",         "iata": "KTM", "icao": "VNKT", "lat": 27.6966,  "lon": 85.3591,   "alt": 4390, "tz": "Asia/Kathmandu"},
    {"name": "Bandaranaike International Airport",       "city": "Colombo",         "country": "Sri Lanka",     "iata": "CMB", "icao": "VCBI", "lat": 7.1808,   "lon": 79.8841,   "alt": 30,   "tz": "Asia/Colombo"},
    # ── Central & East Asia (14) ──────────────────────────────────────────────
    {"name": "Beijing Capital International Airport",    "city": "Beijing",         "country": "China",         "iata": "PEK", "icao": "ZBAA", "lat": 40.0799,  "lon": 116.6031,  "alt": 116,  "tz": "Asia/Shanghai"},
    {"name": "Beijing Daxing International Airport",     "city": "Beijing",         "country": "China",         "iata": "PKX", "icao": "ZBAD", "lat": 39.5095,  "lon": 116.4105,  "alt": 98,   "tz": "Asia/Shanghai"},
    {"name": "Shanghai Pudong International Airport",    "city": "Shanghai",        "country": "China",         "iata": "PVG", "icao": "ZSPD", "lat": 31.1434,  "lon": 121.8052,  "alt": 13,   "tz": "Asia/Shanghai"},
    {"name": "Shanghai Hongqiao International Airport",  "city": "Shanghai",        "country": "China",         "iata": "SHA", "icao": "ZSSS", "lat": 31.1979,  "lon": 121.3363,  "alt": 10,   "tz": "Asia/Shanghai"},
    {"name": "Guangzhou Baiyun International Airport",   "city": "Guangzhou",       "country": "China",         "iata": "CAN", "icao": "ZGGG", "lat": 23.3924,  "lon": 113.2988,  "alt": 50,   "tz": "Asia/Shanghai"},
    {"name": "Shenzhen Bao'an International Airport",   "city": "Shenzhen",        "country": "China",         "iata": "SZX", "icao": "ZGSZ", "lat": 22.6393,  "lon": 113.8107,  "alt": 13,   "tz": "Asia/Shanghai"},
    {"name": "Chengdu Tianfu International Airport",     "city": "Chengdu",         "country": "China",         "iata": "TFU", "icao": "ZUTF", "lat": 30.3128,  "lon": 104.4441,  "alt": 1587, "tz": "Asia/Shanghai"},
    {"name": "Kunming Changshui International Airport",  "city": "Kunming",         "country": "China",         "iata": "KMG", "icao": "ZPPP", "lat": 24.9920,  "lon": 102.7433,  "alt": 6903, "tz": "Asia/Shanghai"},
    {"name": "Hong Kong International Airport",          "city": "Hong Kong",       "country": "China",         "iata": "HKG", "icao": "VHHH", "lat": 22.3080,  "lon": 113.9185,  "alt": 28,   "tz": "Asia/Hong_Kong"},
    {"name": "Tokyo Narita International Airport",       "city": "Tokyo",           "country": "Japan",         "iata": "NRT", "icao": "RJAA", "lat": 35.7720,  "lon": 140.3929,  "alt": 141,  "tz": "Asia/Tokyo"},
    {"name": "Tokyo Haneda Airport",                     "city": "Tokyo",           "country": "Japan",         "iata": "HND", "icao": "RJTT", "lat": 35.5494,  "lon": 139.7798,  "alt": 35,   "tz": "Asia/Tokyo"},
    {"name": "Osaka Kansai International Airport",       "city": "Osaka",           "country": "Japan",         "iata": "KIX", "icao": "RJBB", "lat": 34.4347,  "lon": 135.2440,  "alt": 26,   "tz": "Asia/Tokyo"},
    {"name": "Nagoya Chubu Centrair Intl Airport",       "city": "Nagoya",          "country": "Japan",         "iata": "NGO", "icao": "RJGG", "lat": 34.8583,  "lon": 136.8050,  "alt": 15,   "tz": "Asia/Tokyo"},
    {"name": "Incheon International Airport",            "city": "Seoul",           "country": "South Korea",   "iata": "ICN", "icao": "RKSI", "lat": 37.4602,  "lon": 126.4407,  "alt": 23,   "tz": "Asia/Seoul"},
    # ── Southeast Asia (10) ───────────────────────────────────────────────────
    {"name": "Singapore Changi Airport",                 "city": "Singapore",       "country": "Singapore",     "iata": "SIN", "icao": "WSSS", "lat": 1.3644,   "lon": 103.9915,  "alt": 22,   "tz": "Asia/Singapore"},
    {"name": "Suvarnabhumi Airport",                     "city": "Bangkok",         "country": "Thailand",      "iata": "BKK", "icao": "VTBS", "lat": 13.6900,  "lon": 100.7501,  "alt": 5,    "tz": "Asia/Bangkok"},
    {"name": "Don Mueang International Airport",         "city": "Bangkok",         "country": "Thailand",      "iata": "DMK", "icao": "VTBD", "lat": 13.9126,  "lon": 100.6067,  "alt": 9,    "tz": "Asia/Bangkok"},
    {"name": "Kuala Lumpur International Airport",       "city": "Kuala Lumpur",    "country": "Malaysia",      "iata": "KUL", "icao": "WMKK", "lat": 2.7456,   "lon": 101.7099,  "alt": 69,   "tz": "Asia/Kuala_Lumpur"},
    {"name": "Ngurah Rai International Airport",         "city": "Bali/Denpasar",   "country": "Indonesia",     "iata": "DPS", "icao": "WADD", "lat": -8.7482,  "lon": 115.1670,  "alt": 14,   "tz": "Asia/Makassar"},
    {"name": "Soekarno-Hatta International Airport",     "city": "Jakarta",         "country": "Indonesia",     "iata": "CGK", "icao": "WIII", "lat": -6.1256,  "lon": 106.6559,  "alt": 34,   "tz": "Asia/Jakarta"},
    {"name": "Ninoy Aquino International Airport",       "city": "Manila",          "country": "Philippines",   "iata": "MNL", "icao": "RPLL", "lat": 14.5086,  "lon": 121.0197,  "alt": 75,   "tz": "Asia/Manila"},
    {"name": "Mactan-Cebu International Airport",        "city": "Cebu",            "country": "Philippines",   "iata": "CEB", "icao": "RPVM", "lat": 10.3075,  "lon": 123.9789,  "alt": 31,   "tz": "Asia/Manila"},
    {"name": "Noi Bai International Airport",            "city": "Hanoi",           "country": "Vietnam",       "iata": "HAN", "icao": "VVNB", "lat": 21.2212,  "lon": 105.8072,  "alt": 39,   "tz": "Asia/Ho_Chi_Minh"},
    {"name": "Tan Son Nhat International Airport",       "city": "Ho Chi Minh City","country": "Vietnam",       "iata": "SGN", "icao": "VVTS", "lat": 10.8188,  "lon": 106.6520,  "alt": 33,   "tz": "Asia/Ho_Chi_Minh"},
    # ── Taiwan, Mongolia, Kazakhstan (3) ──────────────────────────────────────
    {"name": "Taiwan Taoyuan International Airport",     "city": "Taipei",          "country": "Taiwan",        "iata": "TPE", "icao": "RCTP", "lat": 25.0777,  "lon": 121.2328,  "alt": 106,  "tz": "Asia/Taipei"},
    {"name": "Almaty International Airport",             "city": "Almaty",          "country": "Kazakhstan",    "iata": "ALA", "icao": "UAAA", "lat": 43.3521,  "lon": 77.0405,   "alt": 2234, "tz": "Asia/Almaty"},
    {"name": "Nursultan Nazarbayev Intl Airport",        "city": "Astana",          "country": "Kazakhstan",    "iata": "NQZ", "icao": "UACC", "lat": 51.0223,  "lon": 71.4669,   "alt": 1165, "tz": "Asia/Almaty"},
    # ── Australia & Pacific (7) ───────────────────────────────────────────────
    {"name": "Sydney Kingsford Smith Airport",           "city": "Sydney",          "country": "Australia",     "iata": "SYD", "icao": "YSSY", "lat": -33.9399, "lon": 151.1753,  "alt": 21,   "tz": "Australia/Sydney"},
    {"name": "Melbourne Airport",                        "city": "Melbourne",       "country": "Australia",     "iata": "MEL", "icao": "YMML", "lat": -37.6733, "lon": 144.8430,  "alt": 434,  "tz": "Australia/Melbourne"},
    {"name": "Brisbane Airport",                         "city": "Brisbane",        "country": "Australia",     "iata": "BNE", "icao": "YBBN", "lat": -27.3842, "lon": 153.1175,  "alt": 13,   "tz": "Australia/Brisbane"},
    {"name": "Perth Airport",                            "city": "Perth",           "country": "Australia",     "iata": "PER", "icao": "YPPH", "lat": -31.9403, "lon": 115.9670,  "alt": 67,   "tz": "Australia/Perth"},
    {"name": "Adelaide Airport",                         "city": "Adelaide",        "country": "Australia",     "iata": "ADL", "icao": "YPAD", "lat": -34.9450, "lon": 138.5300,  "alt": 20,   "tz": "Australia/Adelaide"},
    {"name": "Auckland Airport",                         "city": "Auckland",        "country": "New Zealand",   "iata": "AKL", "icao": "NZAA", "lat": -37.0082, "lon": 174.7917,  "alt": 23,   "tz": "Pacific/Auckland"},
    {"name": "Christchurch Airport",                     "city": "Christchurch",    "country": "New Zealand",   "iata": "CHC", "icao": "NZCH", "lat": -43.4894, "lon": 172.5320,  "alt": 123,  "tz": "Pacific/Auckland"},
    # ── Additional United States (14) ─────────────────────────────────────────
    {"name": "Chicago Midway International Airport",     "city": "Chicago",         "country": "United States", "iata": "MDW", "icao": "KMDW", "lat": 41.7868,  "lon": -87.7522,  "alt": 620,  "tz": "America/Chicago"},
    {"name": "Fort Lauderdale-Hollywood Intl Airport",   "city": "Fort Lauderdale", "country": "United States", "iata": "FLL", "icao": "KFLL", "lat": 26.0726,  "lon": -80.1527,  "alt": 9,    "tz": "America/New_York"},
    {"name": "Sacramento International Airport",         "city": "Sacramento",      "country": "United States", "iata": "SMF", "icao": "KSMF", "lat": 38.6954,  "lon": -121.5908, "alt": 27,   "tz": "America/Los_Angeles"},
    {"name": "Oakland International Airport",            "city": "Oakland",         "country": "United States", "iata": "OAK", "icao": "KOAK", "lat": 37.7213,  "lon": -122.2208, "alt": 9,    "tz": "America/Los_Angeles"},
    {"name": "San Jose International Airport",           "city": "San Jose",        "country": "United States", "iata": "SJC", "icao": "KSJC", "lat": 37.3626,  "lon": -121.9290, "alt": 62,   "tz": "America/Los_Angeles"},
    {"name": "John Wayne Airport",                       "city": "Orange County",   "country": "United States", "iata": "SNA", "icao": "KSNA", "lat": 33.6757,  "lon": -117.8682, "alt": 56,   "tz": "America/Los_Angeles"},
    {"name": "Tucson International Airport",             "city": "Tucson",          "country": "United States", "iata": "TUS", "icao": "KTUS", "lat": 32.1161,  "lon": -110.9410, "alt": 2643, "tz": "America/Phoenix"},
    {"name": "Albuquerque International Sunport",        "city": "Albuquerque",     "country": "United States", "iata": "ABQ", "icao": "KABQ", "lat": 35.0402,  "lon": -106.6091, "alt": 5355, "tz": "America/Denver"},
    {"name": "El Paso International Airport",            "city": "El Paso",         "country": "United States", "iata": "ELP", "icao": "KELP", "lat": 31.8072,  "lon": -106.3779, "alt": 3959, "tz": "America/Denver"},
    {"name": "William P. Hobby Airport",                 "city": "Houston",         "country": "United States", "iata": "HOU", "icao": "KHOU", "lat": 29.6454,  "lon": -95.2789,  "alt": 46,   "tz": "America/Chicago"},
    {"name": "Memphis International Airport",            "city": "Memphis",         "country": "United States", "iata": "MEM", "icao": "KMEM", "lat": 35.0424,  "lon": -89.9767,  "alt": 341,  "tz": "America/Chicago"},
    {"name": "Cincinnati/Northern Kentucky Intl Airport","city": "Cincinnati",      "country": "United States", "iata": "CVG", "icao": "KCVG", "lat": 39.0488,  "lon": -84.6678,  "alt": 896,  "tz": "America/New_York"},
    {"name": "Cleveland Hopkins International Airport",  "city": "Cleveland",       "country": "United States", "iata": "CLE", "icao": "KCLE", "lat": 41.4117,  "lon": -81.8498,  "alt": 791,  "tz": "America/New_York"},
    {"name": "Bradley International Airport",            "city": "Hartford",        "country": "United States", "iata": "BDL", "icao": "KBDL", "lat": 41.9389,  "lon": -72.6832,  "alt": 174,  "tz": "America/New_York"},
    # ── Additional Europe (9) ─────────────────────────────────────────────────
    {"name": "Dusseldorf Airport",                       "city": "Dusseldorf",      "country": "Germany",       "iata": "DUS", "icao": "EDDL", "lat": 51.2895,  "lon": 6.7668,    "alt": 147,  "tz": "Europe/Berlin"},
    {"name": "Hamburg Airport",                          "city": "Hamburg",         "country": "Germany",       "iata": "HAM", "icao": "EDDH", "lat": 53.6304,  "lon": 9.9882,    "alt": 53,   "tz": "Europe/Berlin"},
    {"name": "Lyon Saint-Exupery Airport",               "city": "Lyon",            "country": "France",        "iata": "LYS", "icao": "LFLL", "lat": 45.7256,  "lon": 5.0811,    "alt": 821,  "tz": "Europe/Paris"},
    {"name": "Venice Marco Polo Airport",                "city": "Venice",          "country": "Italy",         "iata": "VCE", "icao": "LIPZ", "lat": 45.5053,  "lon": 12.3519,   "alt": 7,    "tz": "Europe/Rome"},
    {"name": "Naples International Airport",             "city": "Naples",          "country": "Italy",         "iata": "NAP", "icao": "LIRN", "lat": 40.8860,  "lon": 14.2908,   "alt": 294,  "tz": "Europe/Rome"},
    {"name": "Thessaloniki Macedonia Airport",           "city": "Thessaloniki",    "country": "Greece",        "iata": "SKG", "icao": "LGTS", "lat": 40.5197,  "lon": 22.9709,   "alt": 22,   "tz": "Europe/Athens"},
    {"name": "Riga International Airport",               "city": "Riga",            "country": "Latvia",        "iata": "RIX", "icao": "EVRA", "lat": 56.9236,  "lon": 23.9711,   "alt": 36,   "tz": "Europe/Riga"},
    {"name": "Vilnius Airport",                          "city": "Vilnius",         "country": "Lithuania",     "iata": "VNO", "icao": "EYVI", "lat": 54.6341,  "lon": 25.2858,   "alt": 197,  "tz": "Europe/Vilnius"},
    {"name": "Tallinn Airport",                          "city": "Tallinn",         "country": "Estonia",       "iata": "TLL", "icao": "EETN", "lat": 59.4133,  "lon": 24.8328,   "alt": 131,  "tz": "Europe/Tallinn"},
    # ── Additional Asia & Middle East (8) ─────────────────────────────────────
    {"name": "Fukuoka Airport",                          "city": "Fukuoka",         "country": "Japan",         "iata": "FUK", "icao": "RJFF", "lat": 33.5858,  "lon": 130.4511,  "alt": 32,   "tz": "Asia/Tokyo"},
    {"name": "Sapporo New Chitose Airport",              "city": "Sapporo",         "country": "Japan",         "iata": "CTS", "icao": "RJCC", "lat": 42.7752,  "lon": 141.6922,  "alt": 82,   "tz": "Asia/Tokyo"},
    {"name": "Gimpo International Airport",              "city": "Seoul",           "country": "South Korea",   "iata": "GMP", "icao": "RKSS", "lat": 37.5583,  "lon": 126.7906,  "alt": 59,   "tz": "Asia/Seoul"},
    {"name": "Lombok International Airport",             "city": "Lombok",          "country": "Indonesia",     "iata": "LOP", "icao": "WADL", "lat": -8.7573,  "lon": 116.2767,  "alt": 319,  "tz": "Asia/Makassar"},
    {"name": "Yangon International Airport",             "city": "Yangon",          "country": "Myanmar",       "iata": "RGN", "icao": "VYYY", "lat": 16.9073,  "lon": 96.1332,   "alt": 109,  "tz": "Asia/Rangoon"},
    {"name": "Phnom Penh International Airport",         "city": "Phnom Penh",      "country": "Cambodia",      "iata": "PNH", "icao": "VDPP", "lat": 11.5466,  "lon": 104.8440,  "alt": 40,   "tz": "Asia/Phnom_Penh"},
    {"name": "Vientiane Wattay International Airport",   "city": "Vientiane",       "country": "Laos",          "iata": "VTE", "icao": "VLVT", "lat": 17.9883,  "lon": 102.5633,  "alt": 564,  "tz": "Asia/Vientiane"},
    {"name": "Amman Queen Alia International Airport",   "city": "Amman",           "country": "Jordan",        "iata": "AMM", "icao": "OJAI", "lat": 31.7226,  "lon": 35.9932,   "alt": 2395, "tz": "Asia/Amman"},
    # ── Additional Africa (4) ─────────────────────────────────────────────────
    {"name": "Blaise Diagne International Airport",      "city": "Dakar",           "country": "Senegal",       "iata": "DSS", "icao": "GOBD", "lat": 14.6700,  "lon": -17.0730,  "alt": 90,   "tz": "Africa/Dakar"},
    {"name": "Abidjan Felix-Houphouet-Boigny Intl",      "city": "Abidjan",         "country": "Ivory Coast",   "iata": "ABJ", "icao": "DIAP", "lat": 5.2614,   "lon": -3.9263,   "alt": 21,   "tz": "Africa/Abidjan"},
    {"name": "Kigali International Airport",             "city": "Kigali",          "country": "Rwanda",        "iata": "KGL", "icao": "HRYR", "lat": -1.9686,  "lon": 30.1395,   "alt": 4859, "tz": "Africa/Kigali"},
    {"name": "Entebbe International Airport",            "city": "Entebbe",         "country": "Uganda",        "iata": "EBB", "icao": "HUEN", "lat": 0.0424,   "lon": 32.4435,   "alt": 3782, "tz": "Africa/Kampala"},
]

# ─────────────────────────────────────────────────────────────────────────────
# Indexes
# ─────────────────────────────────────────────────────────────────────────────
IATA_INDEX = {a["iata"].upper(): a for a in AIRPORTS}
ICAO_INDEX = {a["icao"].upper(): a for a in AIRPORTS}

# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
GREEN  = "\033[32m"
RED    = "\033[31m"
DIM    = "\033[2m"

def c(color, text):
    return f"{color}{text}{RESET}"

def fmt_airport(a, verbose=False):
    lines = []
    lines.append(c(BOLD + CYAN, f"\n  ✈  {a['name']}"))
    lines.append(f"  {'─' * 52}")
    lines.append(f"  {c(YELLOW, 'IATA:')}  {c(BOLD, a['iata'])}    {c(YELLOW, 'ICAO:')}  {c(BOLD, a['icao'])}")
    lines.append(f"  {c(YELLOW, 'City:')}  {a['city']},  {a['country']}")
    lines.append(f"  {c(YELLOW, 'Timezone:')}  {a['tz']}")
    lines.append(f"  {c(YELLOW, 'Coordinates:')}  {a['lat']:+.4f}°,  {a['lon']:+.4f}°")
    lines.append(f"  {c(YELLOW, 'Elevation:')}  {a['alt']:,} ft  ({int(a['alt'] * 0.3048):,} m)")
    lines.append("")
    return "\n".join(lines)

def fmt_airport_short(a):
    return (
        f"  {c(BOLD, a['iata'])} / {c(BOLD, a['icao'])}  "
        f"{a['name'][:42]:<42}  "
        f"{a['city']}, {a['country']}"
    )

# ─────────────────────────────────────────────────────────────────────────────
# Lookup logic
# ─────────────────────────────────────────────────────────────────────────────
def lookup(code):
    code = code.strip().upper()
    if code in IATA_INDEX:
        return IATA_INDEX[code], "IATA"
    if code in ICAO_INDEX:
        return ICAO_INDEX[code], "ICAO"
    return None, None

def search(query):
    q = query.lower()
    results = []
    for a in AIRPORTS:
        if (q in a["name"].lower()
                or q in a["city"].lower()
                or q in a["country"].lower()
                or q in a["iata"].lower()
                or q in a["icao"].lower()):
            results.append(a)
    return results

def list_country(country_query):
    q = country_query.lower()
    return [a for a in AIRPORTS if q in a["country"].lower()]

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def nearest(lat, lon, n=5):
    scored = sorted(AIRPORTS, key=lambda a: haversine_km(lat, lon, a["lat"], a["lon"]))
    return [(a, haversine_km(lat, lon, a["lat"], a["lon"])) for a in scored[:n]]

# ─────────────────────────────────────────────────────────────────────────────
# JSON export
# ─────────────────────────────────────────────────────────────────────────────
def to_dict(a):
    return {
        "name": a["name"],
        "city": a["city"],
        "country": a["country"],
        "iata": a["iata"],
        "icao": a["icao"],
        "latitude": a["lat"],
        "longitude": a["lon"],
        "elevation_ft": a["alt"],
        "timezone": a["tz"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def build_parser():
    p = argparse.ArgumentParser(
        prog="airport_lookup",
        description=(
            "✈  Airport Routing Code Lookup\n"
            "Supports IATA (e.g. LAX) and ICAO (e.g. KLAX) codes.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  airport_lookup LAX
  airport_lookup KLAX
  airport_lookup LAX JFK NRT
  airport_lookup --search london
  airport_lookup --list-country Japan
  airport_lookup --nearest 51.5 -0.12
  airport_lookup LAX --json
  airport_lookup --stats
        """,
    )
    p.add_argument(
        "codes",
        nargs="*",
        metavar="CODE",
        help="IATA or ICAO code(s) to look up",
    )
    p.add_argument(
        "--search", "-s",
        metavar="QUERY",
        help="Search airports by name, city, or country",
    )
    p.add_argument(
        "--list-country", "-l",
        metavar="COUNTRY",
        help="List all airports in a given country",
    )
    p.add_argument(
        "--nearest", "-n",
        nargs=2,
        metavar=("LAT", "LON"),
        type=float,
        help="Find the 5 nearest airports to given coordinates",
    )
    p.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON",
    )
    p.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics",
    )
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()

    # ── stats ─────────────────────────────────────────────────────────────────
    if args.stats:
        countries = sorted(set(a["country"] for a in AIRPORTS))
        print(c(BOLD + CYAN, f"\n  ✈  Airport Database Statistics"))
        print(f"  {'─' * 40}")
        print(f"  Total airports : {c(BOLD, str(len(AIRPORTS)))}")
        print(f"  Countries      : {c(BOLD, str(len(countries)))}")
        print(f"\n  Countries covered:")
        for co in countries:
            count = sum(1 for a in AIRPORTS if a["country"] == co)
            print(f"    {co:<30} {count} airport{'s' if count > 1 else ''}")
        print()
        return

    # ── nearest ───────────────────────────────────────────────────────────────
    if args.nearest:
        lat, lon = args.nearest
        results = nearest(lat, lon)
        if args.json:
            print(json.dumps([{**to_dict(a), "distance_km": round(d, 1)} for a, d in results], indent=2))
            return
        print(c(BOLD + CYAN, f"\n  ✈  5 Nearest Airports to ({lat:+.4f}, {lon:+.4f})"))
        print(f"  {'─' * 60}")
        for a, dist in results:
            print(f"  {c(BOLD, a['iata'])} / {c(BOLD, a['icao'])}  {c(GREEN, f'{dist:,.0f} km')}  "
                  f"{a['name'][:36]} — {a['city']}, {a['country']}")
        print()
        return

    # ── search ────────────────────────────────────────────────────────────────
    if args.search:
        results = search(args.search)
        if not results:
            print(c(RED, f"\n  No airports found matching '{args.search}'\n"))
            sys.exit(1)
        if args.json:
            print(json.dumps([to_dict(a) for a in results], indent=2))
            return
        print(c(BOLD + CYAN, f"\n  ✈  Search results for '{args.search}'  ({len(results)} found)"))
        print(f"  {'─' * 70}")
        for a in results:
            print(fmt_airport_short(a))
        print()
        return

    # ── list-country ──────────────────────────────────────────────────────────
    if args.list_country:
        results = list_country(args.list_country)
        if not results:
            print(c(RED, f"\n  No airports found for country '{args.list_country}'\n"))
            sys.exit(1)
        if args.json:
            print(json.dumps([to_dict(a) for a in results], indent=2))
            return
        label = results[0]["country"] if results else args.list_country
        print(c(BOLD + CYAN, f"\n  ✈  Airports in {label}  ({len(results)} found)"))
        print(f"  {'─' * 70}")
        for a in results:
            print(fmt_airport_short(a))
        print()
        return

    # ── code lookup ───────────────────────────────────────────────────────────
    if not args.codes:
        parser.print_help()
        return

    found, not_found = [], []
    for code in args.codes:
        a, kind = lookup(code)
        if a:
            found.append((a, kind))
        else:
            not_found.append(code)

    if args.json:
        print(json.dumps([to_dict(a) for a, _ in found], indent=2))
        if not_found:
            for code in not_found:
                sys.stderr.write(f"Not found: {code}\n")
        return

    for a, kind in found:
        print(fmt_airport(a))

    for code in not_found:
        print(c(RED, f"\n  ✗  '{code}' — code not found in database."))
        # suggest close IATA matches
        suggestions = [k for k in list(IATA_INDEX) + list(ICAO_INDEX)
                       if k.startswith(code[:2].upper())][:4]
        if suggestions:
            print(c(DIM, f"     Did you mean: {', '.join(suggestions)}?"))
        print()

    if not_found:
        sys.exit(1)


if __name__ == "__main__":
    main()