# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip white spaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value is not None and isinstance(value, str):
                adapter[field_name] = value.strip()

        # Lowercase 'category' and 'product_type'
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value is not None and isinstance(value, str):
                adapter[lowercase_key] = value.lower()

        # Convert 'price' to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None and isinstance(value, str):
                value = value.replace('£', '')
                try:
                    adapter[price_key] = float(value)
                except ValueError:
                    pass  # Handle invalid price values gracefully

        # Extract number of books in stock from 'availability'
        availability_tuple = adapter.get('availability')
        if availability_tuple and len(availability_tuple) > 0:
            availability_string = availability_tuple[0]
            split_string_array = availability_string.split('(')
            if len(split_string_array) >= 2:
                availability_array = split_string_array[1].split(' ')
                try:
                    adapter['availability'] = int(availability_array[0])
                except ValueError:
                    pass  # Handle invalid availability values gracefully

        # Extract and convert 'num_reviews' to integer
        num_reviews_tuple = adapter.get('num_reviews')
        if num_reviews_tuple and len(num_reviews_tuple) > 0:
            num_reviews_string = num_reviews_tuple[0]
            try:
                adapter['num_reviews'] = int(num_reviews_string)
            except ValueError:
                pass  # Handle invalid num_reviews values gracefully

        # Extract and convert 'stars' to number
        stars_tuple = adapter.get('stars')
        if stars_tuple and len(stars_tuple) > 0:
            stars_string = stars_tuple[0]
            split_stars_array = stars_string.split(' ')
            if len(split_stars_array) >= 2:
                stars_text_value = split_stars_array[1].lower()
                star_mapping = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
                adapter['stars'] = star_mapping.get(stars_text_value, -1)  # Default to -1 if not found

        return item


