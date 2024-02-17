import asyncio
from spy_crawler import SPY

async def main():
    app = SPY(proxy='http://169.254.1.1:8080')

    await app.paginate(
        'https://www.terabyteshop.com.br',
        '.dep__pop a::attr(href)',
        concat=True
    )
    await app.get_all()
    app.get_items_group('.pbox',{
        'product_name': 'h2::text',
        'product_link': 'a::attr(href)',
        'product_price': '.prod-new-price span::text'
    }).to_markdown('dataframe.md')

asyncio.run(main())
