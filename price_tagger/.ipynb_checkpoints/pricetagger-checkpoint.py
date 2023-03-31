import pandas as pd
from PIL import Image,ImageDraw,ImageShow,ImageFont
from tqdm import tqdm
import time 
import os
base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Add():
    def __init__(self,image_path = f'{base_path}/tag_image/001.png'):
        self.image_path = image_path
        self.img = Image.open(image_path, mode = 'r')
        self.draw = ImageDraw.Draw(self.img)
        
#         coordinate_dict = {
#         'name':,
#             'area':,
#         'cata':,
#             'unit':,
#             'spec':,
#             'price':,
        
#         }
 
        
    def text(self,xy,name,fontsize,font_file = None):
        if font_file is None:
            self.font = ImageFont.truetype(f'{base_path}/font/SimHei.ttf', fontsize)
        else:
            self.font = ImageFont.truetype(font_file, fontsize)
        return self.draw.text(xy,name,font = self.font,fill='black')
    
    def get_name(self,name):
        
        assert name is not None
        if len(name) <= 10: 
            return self.text((90,56),name,40)
        elif len(name) >15:
            return self.text((85,58),name,24)
        else:
            return self.text((88,58),name,30)
        
    def get_area(self,area):
       
        return self.text((94,130),str(area),22)
    def get_cata(self,cata):
        
        return self.text((75,191),str(cata),20)
    def get_unit(self,unit):
        
        return self.text((184,191),str(unit),22)
    def get_spec(self,spec):
        
        if len(spec) < 10 :
            return self.text((290,120),spec,22)
        elif len(spec) < 20 :
            return self.text((287,122),spec,20)
        elif len(spec) < 30 :
            return self.text((287,125),spec,15)
        else:
            #字符数30及以上的不计入
            return ''
            # spec_list =spec.split('、')
            # for i,s in enumerate(spec_list):
            #     self.text((287,120+i*15),s,15)
    def get_price(self,price):
        price = float(price)
        return self.text((300,200),"%.2f"%price,60)
    def save(self,file_name):
        self.img.save(file_name)
        self.img.close()
    def get_text(self,text,file_name = None,have_cata = False):
        '''
        text:[名称，规格，产地，货号，单位，价格]
        
        '''
        self.__init__(self.image_path)
        name,spec,area,cata,unit,price = text
        if pd.isna(name):
            name = ''
        if pd.isna(spec):
            spec = ''
        if pd.isna(area):
            area = ''
        if pd.isna(cata):
            cata = ''
        if pd.isna(unit):
            unit = ''
        if pd.isna(price):
            price = ''
        self.get_name(name)
        if pd.isna(have_cata):
            cata = ''
        
        self.get_area(area)
        self.get_cata(cata)
        self.get_unit(unit)
        self.get_spec(spec)
        self.get_price(price)
        if not file_name:
            file_name = f'{base_path}/results/{name}.{time.asctime(time.localtime(time.time()))}.png'
        self.save(file_name)
        
        
        
    
    
        
        