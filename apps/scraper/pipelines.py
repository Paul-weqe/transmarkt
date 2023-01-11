
class TeamPipeline(object):
    def process_item(self, item, spider):
        print("." * 50)
        print("#" * 50)
        item.save()
        return item
