# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy import spiderloader


def run_all_spiders():
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='info.logs',
        format='%(asctime)s - %(levelname)s :: %(message)s',
        level=logging.DEBUG
    )


    settings = get_project_settings()
    process = CrawlerProcess(settings)
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    for spider_name in spider_loader.list():
        logging.debug(f"Running spider {spider_name}")
        process.crawl(spider_loader.load(spider_name))
    process.start()

if __name__ == "__main__":
    run_all_spiders()
