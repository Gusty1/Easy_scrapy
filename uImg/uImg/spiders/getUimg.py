import scrapy
import uuid
# 這邊會錯是正常現象，可以不管
from uImg.items import UimgItem

class GetuimgSpider(scrapy.Spider):
    name = "getUimg"
    allowed_domains = ["www.wallpaperflare.com"]
    # start_urls = ["https://www.wallpaperflare.com"]

    # hololive橫版圖
    # start_urls = ["https://www.wallpaperflare.com/search?wallpaper=hololive&width=1920&height=1080&page=1"]
    # base_url = 'https://www.wallpaperflare.com/search?wallpaper=hololive&width=1920&height=1080&page='

    # 動漫女孩手機圖
    # start_urls = ["https://www.wallpaperflare.com/search?wallpaper=anime+girl&mobile=ok&page=1"]
    # base_url = 'https://www.wallpaperflare.com/search?wallpaper=anime+girl&mobile=ok&page='

    # cosplay手機圖
    start_urls = ["https://www.wallpaperflare.com/search?wallpaper=women+cosplay+asian&mobile=ok&page=1"]
    base_url = 'https://www.wallpaperflare.com/search?wallpaper=women+cosplay+asian&mobile=ok&page='

    url_list = []
    page = 0

    def parse(self, response):
        for page in range(1, 2):
            url = self.base_url + str(page)
            self.page = self.page + 1
            yield scrapy.Request(url=url, callback=self.parse_page)

    # 頁數網址
    def parse_page(self, response):
        xpath_list = response.xpath('//li/figure/a')
        for img in xpath_list:
            # 詳細頁的網址
            detailHref = img.xpath('@href').extract_first()
            # 圖片寬度
            # imgWidth = img.xpath('img/@width').extract_first()
            # 圖片長度
            # imgHeight = img.xpath('img/@height').extract_first()
            # 如果要取橫圖高>寬就跳過
            # if imgHeight > imgWidth or imgHeight == imgWidth:
            #     continue
            # yield scrapy.Request(url=detailHref, callback=self.parse_detail,meta={'name':''})
            # 取得預覽圖
            meta = {
                "previewUrl": img.xpath('img/@data-src').extract_first()
            }
            # 因為後面沒辦法取得預覽圖了，但後面又需要寫入json，所以這邊把他往傳遞
            yield scrapy.Request(url=detailHref, callback=self.parse_detail, meta=meta)

    # 詳細頁網頁
    def parse_detail(self, response):
        # response.xpath('//div[@class=item_left]/img')
        # 前往完整圖片的網址
        href = response.xpath('//div[@class="item_left"]/a/@href').extract_first()
        yield scrapy.Request(url=href, callback=self.parse_full, meta=response.meta)

    # 完整圖片網頁
    def parse_full(self, response):
        url = response.xpath('//section/img/@src').extract_first()
        previewUrl = response.meta['previewUrl']

        # 下載檔案需要名字
        # uimg = UimgItem(url=url, previewUrl=previewUrl,name=str(uuid.uuid4()))

        # 不知為啥回傳總有重複的值，所以就是找最後一個obj
        # self.url_list.append(url)
        # if self.page >= 5:
        uimg = UimgItem(url=url, previewUrl=previewUrl)
        yield uimg
