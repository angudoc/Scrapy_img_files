import scrapy

class UnsplashImage(scrapy.Item):
    image_url = scrapy.Field()    # URL изображения
    title = scrapy.Field()        # Название изображения
    category = scrapy.Field()     # Категория изображения
    image_path = scrapy.Field()   # Локальный путь после загрузки

# Соблюдаем правила robots.txt
ROBOTSTXT_OBEY = True

# User-Agent для идентификации
USER_AGENT = 'unsplash_scraper (+http://example.com)'

# Задержка между запросами
DOWNLOAD_DELAY = 1  # в секундах

# Настройка ImagesPipeline
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
}

# Путь для сохранения изображений
IMAGES_STORE = 'images'

