# digikala-crawler

[![HitCount](http://hits.dwyl.io/rajabzz/digikala-crawler.svg)](http://hits.dwyl.io/rajabzz/digikala-crawler)
[![Maintainability](https://api.codeclimate.com/v1/badges/8ec7c2370e5823d0a025/maintainability)](https://codeclimate.com/github/rajabzz/digikala-crawler/maintainability)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

>🕷️ A crawler to collect comments and product information on digikala.com

## Installation
Install `Python` and `pip`. Then:

```bash
$ git clone https://github.com/rajabzz/digikala-crawler.git
$ cd digikala-crawler
$ pip install -r requirements.txt
```

## Running The Crawler
The following command runs the `comment` spider and saves the output in `results.jl`.
```bash
$ scrapy crawl comment -o results.jl 
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

