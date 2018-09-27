import scrapy
import re
import logging


class CommentSpider(scrapy.Spider):
    name = 'comment'
    comments_count = 0
    products_count = 0

    start_urls = [
        'http://digikala.com/',
    ]

    def parse(self, response):
        for href in response.css('.c-navi-new-list__sublist-option--item a'):
            yield response.follow(href, self.parse_categories)

    def parse_categories(self, response):
        for href in response.css('div.js-product-box a'):
            yield response.follow(href, self.parse_product)

        # follow pagination links
        for url in response.css('a.c-pager__item::attr(href)').extract():
            tokens = url.split('pageno=')
            if len(tokens) > 1:
                page_num = tokens[1]
                yield response.follow('?pageno={}'.format(page_num), self.parse_categories)

    def parse_product(self, response):
        def extract_with_css(query):
            res = response.css(query).extract_first()
            return res.strip() if res is not None else None
        res = re.search('(.*)dkp-(.*)/(.*)', response.url)
        id = res.group(2)
        comments_url = 'https://www.digikala.com/ajax/product/comments/{}/?mode=buyers'.format(id)
        comment_request = response.follow(comments_url, self.parse_comments)
        comment_request.meta['product_id'] = id
        comment_request.meta['title'] = extract_with_css('.c-product__title::text')
        comment_request.meta['category'] = extract_with_css('.c-product__directory li+ li .btn-link-spoiler::text')

        self.products_count += 1

        yield comment_request

    def parse_comments(self, response):
        comments = []
        adjective_selector = response.css('.c-comments__item-rating')
        adjectives_name_raw = adjective_selector.css('div.cell:nth-child(1)::text').extract()
        adjectives_name = [adj.strip().replace(':', '') for adj in adjectives_name_raw]
        adjectives_rate_raw = adjective_selector.css('div.js-rating-value::attr(data-rate-value)').extract()
        adjectives_rate = [(float(r.replace('%', '').strip())) / 100 for r in adjectives_rate_raw if r.strip() != '']

        product_rate = sum(adjectives_rate) / float(len(adjectives_rate)) if len(adjectives_rate) != 0 else None

        adjectives = []
        for adj_name, adj_rate in zip(adjectives_name, adjectives_rate):
            adjectives.append({
                adj_name: adj_rate
            })
        for comment_section in response.css('section'):
            comment_selector = comment_section.css('.article')
            pos_raw = comment_selector.css('.c-comments__evaluation-positive li::text').extract()
            pos = [x.strip() for x in pos_raw]
            neg_raw = comment_selector.css('.c-comments__evaluation-negative li::text').extract()
            neg = [x.strip() for x in neg_raw]
            txt = comment_selector.css('p::text').extract_first()
            txt = txt.strip() if txt is not None else None
            polarity = None
            if comment_section.css('.c-message-light--opinion-negative::text').extract_first() is not None:
                polarity = -1
            elif comment_section.css('.c-message-light--opinion-positive::text').extract_first() is not None:
                polarity = 1
            comments.append({
                'pol': polarity,
                'pos': pos,
                'neg': neg,
                'txt': txt
            })

        product_title_raw = response.css('h2.c-comments__headline span span:nth-child(1)::text').extract_first()
        product_title = product_title_raw.strip() if product_title_raw is not None else None

        self.comments_count += len(comments)
        logging.info('products count: {}, comments count: {}'.format(
            self.products_count, self.comments_count
        ))

        yield {
            'id': response.meta.get('product_id', None),
            't': response.meta.get('title', product_title),
            'c': response.meta.get('category', None),
            'r': response.meta.get('rate', product_rate),
            'adjs': response.meta.get('adjectives', adjectives),
            'cmts': comments
        }

        # follow pagination links
        for href in response.css('.c-pager__item'):
            comment_request = response.follow(href, self.parse_comments)
            comment_request.meta['product_id'] = response.meta.get('product_id', None)
            comment_request.meta['title'] = response.meta.get('title', product_title)
            comment_request.meta['category'] = response.meta.get('category', None)
            comment_request.meta['rate'] = product_rate
            comment_request.meta['adjectives'] = adjectives
            yield comment_request
