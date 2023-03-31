from PIL import Image
import os
base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Img2pdf():
    def __init__(self,image_list):
        assert isinstance(image_list,list)
        self.image_list = []
        for i in image_list:
            if i.endswith('png') or i.endswith('jpg') or i.endswith('jpeg'):
                self.image_list.append(i)
            else:
                raise ValueError(f'仅支持png与jpg「{i}」')
                
    def save_pdf(self,filename = None):
        
        img = Image.open(self.image_list[0])
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        append_images = []
        for image in self.image_list[1:]:
            image = Image.open(image)
            if image.mode == 'RGBA':
                image = image.convert('RGB')
                append_images.append(image)
            elif image.mode == 'RGB':
                append_images.append(image)
            else:
                raise ValueError('图片模式错误')
        if not filename:
            filename = f"{base_path}/results/{self.image_list[0].split('/')[-1].strip('.png')}.pdf"
        img.save(
            filename,
            save_all = True,
            append_images = append_images
        )
                
        
                
                
                
        

            
            
            
    
    