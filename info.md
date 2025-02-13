# Axeos Miner Integration

## Übersicht
Die Axeos Miner Integration ermöglicht es Benutzern, Daten von ihrem Axeos Miner über Home Assistant zu überwachen und zu steuern. Diese Integration nutzt die API des Axeos Miners, um wichtige Informationen wie Leistung, Spannung und Temperatur abzurufen.

## Installation
1. Stellen Sie sicher, dass Sie Home Assistant installiert haben.
2. Klonen Sie dieses Repository in das Verzeichnis `custom_components` Ihrer Home Assistant-Installation.
3. Starten Sie Home Assistant neu, um die Integration zu aktivieren.

## Konfiguration
Um die Axeos Miner Integration zu konfigurieren, fügen Sie die folgenden Zeilen zu Ihrer `configuration.yaml` hinzu:

```yaml
sensor:
  - platform: axeos_miner
    host: "http://IP"
```

Ersetzen Sie `http://IP` durch die IP-Adresse Ihres Axeos Miners.

## Häufige Probleme
- **API nicht erreichbar**: Stellen Sie sicher, dass die IP-Adresse korrekt ist und der Axeos Miner eingeschaltet ist.
- **Sensoren werden nicht angezeigt**: Überprüfen Sie die Home Assistant-Protokolle auf Fehler und stellen Sie sicher, dass die Integration korrekt installiert ist.

## Unterstützung
Für Unterstützung und Fragen besuchen Sie bitte das [Support-Forum](https://forum.home-assistant.io).