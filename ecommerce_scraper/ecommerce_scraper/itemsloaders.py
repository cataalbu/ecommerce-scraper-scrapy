from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class SSREcommerceProductLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: float(x[1:]))
    rating_in = MapCompose(lambda x: int(x.split(" ")[0]))


class CSREcommerceProductLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: float(x[1:]))
    rating_in = MapCompose(lambda x: int(x.split(" ")[0]))