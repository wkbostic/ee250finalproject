from icrawler.builtin import BingImageCrawler

# Find positive images
classes=['red solo cup'] 
number=200
for c in classes:
    bing_crawler=BingImageCrawler(storage={'root_dir':f'p/{c.replace(" ",".")}'})
    bing_crawler.crawl(keyword=c,filters=None,max_num=number,offset=0)

# Find negative images
classes=['trees','roads','Human faces', 'red ball', 'red shirt']
number=500
for c in classes:
    bing_crawler2=BingImageCrawler(storage={'root_dir':f'n/{c.replace(" ",".")}'})
    bing_crawler2.crawl(keyword=c,filters=None,max_num=number,offset=0)