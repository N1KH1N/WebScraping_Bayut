import scrapy

class WiskeySpider(scrapy.Spider):
    name = 'reaver'
    start_urls=['https://www.bayut.com/to-rent/property/dubai/']
    max_properties =3600

    def __init__(self, *args, **kwargs):
        super(WiskeySpider, self).__init__(*args, **kwargs)
        self.property_count = 0

    def parse(self,response):
        property_urls=response.xpath('//a[contains(@class, "_287661cb")]/@href').getall()

        for url in property_urls:
            yield response.follow(url,callback=self.infoparse_)
            self.property_count += 1

        if self.property_count >= self.max_properties:
            return

        next_page = response.css('[title="Next"]::attr(href)').get()
        if next_page is not None and self.property_count < self.max_properties:
            next_url = 'https://www.bayut.com' + next_page
            yield response.follow(next_url, callback=self.parse)


    def infoparse_(self,response):
        for plot in response.xpath('//div[contains(@class, "_6803f627")]'):
            for plott in response.xpath('.//div[contains(@class, "_607ecfd5") and contains(@class, "_3532643f")]'):
                    for bread in response.xpath('.//div[contains(@class, "_74ac503e")]'):
                        for pc in response.xpath('.//div[contains(@class, "_31cc6dcd")]'):

                                yield {
                                        'property_id': plot.xpath('//span[@class="_812aa185"]/text()')[2].getall(),
                                        'purpose':plot.xpath('//span[@class="_812aa185"]/text()').getall()[1],
                                        'type':plot.xpath('//span[@class="_812aa185"]/text()').getall()[0],
                                        'added_on':plot.xpath('//span[@class="_812aa185"]/text()').getall()[5],
                                        'furnishing':plot.xpath('//span[@class="_812aa185"]/text()').getall()[3],
                                        'price':{'currency':plot.xpath('//span[@class="e63a6bfb"]/text()').get(),
                                                    'amount':plot.xpath('//span[@class="_105b8a67"]/text()').get()},
                                        'location' : plot.xpath('//div[@class="_1f0f1758"]/text()').get(),
                                        'bed_bath_size':{"bedrooms":plot.xpath('//span[@class="fc2d1086"]/text()')[0].get(),
                                                        "bathrooms":plot.xpath('//span[@class="fc2d1086"]/text()')[1].get(),
                                                        "size": plot.xpath('.//span[@class="fc2d1086"]/span[1]/text()').get(),},
                                        'agent_name':plott.xpath('//a[@class="f730f8e6"]/text()').get(),
                                        'image_url': pc.xpath('//div[contains(@class, "_31cc6dcd")]//img/@src').get(default=''),
                                        'breadcrumbs':bread.xpath('//span[@class="_327a3afc"]/text()').getall(),
                                        'amenities':plot.xpath('//span[@class="_005a682a"]/text()').getall(),
                                        'description':plot.xpath('//span[@class="_2a806e1e"]/text()').getall()
                                    }