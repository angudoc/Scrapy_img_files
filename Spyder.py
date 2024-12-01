import scrapy
from unsplash_scraper.items import UnsplashImage

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ['https://unsplash.com/sitemap/categories']

    def parse(self, response):
        # Извлекаем ссылки на категории
        categories = response.css('a[href*="/t/"]::attr(href)').getall()
        for category in categories:
            category_url = response.urljoin(category)
            category_name = category.split("/")[-1]
            yield scrapy.Request(
                category_url,
                callback=self.parse_category,
                meta={'category': category_name}
            )

    def parse_category(self, response):
        category = response.meta['category']
        # Извлекаем ссылки на фотографии
        photo_links = response.css('figure a::attr(href)').getall()
        for photo in photo_links:
            photo_url = response.urljoin(photo)
            yield scrapy.Request(
                photo_url,
                callback=self.parse_photo,
                meta={'category': category}
            )

        # Переход на следующую страницу
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_category,
                meta={'category': category}
            )

    def parse_photo(self, response):
        category = response.meta['category']
        title = response.css('h1::text').get() or "Untitled"
        image_url = response.css('img[src*="photo-"]::attr(src)').get()

        if image_url:
            yield UnsplashImage(
                image_url=image_url,
                title=title.strip(),
                category=category
            )
