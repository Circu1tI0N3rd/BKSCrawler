'''
EXCEPTION DEFINITION FILE FOR CRAWLER
'''
class CrawlerError(Exception):
    def __init__(self, args, nil=None):
        self.args = args
        self.Reduced = nil
        super(CrawlerError, self).__init__(args)