#-*- encoding: utf-8 -*-
from my_yaml import MyYAML


class TestYAML(object):
    def __init__(self):
        self.my_ini = MyYAML()
        
    def get_ini(self):
        print self.my_ini.get_ini()['usefulkkdd']
        
    def set_ini(self):
        data = self.my_ini.get_ini()
        data['usefulkkdd'] = ['789', '456', '123', 'user']
        print self.my_ini.set_ini(data)

if __name__ == "__main__":
    ty = TestYAML()
    ty.get_ini()
    #ty.set_ini()
    #ty.set_ini()
