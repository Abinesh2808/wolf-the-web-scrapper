# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from dotenv import load_dotenv
import mysql.connector


class QuotesPipeline:
    def __init__(self):
        load_dotenv()
        self.connection = None
        self.cursor = None
        self.create_connection()
        self.create_table()

    def create_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USERNAME"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )
            self.cursor = self.connection.cursor()
        return self.connection, self.cursor

    def create_table(self):
        try:
            self.connection.start_transaction()

            # cursor.execute(""" drop table if exists quotes """)
            self.cursor.execute(""" create table if not exists quotes (
                                    id int auto_increment primary key,
                                    title text,
                                    author text,
                                    tags text,
                                    is_deleted enum('yes', 'no') default 'no',
                                    created_at timestamp default current_timestamp,
                                    updated_at timestamp default current_timestamp on update current_timestamp
                                ) 
                            """)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        finally:
            self.close_connection()

    def insert_data(self, data):
        try:
            self.create_connection()
            self.connection.start_transaction()
            self.cursor.execute("""insert into quotes (title,author,tags) values (%s, %s, %s)""", (data['title'], data['author'], data['tags']))

            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        finally:
            self.close_connection()

    def process_item(self, item, spider):
        data = {}
        data['title'] = item['title'][0]
        data['author'] = item['author'][0]
        data['tags'] = item['tags'][0]
        self.insert_data(data)
        return item

    def close_connection(self):
        self.cursor.close()
        self.connection.close()