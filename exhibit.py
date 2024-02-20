import streamlit as st
import streamlit.components.v1 as components 
from price_tagger import Add,Img2pdf
# from price_tagger.code_spider import CodeSpider
# from price_tagger.decoder import decodeDisplay
from glob import glob
import os
from PIL import Image,ImageDraw,ImageFont
import pandas as pd
import time
from PIL import Image
# import cv2
# import numpy as np


def main():
    st.set_page_config('价签生成器',page_icon = '💰')
    tab1,tab2,tab4,tab3 = st.tabs(['价签生成','价签智能生成','价签内部查询','文字生成',])


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
    def remove_file(file):
        file_path = os.path.dirname(__file__)+file
        os.remove(file_path)
        st.write(f'正在删除{file_path}')
    def write_data(text):
        with open('added_data.csv','a+') as f:
            #text = [name,spec,area,cata,unit,price]
            f.write(', '.join(map(str,text))+'\n')


    with st.sidebar:

        files = glob('results/*')
        if files:
            st.write('文件夹含有不相关早期内容，请及时清理。')
            st.write(files)
            st.button('清空已有文件', on_click=remove)
            delefile = st.selectbox('选择需要删除文件',glob('results/*'))
            if st.button('删除文件'):
               
                
                st.info(f'你打算删除{delefile}对吗？')
                is_true = st.checkbox('同意',value =True)
                if is_true and st.button('确认',on_click=remove_file,kwargs={'file':delefile}):
                    # os.remove(delefile)
                    st.write(f'已删除{delefile}')

        else:
            st.sidebar.write('结果文件夹为空，请放心使用')
        
            
        
        if st.button('合成pdf文件',key='hecheng'):
            
            img_list = glob('results/*.png')
            img2pdf = Img2pdf(img_list)
            img2pdf.save_pdf()
            if glob('results/*.pdf'):
                pdf = st.selectbox('选择需要下载的pdf文件',glob('results/*.pdf'),key='xiazai')
    
                try:
                    with open(pdf,'rb') as file:
                        st.download_button(
                        label = '下载合并后的pdf文件',
                            data =  file,
                            file_name="dowloaded.pdf",
                            mime = 'application/octet-stream')
                except:
                    pass
            else:
                st.write('暂无pdf文件')


    with tab1:

        def generate(name='',spec='',area='',cata='',unit=''):

            name = st.text_input('名称',value=name,key='name'+name)
            if len(spec)<1:
                spec_key = 'spec'+spec+name
            else:
                spec_key = 'spec'+spec+name
            spec = st.text_input('规格',value=spec,key=spec_key)
            if len(area)>5:
                new_area = area[:2]
                area_key = 'area' + area+name
            else:
                new_area = area
                area_key = 'area' + area+name
            area = st.text_input('产地',value=new_area,key=area_key,placeholder=area)
            cata = st.text_input('货号',value=cata,key='cata'+name+spec)
            if len(unit)<1:
                unit_key = 'unit'+unit+name
            else:
                unit_key = 'unit'+unit+name
            unit = st.text_input('单位',value=unit,key=unit_key)
            price = st.number_input('价格',format='%2f',min_value=0.0,key='price'+name)
            text = [name,spec,area,cata,unit,price]
            

            if st.button('生成',key='shengcheng'+name):
                write_data(text)
                get_res(text)
                img_list = glob('results/*.png')
                for i in img_list:
                    if i.endswith('png'):
                        st.image(i)



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
    with tab4:
        ## 库存搜索功能
        @st.cache_resource
        def get_data():
            data = pd.read_csv('产品数据全量.csv',index_col = 0,keep_default_na=0)
            data = data.drop_duplicates(subset=['货号','通用名'])
            # added_data = pd.read_csv('added_data.csv',header =None,index_col = 0,keep_default_na=0)
            
            # if added and len(added_data)>0:
            #     added_data.columns =['通用名','规格','产地','货号','单位','价格']
            #     added_data = added_data.drop_duplicates(subset=['货号','通用名'])
            #     return pd.concat([data,added_data],axis=0)
            # else:
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

    with tab2:
        st.title('条码查询')
        with st.expander('扫描',expanded = True):
            st.write('加入中...')

            # codespider = CodeSpider()

            # def get_info(barcode):
            #     return codespider.requestT1(barcode)
            # barcode = st.text_input('扫条形码')
            # data_dict = get_info(barcode)
            # st.write(data_dict)
            # if data_dict['msg'] != '查询成功':
            #     st.info('请输入查询，再试一次或者换一个')
            #     st.stop()
            # else:
            #     json_dict = data_dict['json']
            #     address = json_dict['code_address']
            #     if address[:2] not in ['黑龙','内蒙',]:
            #         address = address[:2]
            #     else:
            #         address = address[:3]
            #     generate(json_dict['code_name'],json_dict['code_spec'],
            #             address,'',
            #             json_dict['code_unit'])

    #     with st.form('条码查询'):
    #         code_cn = st.text_input('请输入条码')
    #         if st.form_submit_button('提交'):
    #             if not code_cn:
    #                 st.error('不能为空')
    #             c_spider = CodeSpider().requestT1(code_cn)

    #             st.write(c_spider)
    #             if c_spider['msg'] != '查询成功':
    #                 st.error('未查到，再试一次或者换一个')
    #                 st.stop()
    #             st.session_state.json_data = c_spider.get('json',None)
    #             # st.json(json_data)
    #     # try:
    #     if st.session_state.json_data['code_name']:
    #         generate(name=st.session_state.json_data['code_name'], spec=st.session_state.json_data['code_spec'],
    #                      area=st.session_state.json_data['code_company'], cata=' ', unit=st.session_state.json_data['code_unit'])
        # except:
        #     pass


if __name__ == '__main__':
    # subprocess.run(["streamlit", "run exhibit.py"])
    main()
        

        
    
