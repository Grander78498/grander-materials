import xml.etree.ElementTree as ET

xml_data = ET.parse('data.xml')
result_json = []

for item in xml_data.findall('item'):
    item_values = {'motion': None, 'sound_level': None, 'illuminance': None, 'temperature': None, 'file_time': None, 'case_id': None}
    for key in item_values:
        item_values[key] = item.find(key).text
    result_json.append(item_values)
print(result_json)