#!/usr/bin/env python

import scrapy
from scrapy.crawler import CrawlerProcess
import configparser
import os, sys, pkgutil, importlib

#from spiders.wikipedia_spider import WikipediaSpider
#from spiders import wikipedia_spider

from language import Language

languages = [
    Language('sah', 'Sakha', 'https://en.wikipedia.org/wiki/Yakut_language'),
    Language('nrf', 'Jèrriais', 'https://en.wikipedia.org/wiki/J%C3%A8rriais'),
    Language('qwe', 'Quechua', 'https://en.wikipedia.org/wiki/Quechuan_languages'),
    Language('nys', 'Nyungar', 'https://en.wikipedia.org/wiki/Nyungar_language'),
    Language('xho', 'Xhosa', 'https://en.wikipedia.org/wiki/Xhosa_language'),
    Language('dak', 'Sioux', 'https://en.wikipedia.org/wiki/Sioux_language')
]

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.jl": {
                "format": "jl"
            }
        }
    }
)

def process_site(site_tuple):
    root_url = config[site_tuple[1]]['root']
    site_language_pages = config[site_tuple[1]]['site_language_pages']
    site_language_pages_items = config.items(site_language_pages)
    site_languages = [] 
    for site_lang_page_item in site_language_pages_items:
        site_languages.append(Language(config['language_codes'][site_lang_page_item[0]], site_lang_page_item[0], config[site_tuple[1]]['root'] + site_lang_page_item[1]))
    
    tree = os.listdir('wikitongues/wikitongues/spiders')

    for t in tree:
        if t.__contains__(site_tuple[0]):
            myClass = getattr(importlib.import_module('spiders.' + t[:-3]), config['spiders'][site_tuple[0]])
            process.crawl(myClass, site_languages)
            process.start()
            

    
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', 'indexing.cfg'))
sites = config.items('sites')
#start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')
start_all_crawls = 'y'
if start_all_crawls.lower() == 'n':
    site_to_crawl = input('Which site would you like to crawl? ')
    for site in sites:
        if site_to_crawl == site[0]:
            process_site(site_to_crawl)
            break
    print('Invalid input: could not find a site that matched your input')
        
elif start_all_crawls.lower() == 'y':
    for site in sites:
        process_site(site)
        print(site[1])

else:
    print('invalid input')

    
#crawl all websites
print(sites)
print("Yer, this is cool!")

#process.crawl(WikipediaSpider, languages)

#process.start()
