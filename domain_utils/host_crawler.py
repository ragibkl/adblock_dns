#!python3
import requests
from datetime import datetime


# hosts file line filter methods
def is_not_comment(line):
    if line.startswith('#'):
        return False
    return True


def is_valid_length(line):
    if len(line) == 0:
        return False
    line_parts = line.split(' ')

    return len(line_parts) >= 2


def does_not_contains_invalid_chars(line):
    invalid_strings = [ 'localhost', '_' ]
    if any( s in line for s in invalid_strings ):
        return False

    return True


def starts_with_local_ip(line):
    localhosts = [ '0.0.0.0 ', '127.0.0.1 ' ]
    return any( line.startswith(host) for host in localhosts )


class HostCrawler:
    """Crawler class, to crawl the http source for the adblock list"""
    filters = [
        is_not_comment,
        is_valid_length,
        does_not_contains_invalid_chars,
        starts_with_local_ip,
    ]

    @classmethod
    def remove_duplicates(cls, domain_list):
        before_count = len(domain_list)
        print('Before del duplicates, row count = {}'.format(before_count))

        dedup_list = list(set(domain_list))
        after_count = len(dedup_list)
        print('After de-duplicate, row count = {}'.format(after_count))

        return dedup_list

    def __init__(self, source):
        self.source = source

    def get_domains(self):
        lines = self.fetch_list()
        filtered_lines = [ line for line in lines if self.is_line_valid(line) ]
        domain_names = [ self.get_domain_name(line) for line in filtered_lines ]

        return domain_names

    def fetch_list(self):
        print('Started downloading from : {}'.format(self.source))
        response = requests.get(self.source)
        openfile = str(response.content, 'UTF-8')
        lines = openfile.replace('\r','').split('\n')
        lines = [ line.replace('\t', ' ') for line in lines ]
        return lines

    def get_domain_name(self, line):
        string_parts = line.split(' ')
        return string_parts[1].encode("idna").decode('ascii')

    def is_line_valid(self, line):
        try:
            for filter_func in self.filters:
                if not filter_func(line):
                    print('Validation failed: [{}], line: "{}"'.format(filter_func.__name__, line))
                    return False
        except Exception as e:
            print('Exception in source: "{}", reason: {}, line: "{}", '.format(self.source, e, line))
            return False

        return True
