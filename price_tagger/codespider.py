import ddddocr
import requests
import json
import os
import time
import sys


class CodeSpider():

    def __init__(self):
         self.headers= {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
         self.path = os.path.abspath(os.path.dirname(sys.argv[0]))

    # json化
    def parse_json(self, s):
        begin = s.find('{')
        end = s.rfind('}') + 1
        return json.loads(s[begin:end])

    # 创建目录
    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path)
            # logger.info(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # logger.info(path + ' 目录已存在')
            return False

    # 爬取 "tiaoma.cnaidc.com" 来查找商品信息

    def requestT1(self, shop_id):
        url = 'http://tiaoma.cnaidc.com'
        s = requests.session()

        # 获取验证码
        img_data = s.get(url + '/index/verify.html?time=', headers=self.headers).content
        with open('data/verification_code.png', 'wb') as v:
            v.write(img_data)

        # 解验证码
        ocr = ddddocr.DdddOcr()
        with open('data/verification_code.png', 'rb') as f:
            img_bytes = f.read()
        code = ocr.classification(img_bytes)
        # logger.info('当前验证码为 ' + code)
        print(code)
        # 请求接口参数
        data = {"code": shop_id, "verify": code}
        resp = s.post(url + '/index/search.html', headers=self.headers, data=data)
        resp_json = self.parse_json(resp.text)
        # logger.info(resp_json)

        # 判断是否查询成功
        if resp_json['msg'] == '查询成功' and resp_json['json'].get('code_img'):
            # 保存商品图片
            img_url = ''
            if resp_json['json']['code_img'].find('http') == -1:
                img_url = url + resp_json['json']['code_img']
            else:
                img_url = resp_json['json']['code_img']

            try:
                shop_img_data = s.get(img_url, headers=self.headers, timeout=10, ).content
                # 新建目录
                self.mkdir(self.path + '\\' + shop_id)
                localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                # 保存图片
                with open(self.path + '\\' + shop_id + '\\' + str(localtime) + '.png', 'wb') as v:
                    v.write(shop_img_data)
                # logger.info(path + '\\' + shop_id + '\\' + str(localtime) +'.png')
            except requests.exceptions.ConnectionError:
                pass
                # logger.info('访问图片URL出现错误！')

        if resp_json['msg'] == '验证码错误':
            CodeSpider().requestT1(shop_id)

        return resp_json
