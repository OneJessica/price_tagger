import streamlit as st
from price_tagger import Add,Img2pdf
from glob import glob
import os
from PIL import Image,ImageDraw,ImageFont

st.set_page_config('价签生成器',page_icon = '💰')
tab1,tab2 = st.tabs(['价签生成','文字生成'])
with tab1:
    name = st.text_input('名称')
    spec = st.text_input('规格')
    area = st.text_input('产地')
    cata = st.text_input('货号')
    unit = st.text_input('单位')
    price = st.number_input('价格',format='%f',)
    text = [name,spec,area,cata,unit,price]

    def get_res(text):
        add = Add()
        add.get_text(text 
                     # file_name = 'test.png'
                    )
    if st.button('生成'):
        get_res(text)
        img_list = glob('results/*.png')
        for i in img_list:
            if i.endswith('png'):
                st.image(i)
    if st.button('合成pdf文件'):
        img_list = glob('results/*.png')
        img2pdf = Img2pdf(img_list)
        img2pdf.save_pdf()
    pdf = st.selectbox('选择需要下载的pdf文件',glob('results/*.pdf'))
    try:
        with open(pdf,'rb') as file: 
            st.download_button(
            label = '下载合并后的pdf文件',
                data =  file,
                file_name="dowloaded.pdf",
                mime = 'application/octet-stream')
    except:
        pass
with tab2:
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


def remove():
    filedir = os.path.dirname(__file__)+'/results/*'
    for i in glob(filedir):
        st.write('正在删除……')
        st.write(i)
        os.remove(i)
with st.sidebar:
    if pdf is not None:
        st.write('文件夹含有不相关早期内容，请及时清理。')
        st.write(glob('results/*'))
        st.button('清空已有文件',on_click = remove)
           
    else:
        st.sidebar.write('结果文件夹为空，请放心使用')
            
    

