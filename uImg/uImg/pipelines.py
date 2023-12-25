# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UimgPipeline:
    # 在爬蟲文件之前的執行方法
    def open_spider(self, spider):
        self.fp = open('uImg.json', 'w', encoding='utf-8')

    # 寫入文件
    def process_item(self, item, spider):
        self.fp.write(str(item)+',')
        return item

    # 在爬蟲文件之後執行的方法
    def close_spider(self, spider):
        self.fp.close()


import urllib.request


class UimgDownloadPipeline:
    def process_item(self, item, spider):
        # 需先去settings.py設定管道

        header = {  # 伪造浏览器头部
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        # 預設會在uimg下，路徑的資料夾必須先建好，不然會報錯
        urllib.request.urlretrieve(url=item.get('url'), filename='./images/' + item.get('name') + '.jpg')

        # url = item.get('url')
        # filename = './images/' + item.get('name')
        #
        # urllib.request.urlretrieve(url=url, filename=filename)
        return item
