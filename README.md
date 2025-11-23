# Prague Parking V2 (Continuous Delivery Example)

Detta repository innehåller version 2 av Prague Parking, implementerat som ett Python Flask API med en komplett CI/CD-pipeline (GitHub Actions).

Projektet är uppbyggt kring en OOP-kärna (Vehicle, ParkingSpot, ParkingGarage) som hanterar komplex parkering och prisberäkning, läser konfiguration från en JSON-fil, och testas via Pytest.

## ⚙️ CI/CD Status
| Pipeline | Status |
| :--- | :--- |
| **CI - Build and Test** | [![CI Status](https://github.com/Xanzy-pewpew/PragueParking_Final_Version/actions/workflows/ci.yml/badge.svg)](https://github.com/Xanzy-pewpew/PragueParking_Final_Version/actions/workflows/ci.yml) |
| **CD - Release Artifact** | [![CD Status](https://github.com/Xanzy-pewpew/PragueParking_Final_Version/actions/workflows/cd.yml/badge.svg)](https://github.com/Xanzy-pewpew/PragueParking_Final_Version/actions/workflows/cd.yml) |

## 🛠️ Lokalt Uppstart
1. Klona repositoryt.
2. Installera beroenden: `pip install -r requirements.txt`
3. Kör CLI-applikationen: `python cli.py`
4. Kör Pytest: `pytest`
