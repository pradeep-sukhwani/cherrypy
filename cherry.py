import cherrypy
import urlparse
from jinja2 import Environment, FileSystemLoader
import os.path
from datetime import datetime
import unicodecsv as csv

env = Environment(loader=FileSystemLoader('templates'))


class Stock(object):
    def index(self):
        getParams  = urlparse.parse_qs(cherrypy.request.query_string)
        print getParams
        stock_dict = {}
        with open("EQ190118.CSV") as stock_data:
            csv_reader = csv.reader(stock_data)
            for count, row in enumerate(csv_reader):
                if count == 0:
                    continue
                if count == 11:
                    break
                my_list = [row[0], row[4], row[5], row[6], row[7]]
                stock_dict.update({row[1]: my_list})
            # import ipdb; ipdb.set_trace()
            if cherrypy.request.method == "GET":
                stock_name = cherrypy.request.params.get("search_stock")
                if stock_name:
                    stock_dict = stock_dict[str(stock_name)]
        template = env.get_template('index.html')
        return template.render(date=datetime.today().strftime("%d-%m-%y"), stock=stock_dict)
    index.exposed = True

config_file = os.path.join(os.path.dirname(__file__), 'server.conf')

cherrypy.quickstart(Stock(), config=config_file)
