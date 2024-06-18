import json

# Open the file for reading with UTF-8 encoding
with open("convert_temperature.json", encoding="utf-8") as f:
  data = json.load(f)

# Open the file for writing with UTF-8 encoding
with open("convert_temperature.json", "w", encoding="utf-8") as d:
  json.dump(data, d, ensure_ascii=False, indent=4)