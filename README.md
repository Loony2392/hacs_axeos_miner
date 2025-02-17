# ![AxeOS Miner](logo_256x256.png) AxeOS Miner Integration for Home Assistant

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Loony2392/hacs_axeos_miner)](https://github.com/Loony2392/hacs_axeos_miner/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![GitHub issues](https://img.shields.io/github/issues/Loony2392/hacs_axeos_miner)](https://github.com/Loony2392/hacs_axeos_miner/issues)
[![GitHub license](https://img.shields.io/github/license/Loony2392/hacs_axeos_miner)](https://github.com/Loony2392/hacs_axeos_miner/blob/main/LICENSE)

This project provides an integration for the AxeOS Miner, allowing users to monitor and manage their mining operations through Home Assistant. The integration fetches data from the AxeOS Miner API and presents it as sensors within Home Assistant.

## Features

- 📊 **Real-time monitoring** of mining performance
- ⚡ **Access to various metrics** such as power consumption, voltage, and temperature
- 🛠️ **Easy integration** with Home Assistant

## Installation

### HACS (Home Assistant Community Store)

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Loony2392&repository=hacs_axeos_miner&category=integration)

1. Go to HACS in your Home Assistant instance.
2. Click on **Integrations**.
3. Click on the **+ Explore & Download Repositories** button.
4. Search for "AxeOS Miner" and install the integration.
5. Restart Home Assistant to load the new integration.

### Manual Installation

1. Clone this repository to your Home Assistant `custom_components` directory:
   ```sh
   git clone https://github.com/Loony2392/hacs_axeos_miner.git
   ```

2. Restart Home Assistant to load the new integration.

3. Configure the integration in your `configuration.yaml` file:
   ```yaml
   sensor:
     - platform: axeos_miner
       host: "http://IP"
   ```

## Usage

Once the integration is installed and configured, you will be able to see the AxeOS Miner sensors in your Home Assistant dashboard. You can use these sensors to monitor the performance and health of your mining operations.

## Troubleshooting

If you encounter any issues, please refer to the `info.md` file for common problems and solutions.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.