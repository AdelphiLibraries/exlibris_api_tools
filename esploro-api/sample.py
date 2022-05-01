import esploro_api as esp


# Set to "DEV" to use sandbox API key per config.ini.
esp.MODE = "DEV"

res_file_path = "output/dev/esploro_researchers_DEV.json"
x = esp.get_researchers()
esp.save_json(x, res_file_path)
esp.output_researchers(res_file_path, dir="output/dev")


asset_file_path = "output/dev/esploro_assets_DEV.json"
y = esp.get_assets()
esp.save_json(y, asset_file_path)

esp.MODE = "PROD"
z = esp.get_organizations()
print(z)
