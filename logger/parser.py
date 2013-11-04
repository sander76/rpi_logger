'''
Created on 27 aug. 2013

@author: Teunissen-S
'''


class Parser():
    def __init__(self):
        pass

    def parse(self, dict_to_parse):
        if dict_to_parse['status'] == 'error':
            return '{},{},error {}'.format(dict_to_parse['tm'],
                                        dict_to_parse['time'],
                                        dict_to_parse['data'])
        elif dict_to_parse['status'] == 'ok':
            value = dict_to_parse['data'][-4:]
            return '{},{},{},{}'.format(dict_to_parse['tm'],
                                        dict_to_parse['time'],
                                        value,
                                        dict_to_parse['data'])
