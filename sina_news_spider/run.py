import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

s = get_project_settings()

with open("config") as f:
    config_json = f.read()
    config_obj = json.loads(config_json)

config_dict = config_obj['configs']

# config_dict['LOG_FILE'] = config_obj['logPath']
# config_dict['IMAGES_STORE'] = config_obj['filePath']

for key, value in config_dict.items():
    value = value.strip()
    if value == "True":
        config_dict[key] = True
    elif value == "False":
        config_dict[key] = False
    elif value.isdigit():
        config_dict[key] = int(value)

s.update(config_dict)

process = CrawlerProcess(s)
process.crawl(config_obj['name'], **s)
process.start()
