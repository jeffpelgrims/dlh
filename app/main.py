#!/usr/bin/env python3
import requests
import random

def get_random_lufthansa_flight(include_ground=True):
    """Lufthansa flights LIVE - OpenSky uniquement (AUCUN RATE LIMIT)"""
    # Focus Europe (où Lufthansa vole le plus)
    params = {
        'lamin': 35, 'lomin': -10,  # Europe Sud-Ouest
        'lamax': 60, 'lomax': 25    # Europe Nord-Est
    }
    
    resp = requests.get("https://opensky-network.org/api/states/all", params=params)
    states = resp.json()['states']
    
    # TOUS les vols Lufthansa détectés
    dlh_flights = []
    for state in states:
        callsign = state[1]
        if callsign and callsign.startswith(('DLH', 'LHG')):  # DLH + sector callsigns
            onground = bool(state[8])
            if include_ground or not onground:
                dlh_flights.append({
                    'callsign': callsign.strip(),
                    'icao24': state[0],
                    'lat': state[6],
                    'lon': state[5],
                    'altitude': state[7] or 0,
                    'speed': state[9] or 0,
                    'onground': onground,
                    'status': "🛬 AU SOL" if onground else "✈️ EN VOL"
                })
    
    if dlh_flights:
        flight = random.choice(dlh_flights)
        return {
            'callsign': flight['callsign'],  # DLH463 ou DLH8HP
            'status': flight['status'],
            'position': f"{round(flight['lat'], 4)}, {round(flight['lon'], 4)}",
            'altitude_ft': int(flight['altitude'] * 3.28084),
            'speed_kts': int(flight['speed'] * 1.94384),
            'trackers': [
                f"https://globe.adsb.fi/?icao={flight['icao24']}",
                f"https://www.flightradar24.com/data/aircraft/{flight['icao24']}"
            ]
        }
    return None

def print_flight(flight):
    if not flight:
        print("❌ Aucun vol Lufthansa détecté (essaie plus tard)")
        return
    
    print(f"\n✈️  LUFTHANSA {flight['callsign']} {flight['status']}")
    print(f"   📍 {flight['position']}")
    print(f"   🏔️  {flight['altitude_ft']} ft | ⚡ {flight['speed_kts']} kts")
    print("   🔗", flight['trackers'][0])
    print("   🔗", flight['trackers'][1])

# LANCEMENT
if __name__ == "__main__":
    print("🔍 Recherche vols Lufthansa...\n")
    
    # Test au sol
    flight2 = get_random_lufthansa_flight(include_ground=True)
    print_flight(flight2)
