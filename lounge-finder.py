import argparse

<<<<<<< HEAD
# 2026 Global Lounge Database: Final Consolidated Edition
# Includes: Asia-Pac, Business Darlings, US West Coast, LH Group, Med & Africa
LOUNGE_DATA = {
    # --- ASIA-PACIFIC & BUSINESS DARLINGS ---
    "HND": {
        "Star Alliance Gold": [
            {"name": "ANA Suite Lounge", "term": "T2 & T3", "sub_term": "International", "showers": True, "premium_food": True, "guests": True, "day_pass": False},
            {"name": "ANA Lounge", "term": "T2 & T3", "sub_term": "International", "showers": True, "premium_food": False, "guests": True, "day_pass": True}
        ],
        "Oneworld Emerald": [{"name": "JAL First Class Lounge", "term": "T3", "sub_term": "International", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Oneworld Sapphire": [
            {"name": "JAL Sakura Lounge", "term": "T3", "sub_term": "International", "showers": True, "premium_food": False, "guests": True, "day_pass": False},
            {"name": "Cathay Pacific Lounge", "term": "T3", "sub_term": "Level 6", "showers": False, "premium_food": True, "guests": True, "day_pass": False}
        ],
        "SkyTeam Elite Plus": [{"name": "Delta Sky Club", "term": "T3", "sub_term": "International", "showers": True, "premium_food": True, "guests": True, "day_pass": False}]
    },
    "PEK": {
        "Oneworld Emerald/Sapphire": [{"name": "Cathay Pacific Lounge (New Flagship)", "term": "T3E", "sub_term": "Near Gate E20", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Star Alliance Gold": [{"name": "Air China First/Business Class", "term": "T3E", "sub_term": "International", "showers": True, "premium_food": True, "guests": True, "day_pass": False}]
    },
    "GMP": {
        "Star Alliance Gold": [{"name": "Asiana Lounge", "term": "Intl", "sub_term": "3F (Near Gate 34)", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "SkyTeam Elite Plus": [{"name": "Korean Air KAL Lounge", "term": "Intl", "sub_term": "4F", "showers": False, "premium_food": True, "guests": True, "day_pass": False}]
    },
    "TSA": {
        "Alliance Shared": [{"name": "Airlines VIP Lounge", "term": "T1", "sub_term": "Post-Security", "showers": False, "premium_food": True, "guests": True, "day_pass": False}],
        "Independent": [{"name": "Plaza Premium Lounge (New 2025)", "term": "T1", "sub_term": "International", "showers": False, "premium_food": True, "guests": True, "day_pass": True}]
    },
    "SHA": {
        "SkyTeam Elite Plus": [{"name": "China Eastern V01 Lounge", "term": "T1", "sub_term": "4th Floor", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Star Alliance Gold": [{"name": "Air China V02 Lounge", "term": "T1", "sub_term": "4th Floor", "showers": True, "premium_food": True, "guests": True, "day_pass": False}]
    },
    "LCY": {
        "Independent/Credit": [{"name": "Juniper & Co. (Dining Credit)", "term": "Main", "sub_term": "East Pier", "showers": False, "premium_food": True, "guests": True, "day_pass": True}]
    },

    # --- EUROPE & LH GROUP (Audited 2026) ---
    "BRU": {
        "Star Alliance Gold/Business": [
            {"name": "Pop-up LOFT (Temporary)", "term": "Pier A", "sub_term": "Near Gate A27", "showers": False, "premium_food": True, "guests": True, "day_pass": False},
            {"name": "Sunrise Lounge", "term": "Pier A", "sub_term": "End of Pier", "showers": True, "premium_food": True, "guests": True, "day_pass": False}
        ]
    },
    "VIE": {
        "Star Alliance Gold": [{"name": "Austrian Senator Lounge", "term": "T3", "sub_term": "F/G Gates", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Independent": [{"name": "VIENNA Lounge", "term": "T1", "sub_term": "Post-Security", "showers": True, "premium_food": True, "guests": True, "day_pass": True}]
    },
    "LUX": {
        "LH Group / Luxair Business": [{"name": "Luxair Business Lounge", "term": "Main", "sub_term": "Near B-Gates", "showers": False, "premium_food": True, "guests": True, "day_pass": True}]
    },
    "ZRH": {
        "Star Alliance Gold": [{"name": "SWISS Senator Lounge", "term": "Dock E", "sub_term": "Flagship w/ Terrace", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Star Alliance Business": [{"name": "SWISS Business Lounge", "term": "Dock A", "sub_term": "28m Bar", "showers": True, "premium_food": True, "guests": False, "day_pass": True}]
    },

    # --- MEDITERRANEAN & AFRICA ---
    "FCO": {
        "Star Alliance Gold / SkyTeam": [{"name": "Piazza di Spagna (ITA)", "term": "T3", "sub_term": "Gate E", "showers": True, "premium_food": True, "guests": True, "day_pass": True}],
        "Star Alliance Gold": [{"name": "Star Alliance Lounge FCO", "term": "T3", "sub_term": "Gate D", "showers": True, "premium_food": True, "guests": True, "day_pass": False}]
    },
    "IST": {
        "Star Alliance Gold": [{"name": "Turkish Airlines Business Lounge", "term": "Intl", "sub_term": "Near Gate E1", "showers": True, "premium_food": True, "guests": False, "day_pass": False}],
        "Independent": [{"name": "iGA Lounge (With Terrace)", "term": "Intl", "sub_term": "Mezzanine", "showers": True, "premium_food": True, "guests": True, "day_pass": True}]
    },
    "JNB": {
        "Star Alliance Gold": [{"name": "SAA Platinum Lounge", "term": "Intl A", "sub_term": "Duty Free", "showers": True, "premium_food": True, "guests": True, "day_pass": False}],
        "Oneworld Sapphire": [{"name": "Slow Lounge", "term": "Intl", "sub_term": "Near Gate A2", "showers": True, "premium_food": True, "guests": True, "day_pass": True}]
    },

    # --- US WEST COAST ---
    "SFO": {
        "Star Alliance Gold": [{"name": "United Polaris", "term": "Intl G", "sub_term": "Long-haul", "showers": True, "premium_food": True, "guests": False, "day_pass": False}],
        "Independent": [{"name": "The Club SFO", "term": "T1", "sub_term": "Concourse B", "showers": True, "premium_food": True, "guests": True, "day_pass": True}]
    },
    "LAX": {
        "Star Alliance Gold": [{"name": "Star Alliance Lounge (TBIT)", "term": "TBIT", "sub_term": "Level 6", "showers": True, "premium_food": True, "guests": True, "day_pass": True}],
        "Oneworld Emerald": [{"name": "Qantas First Lounge", "term": "TBIT", "sub_term": "Level 5", "showers": True, "premium_food": True, "guests": True, "day_pass": False}]
    }
}

# Regional and Country Mapping for Country-Wide Searches
LOUNGE_BY_COUNTRY = {
    "JAPAN": ["HND", "NRT"],
    "SOUTH KOREA": ["ICN", "GMP"],
    "TAIWAN": ["TPE", "TSA"],
    "CHINA": ["PEK", "SHA", "PVG", "HKG"],
    "GERMANY": ["FRA", "MUC", "BER"],
    "SWITZERLAND": ["ZRH", "GVA"],
    "USA": ["SFO", "LAX", "SJC", "SNA", "JFK"],
    "UK": ["LHR", "LCY"]
}

ALERTS = {
    "HND": "ℹ️ ANA shower reservations (Jan 2026) are managed via the ANA App.",
    "BRU": "🚨 THE LOFT is CLOSED until late Summer 2026. Use the Pop-up LOFT (A27) or Sunrise Lounge.",
    "LCY": "ℹ️ No private lounges exist. Priority Pass/Amex users get an £18 credit at Juniper & Co.",
    "TSA": "✨ NEW: Plaza Premium TSA (opened March 2025) is the first independent lounge here.",
    "FCO": "🇮🇹 ITA Airways lounges now fully support Lufthansa Miles & More status following the merger.",
    "SFO": "✨ The Club SFO (T1) features a Lululemon 'Mindful Room' for pre-flight stretching.",
    "IST": "✨ The iGA Lounge features the terminal's only outdoor fresh-air terrace.",
    "PEK": "✨ NEW: Cathay Pacific Flagship (T3E) features a Noodle Bar and Teahouse as of Aug 2025."
}

def display_lounges(airport_code, alliance_filter=None, showers_only=False, daypass_only=False):
    code = airport_code.upper()
    if code not in LOUNGE_DATA:
        print(f"\n❌ Error: {code} data missing or not yet audited for 2026.")
=======
# Comprehensive 2026 Lounge Database (Updated with Tokyo)
LOUNGE_DATA = {
    "HND": {
        "Star Alliance Gold": ["ANA Suite Lounge (T2 & T3)", "ANA Lounge (T2 & T3)"],
        "Oneworld Emerald": ["JAL First Class Lounge (T3)"],
        "Oneworld Sapphire": ["JAL Sakura Lounge (T3)", "Cathay Pacific Lounge (T3 - Level 6)"],
        "SkyTeam Elite Plus": ["Delta Sky Club (T3 - Flagship with Noodle Bar)", "TIAT Lounge (Contract for other SkyTeam)"]
    },
    "NRT": {
        "Star Alliance Gold": ["ANA Suite Lounge (T1 Satellite 5)", "ANA Lounge (T1 Satellite 2 & 5)", "United Club (T1 Satellite 3)"],
        "Oneworld Emerald": ["JAL First Class Lounge (T2)"],
        "Oneworld Sapphire": ["JAL Sakura Lounge (T2)", "Cathay Pacific First & Business Class Lounge (T2)"],
        "SkyTeam Elite Plus": ["Korean Air KAL Lounge (T1)", "China Airlines Dynasty Lounge (T2)"]
    },
    "LHR": {
        "Star Alliance Gold": ["United Club (T2)", "Lufthansa Senator Lounge (T2)", "Singapore SilverKris (T2)", "Air Canada Maple Leaf Lounge (T2)"],
        "Oneworld Emerald": ["Cathay Pacific First Class Lounge (T3)", "British Airways First Lounge (T5/T3)", "American Airlines First Class Lounge (T3)"],
        "Oneworld Sapphire": ["Cathay Pacific Business Lounge (T3)", "Qantas London Lounge (T3)", "BA Galleries Club (T5/T3)", "American Admirals Club (T3)"],
        "SkyTeam Elite Plus": ["Virgin Atlantic Clubhouse (T3 - Access for DL/VS/AF/KL)", "SkyTeam Lounge (T4)"]
    },
    "SIN": {
        "Star Alliance Gold": ["KrisFlyer Gold Lounge (T2/T3)", "SilverKris Lounge (Business Class section)"],
        "Oneworld Emerald": ["Qantas First Lounge (T1)", "Cathay Pacific Lounge (T4)"],
        "Oneworld Sapphire": ["Qantas Business Lounge (T1)", "British Airways Lounge (T1)"],
        "SkyTeam Elite Plus": ["Marhaba Lounge (T1/T3)", "SATS Premier Lounge (T2)"]
    },
    "JFK": {
        "Star Alliance Gold": ["Lufthansa Senator Lounge (T1)", "Turkish Airlines Lounge (T1)", "Air India Maharaja Lounge (T4)"],
        "Oneworld Emerald": ["Soho Lounge (T8)", "Chelsea Lounge (T8)"],
        "Oneworld Sapphire": ["Greenwich Lounge (T8)", "British Airways Galleries (T8)"],
        "SkyTeam Elite Plus": ["Delta Sky Club (T4)", "Virgin Atlantic Clubhouse (T4)", "Air France Lounge (T1)"]
    },
    "FRA": {
        "Star Alliance Gold": ["Lufthansa Senator Lounges (T1 - A, B, Z)", "Air Canada Maple Leaf Lounge (T1B)"],
        "Oneworld Emerald": ["JAL First Class Lounge (T2)", "Cathay Pacific Lounge (T2)"],
        "SkyTeam Elite Plus": ["New SkyTeam Flagship Lounge (T3 - Opening April 2026!)", "Air France/KLM Lounge (T2)"]
    },
    "HKG": {
        "Star Alliance Gold": ["Singapore SilverKris Lounge (T1)", "United Club (T1)"],
        "Oneworld Emerald": ["The Pier, First (Near Gate 63)", "The Deck (Interim Emerald Lounge)"],
        "Oneworld Sapphire": ["The Pier, Business", "The Qantas Hong Kong Lounge", "The Bridge"],
        "SkyTeam Elite Plus": ["SkyTeam Exclusive Lounge (Gate 15)"]
    },
    "SYD": {
        "Star Alliance Gold": ["Air New Zealand Lounge (T1)", "Singapore SilverKris (T1)"],
        "Oneworld Emerald": ["Qantas International First Lounge (T1)"],
        "Oneworld Sapphire": ["Qantas Business (Temp space near G24 during 2026 reno)"],
        "SkyTeam Elite Plus": ["SkyTeam Exclusive Lounge (T1 Pier B)"]
    },
    "DOH": {
        "Oneworld Emerald": ["Qatar Airways Platinum Lounge South", "Al Safwa First (Ticketed First Only)"],
        "Oneworld Sapphire": ["Qatar Airways Gold Lounge South", "Al Mourjan Business (Ticketed J Only)"],
        "Star Alliance Gold": ["Al Maha Lounge (Contract)"]
    },
    "ICN": {
        "SkyTeam Elite Plus": ["Korean Air Prestige Lounge (T2)", "Korean Air First Lounge (T2)"],
        "Oneworld Emerald/Sapphire": ["oneworld Branded Lounge (T1 Gate 28)"],
        "Star Alliance Gold": ["Asiana Business Lounge (T1 - Check merger status for T2 move)"]
    }
}

# 2026 Operational Alerts
ALERTS = {
    "HND": "ℹ️ ANA (Star Alliance) updated its shower reservation system (Jan 2026). Use the ANA App to book.",
    "FRA": "⚠️ Terminal 3 opens April 2026. SkyTeam operations moving from T2 to T3.",
    "ICN": "⚠️ Asiana (Star Alliance) merger into Korean Air (SkyTeam) is nearing completion; expect T1 gate changes.",
    "SYD": "⚠️ Qantas Business Lounge reno continues. Follow signs for 'Temporary Lounge' near Gate 24.",
    "HKG": "⚠️ 'The Wing' First Class remains closed for renovation. Use 'The Deck' for Emerald access."
}

def display_lounges(airport_code, alliance_filter=None):
    code = airport_code.upper()
    if code not in LOUNGE_DATA:
        print(f"\n❌ Error: {code} data missing.")
>>>>>>> d8d74b7121e0d97d34f3108cdeb6337831a5fe0a
        return

    print(f"\n--- ✈️ 2026 LOUNGE ACCESS: {code} ---")
    if code in ALERTS: print(f"\n{ALERTS[code]}")

    found_any = False
    for tier, lounges in LOUNGE_DATA[code].items():
        if alliance_filter and alliance_filter.lower() not in tier.lower():
            continue
<<<<<<< HEAD
        
        filtered = [l for l in lounges if 
                    (not showers_only or l["showers"]) and
                    (not daypass_only or l["day_pass"])]

        if filtered:
            found_any = True
            print(f"\n🔹 {tier}")
            for l in filtered:
                s_icon = "🚿" if l["showers"] else "❌"
                f_icon = "🍽️" if l["premium_food"] else "🥪"
                g_icon = "👤+1" if l["guests"] else "👤"
                p_icon = "💳 $" if l["day_pass"] else "🔒"
                print(f"  - {l['name']} [{l['term']} | {l['sub_term']}]")
                print(f"    [ Showers: {s_icon} | Dining: {f_icon} | Guests: {g_icon} | Day Pass: {p_icon} ]")

    if not found_any:
        print("\nNo lounges match your current 2026 filters.")

def display_country_lounges(country, alliance_filter=None):
    country_key = country.upper()
    if country_key not in LOUNGE_BY_COUNTRY:
        print(f"\n❌ Error: No data for country: {country}")
        return

    print(f"\n--- 🌏 2026 COUNTRY-WIDE LOUNGES: {country_key} ---")
    for airport_code in LOUNGE_BY_COUNTRY[country_key]:
        display_lounges(airport_code, alliance_filter)

def main():
    parser = argparse.ArgumentParser(description="2026 Global & Country Lounge Finder")
    parser.add_argument("-a", "--airport", help="3-letter IATA code (e.g. HND, BRU, SFO)")
    parser.add_argument("-c", "--country", help="List all lounges in a country (e.g. Japan, Germany, USA)")
    parser.add_argument("-f", "--alliance", help="Filter by alliance (Star, Oneworld, SkyTeam, Independent)")
    parser.add_argument("-s", "--showers", action="store_true", help="Show only with showers")
    parser.add_argument("-d", "--daypass", action="store_true", help="Show only with day pass access")
    
    args = parser.parse_args()

    if args.country:
        display_country_lounges(args.country, args.alliance)
    elif args.airport:
        display_lounges(args.airport, args.alliance, args.showers, args.daypass)
    else:
        print("Please specify an --airport or a --country.")
=======
        found_any = True
        print(f"\n🔹 {tier}")
        for lounge in lounges:
            print(f"  - {lounge}")

def main():
    parser = argparse.ArgumentParser(description="2026 Global Alliance Lounge Finder")
    parser.add_argument("airport", help="3-letter IATA code (e.g. HND, NRT, LHR)")
    parser.add_argument("-a", "--alliance", help="Filter by alliance (Star, Oneworld, SkyTeam)")
    args = parser.parse_args()
    display_lounges(args.airport, args.alliance)
>>>>>>> d8d74b7121e0d97d34f3108cdeb6337831a5fe0a

if __name__ == "__main__":
    main()