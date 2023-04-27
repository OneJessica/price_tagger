## Application
用于价签生成并合并为pdf
## content
price_tagger 含有连个类 Add——添加文本，Img2pdf——将图片合成为pdf
## Usage
```
from price_tagger import Add,Img2pdf
add = Add()
add.get_text(text = ['c','b','c','d','e',12
                    
                    ],
             # file_name = 'test.png' #可有可无，无时默认放入results文件夹中，按名称.时间命名
            )
img_list = ['results/a.png']      # 一系列图片      
img2pdf = Img2pdf(img_list)     
img2pdf.save_pdf('a.pdf')       #存成pdf,文件名可有可无，无时默认为某张图片名称


```
## 其他使用
web端直接使用，使用streamlit 展示界面使用，见exhinit.py
需要安装streamlit (pip install streamlit) 和 git （brew intall git）
 ```
git clone https://github.com/OneJessica/price_tagger.git
cd price_tagger
streamlit run exhibit.py
```
