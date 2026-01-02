#!/usr/bin/env python3
import requests
import random

def get_random_star_alliance_flight(include_ground=True):
    """Star Alliance flights LIVE - OpenSky uniquement (AUCUN RATE LIMIT)"""
    # Focus Europe (où Lufthansa vole le plus)
    # params = {
    #    'lamin': 35, 'lomin': -10,  # Europe Sud-Ouest
    #    'lamax': 60, 'lomax': 25    # Europe Nord-Est
    # }
    
    resp = requests.get("https://opensky-network.org/api/states/all", """params=params""")
    states = resp.json()['states']
    
    # TOUS les vols Star Alliance détectés
    star_flights = []
    for state in states:
        callsign = state[1]
        if callsign and callsign.startswith(('DLH', 'LHG', 'BEL', 'AEE', 'ACA', 'CCA', 'AIC', 'ANZ', 'ANA', 'AAR', 'AUA', 'AVA', 'TPU', 'CMP', 'CTN', 'MSR', 'ETH', 'EVA', 'LOT', 'CSZ', 'SIN', 'SAA', 'SWR', 'TAP', 'THA', 'THY', 'UAL')):  # DLH + sector callsigns
            onground = bool(state[8])
            if include_ground or not onground:
                star_flights.append({
                    'callsign': callsign.strip(),
                    'icao24': state[0],
                    'lat': state[6],
                    'lon': state[5],
                    'altitude': state[7] or 0,
                    'speed': state[9] or 0,
                    'onground': onground,
                    'status': "🛬 AU SOL" if onground else "✈️ EN VOL"
                })
    
    if star_flights:
        flight = random.choice(star_flights)
        return {
            'callsign': flight['callsign'],  # DLH463 ou DLH8HP
            'status': flight['status'],
            'position': f"{round(flight['lat'], 4)}, {round(flight['lon'], 4)}",
            'altitude_ft': int(flight['altitude'] * 3.28084),
            'speed_kts': int(flight['speed'] * 1.94384),
            'trackers': [
                f"Voir le vol en direct : https://globe.adsb.fi/?icao={flight['icao24']}",
            ]
        }
    return None

def print_flight(flight):
    if not flight:
        print("❌ Aucun vol Lufthansa détecté (essaie plus tard)")
        return
    
    print(f"\n✈️  VOL {flight['callsign']} {flight['status']}")
    print(f"\n Généré par OpenSky Network - https://opensky-network.org/")
    print(f"   📍 {flight['position']}")
    print(f"   🏔️  {flight['altitude_ft']} ft | ⚡ {flight['speed_kts']} kts")
    print("   🔗", flight['trackers'][0])

# LANCEMENT
if __name__ == "__main__":
    print("🔍 Recherche vols Star Alliance...\n")
    
    # Test au sol
    flight2 = get_random_star_alliance_flight(include_ground=True)
    print_flight(flight2)
