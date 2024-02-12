
import sys
import os
path_file = os.path.dirname(os.path.abspath(__file__))
if path_file not in sys.path:
    sys.path.append(path_file)
from image2pdf import Img2pdf
from pricetagger import Add
from code_spider import CodeSpider




# __all__ = ['Img2pdf', 'Add', ]
