class DebugPipeline:
    def process_item(self, item, spider):
        spider.logger.info(f"Got item: {item}")
        return item
