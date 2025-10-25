from itemadapter import ItemAdapter


class IPCheckerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        spider.logger.info(f"Changed IP address: {adapter['ip']}")
        return item
