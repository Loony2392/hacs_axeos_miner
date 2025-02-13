# Axeos Miner Integration for Home Assistant

This project provides an integration for the Axeos Miner, allowing users to monitor and manage their mining operations through Home Assistant. The integration fetches data from the Axeos Miner API and presents it as sensors within Home Assistant.

## Features

- Real-time monitoring of mining performance
- Access to various metrics such as power consumption, voltage, and temperature
- Easy integration with Home Assistant

## Installation

1. Clone this repository to your Home Assistant `custom_components` directory:
   ```
   git clone https://github.com/yourusername/axeos_miner_integration.git
   ```

2. Restart Home Assistant to load the new integration.

3. Configure the integration in your `configuration.yaml` file:
   ```yaml
   sensor:
     - platform: axeos_miner
       host: "http://IP"
   ```

## Usage

Once the integration is installed and configured, you will be able to see the Axeos Miner sensors in your Home Assistant dashboard. You can use these sensors to monitor the performance and health of your mining operations.

## Troubleshooting

If you encounter any issues, please refer to the `info.md` file for common problems and solutions.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.