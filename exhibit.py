import streamlit as st
import streamlit.components.v1 as components 
from price_tagger import Add,Img2pdf
from glob import glob
import os
from PIL import Image,ImageDraw,ImageFont
import pandas as pd
import time
from PIL import Image
import cv2
import numpy as np
import ddddocr
st.set_page_config('价签生成器',page_icon = '💰')
tab1,tab4,tab3 = st.tabs(['价签生成','价签内部查询','文字生成',])


def get_res(text):
    add = Add()
    add.get_text(text
                 # file_name = 'test.png'
                 )
def remove():
    filedir = os.path.dirname(__file__)+'/results/*'
    for i in glob(filedir):
        st.write('正在删除……')
        st.write(i)
        os.remove(i)


with st.sidebar:
    files = glob('results/*')
    if files:
        st.write('文件夹含有不相关早期内容，请及时清理。')
        st.write(files)
        st.button('清空已有文件', on_click=remove)

    else:
        st.sidebar.write('结果文件夹为空，请放心使用')

with tab1:
    def generate(name='',spec='',area='',cata='',unit=''):
        name = st.text_input('名称',value=name,key='name'+name+str(time.time()))
        if len(spec)<1:
            spec_key = 'spec'+spec+name+str(time.time())
        else:
            spec_key = 'spec'+spec+name
        spec = st.text_input('规格',value=spec,key=spec_key)
        if len(area)>5:
            new_area = area[:2]
            area_key = 'area' + area+name
        else:
            new_area = area
            area_key = 'area' + area+str(time.time())+name
        area = st.text_input('产地',value=new_area,key=area_key,placeholder=area)
        cata = st.text_input('货号',value=cata,key='cata'+cata+str(time.time()))
        if len(unit)<1:
            unit_key = 'unit'+unit+str(time.time())+name
        else:
            unit_key = 'unit'+unit+name
        unit = st.text_input('单位',value=unit,key=unit_key)
        price = st.number_input('价格',format='%f',min_value=0.0,key='price'+name)
        text = [name,spec,area,cata,unit,price]


        if st.button('生成',key='shengcheng'+name):
            get_res(text)
            img_list = glob('results/*.png')
            for i in img_list:
                if i.endswith('png'):
                    st.image(i)
        if st.button('合成pdf文件',key='hecheng'+name):
            img_list = glob('results/*.png')
            img2pdf = Img2pdf(img_list)
            img2pdf.save_pdf()
        pdf = st.selectbox('选择需要下载的pdf文件',glob('results/*.pdf'),key='xiazai'+name)

        try:
            with open(pdf,'rb') as file:
                st.download_button(
                label = '下载合并后的pdf文件',
                    data =  file,
                    file_name="dowloaded.pdf",
                    mime = 'application/octet-stream')
        except:
            pass


    generate(name='',spec='',area='',cata='',unit='')

with tab3:
    ch_text = st.text_input('文字',value = '中药饮片')
    text_color = st.color_picker('文字颜色','#00FFAA')
    bg_color = st.color_picker('背景颜色','#00f900')
    zxk_color = st.color_picker('矩形框颜色','#000')
    font_size = st.slider('字体大小',20,100,80)
    w,h = 400,200
    x,y = 40,40
    img = Image.new('RGB',(w,h),'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle((x,y,w-x,h-y),fill = bg_color,outline = zxk_color)
    size = font_size
    font = ImageFont.truetype('font/SimHei.ttf',size)
   
    draw.text(((w-len(ch_text)*size)/2,(h-size)/2),ch_text,fill = text_color,font = font)
    img.save('test.png')
    st.image('test.png')



        # Check the type of cv2_img:
        # Should output: <class 'numpy.ndarray'>
        # st.write(type(cv2_img))

        # Check the shape of cv2_img:
        # Should output shape: (height, width, channels)
        # st.write(cv2_img.shape)



        
with tab4:
    ## 库存搜索功能
    @st.cache_resource
    def get_data():
        data = pd.read_csv('产品数据全量.csv',index_col = 0,keep_default_na=0)
        data = data.drop_duplicates(subset=['货号','通用名'])
        return data
    data = get_data()
    if 'info' not in st.session_state:
        st.session_state.info={'通用名':'',
                               "规格":'',
                               '生产厂家':'',
                               '单位':'',
                               }

    def get_text_info(text):
        name_df = data[data['通用名'].map(lambda x:True if text and text.lower() in x.lower() else False)]
        code = data[data['货号'].map(lambda x:True if text and str(text).lower() in str(x).lower() else False)]
        return name_df.merge(code,how='outer')
    
    with st.form('搜索🔍'):
        text = st.text_input('请输入商品名或条码：')
        print(text)
        info = get_text_info(text)
        # st.dataframe(info)
        if st.form_submit_button('搜索',):
            st.dataframe(info)
        if len(info) == 1:
            info = info.T.to_dict()[0]
            st.session_state.info = info
    if st.session_state.info['通用名']:
        generate(name=st.session_state.info['通用名'], spec=st.session_state.info['规格'], area=st.session_state.info['生产厂家'], cata='', unit=st.session_state.info['单位'])
        
    
