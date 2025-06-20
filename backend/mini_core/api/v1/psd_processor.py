import logging
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from flask.views import MethodView
from PIL import Image, ImageDraw, ImageFont
from psd_tools import PSDImage
from datetime import datetime
from pathlib import Path
import uuid
from kit.util.blueprint import APIBlueprint
from werkzeug.utils import secure_filename
from flask import  current_app
from backend.mini_core.schema.psd_processor import (
    PSDProcessRequestSchema, PSDProcessResponseSchema
)

# 配置日志
logger = logging.getLogger(__name__)

blp = APIBlueprint('psd_processor', 'psd_processor', url_prefix='/psd')

@dataclass
class TextAttributes:
    """文本属性数据类"""
    text: str
    font_name: str
    font_size: int
    color: Tuple[int, int, int, int]
    position: Tuple[int, int]
    transform: any
    layer_size: Tuple[int, int]

class FontManager:
    """字体管理类"""
    FALLBACK_FONTS = [
        'simkai.ttf',      # 楷体
        'simhei.ttf',      # 黑体
        'simsun.ttc',      # 宋体
        'msyh.ttc',        # 微软雅黑
        'simfang.ttf',     # 仿宋
        'STKAITI.TTF',     # 华文楷体
        'STXIHEI.TTF',     # 华文细黑
        'STZHONGS.TTF',    # 华文中宋
        'STFANGSO.TTF',    # 华文仿宋
    ]

    @staticmethod
    def load_font(font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """加载字体，如果指定字体不可用则尝试备用字体"""
        try:
            # 处理字体名称并尝试不同的文件扩展名
            font_bases = [
                str(font_name).replace("'", "").lower(),
                str(font_name).replace("'", ""),
                str(font_name).replace("'", "").replace("-", ""),
                str(font_name).replace("'", "").replace("-Regular", ""),
            ]

            # 尝试不同的文件扩展名
            extensions = ['.ttf', '.ttc', '.TTF', '.TTC', '.otf']

            # 尝试所有可能的字体文件名组合
            for base in font_bases:
                for ext in extensions:
                    try:
                        font_file = base + ext
                        return ImageFont.truetype(font_file, font_size)
                    except Exception:
                        continue
            cc=str(font_name).replace("'", "").lower()

            # 如果原始字体加载失败，尝试备用字体
            logger.warning(f"无法加载主字体 {font_name}，尝试备用{cc}字体")
            for fallback_font in FontManager.FALLBACK_FONTS:
                try:
                    return ImageFont.truetype(fallback_font, font_size)
                except Exception as e:
                    logger.warning(f"无法加载备用字体 {fallback_font}: {e}")

            # 如果所有备用字体都失败，使用默认字体
            logger.warning("所有字体加载失败，使用默认字体")
            return ImageFont.load_default()

        except Exception as e:
            logger.error(f"字体加载过程中发生错误: {e}")
            return ImageFont.load_default()

def convert_psd_text_to_imagedraw(layer):

    """
    将PSD文本图层的属性转换为ImageDraw需要的值

    Args:
        layer: PSD文本图层对象

    Returns:
        dict: 包含转换后的属性
    """
    try:
        # 获取文本内容
        text = layer.engine_dict['Editor']['Text'].value

        # 获取字体信息
        fontset = layer.resource_dict['FontSet']
        runlength = layer.engine_dict['StyleRun']['RunLengthArray']
        rundata = layer.engine_dict['StyleRun']['RunArray']
            # 访问字符样式RunData
        # 解析字体和样式信息
        font_info = parse_font_info(fontset)

        # 获取颜色信息
        color_info = parse_color_info(rundata)

        # 获取字体大小
        font_size = parse_font_size(rundata)

        # 获取文本位置和变换信息
        transform = layer.transform
        position = (layer.left, layer.top)

        return {
            'text': text,
            'font_name': font_info['font_name'],
            'font_size': font_size,
            'color': color_info,
            'position': position,
            'transform': transform,
            'layer_size': layer.size
        }

    except Exception as e:
        print(f"转换文本属性时出错: {str(e)}")
        return None

def parse_font_info(fontset):
    """解析字体信息"""
    try:
        # 获取第一个字体（通常是最主要的字体）
        if fontset and len(fontset) > 0:
            # 查找非AdobeInvisFont的字体
            for font in fontset:
                if font['Name'] != 'AdobeInvisFont':
                    return {
                        'font_name': font['Name'],
                        'script': font.get('Script', 0),
                        'font_type': font.get('FontType', 0)
                    }

            # 如果都是AdobeInvisFont，返回第一个
            return {
                'font_name': fontset[0]['Name'],
                'script': fontset[0].get('Script', 0),
                'font_type': fontset[0].get('FontType', 0)
            }
    except Exception as e:
        print(f"解析字体信息时出错: {str(e)}")

    return {'font_name': 'Arial', 'script': 0, 'font_type': 0}

def parse_color_info(rundata):
    """解析颜色信息"""
    try:
        if rundata and len(rundata) > 1:  # 确保至少有2个元素
            style_data = rundata[1]['StyleSheet']['StyleSheetData']
            if 'FillColor' in style_data:
                fill_color = style_data['FillColor']
                if fill_color['Type'] == 1:  # RGB颜色
                    values = fill_color['Values']
                    # PSD中的颜色值是0-1范围，需要转换为0-255
                    a = int(values[0] * 255)
                    r = int(values[1] * 255)
                    g = int(values[2] * 255)
                    b = int(values[3] * 255)
                    return (r, g, b, a)
        elif rundata and len(rundata) > 0:  # 如果只有一个元素，使用第一个
            style_data = rundata[0]['StyleSheet']['StyleSheetData']
            if 'FillColor' in style_data:
                fill_color = style_data['FillColor']
                if fill_color['Type'] == 1:  # RGB颜色
                    values = fill_color['Values']
                    # PSD中的颜色值是0-1范围，需要转换为0-255
                    a = int(values[0] * 255)
                    r = int(values[1] * 255)
                    g = int(values[2] * 255)
                    b = int(values[3] * 255)
                    return (r, g, b, a)
    except Exception as e:
        print(f"解析颜色信息时出错: {str(e)}")

    return (0, 0, 0, 255)  # 默认黑色

def parse_font_size(rundata):
    """解析字体大小"""
    try:
        if rundata and len(rundata) > 1:  # 确保至少有2个元素
            style_data = rundata[1]['StyleSheet']['StyleSheetData']
            if 'FontSize' in style_data:
                return int(style_data['FontSize'])
        elif rundata and len(rundata) > 0:  # 如果只有一个元素，使用第一个
            style_data = rundata[0]['StyleSheet']['StyleSheetData']
            if 'FontSize' in style_data:
                return int(style_data['FontSize'])
    except Exception as e:
        print(f"解析字体大小时出错: {str(e)}")

    return 20  # 默认字体大小

def create_text_image_with_psd_attributes(psd, layer, new_text,i,file_name_color):
    """
    使用PSD文本图层的属性创建新的文本图像

    Args:
        psd: PSD文件对象
        layer: 文本图层对象
        new_text: 新的文本内容
    """
    try:
        # 转换PSD属性
        text_attrs = convert_psd_text_to_imagedraw(layer)
        if not text_attrs:
            print("无法获取文本属性")
            return

        print("转换后的属性:")
        print(f"原文本: {text_attrs['text']}")
        print(f"新文本：{new_text}")
        print(f"字体: {text_attrs['font_name']}")
        print(f"字体大小: {text_attrs['font_size']}")
        print(f"颜色: {text_attrs['color']}")
        print(f"位置: {text_attrs['position']}")
        # 创建图像
        img = Image.new('RGBA', layer.size,(0,0,0,0))
        draw = ImageDraw.Draw(img)
        font = FontManager.load_font(text_attrs['font_name'], text_attrs['font_size'])
        # 计算文本位置（居中）
        text_bbox = draw.textbbox((0, 0), new_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (layer.size[0] - text_width) // 2
        y = (layer.size[1] - text_height) // 2
        # 打印字体名称,用于调试字体加载问题
        # 绘制文本
        draw.text((x,y), new_text, font=font, fill=text_attrs['color'])
        # draw.text((x,y), new_text, font=font, fill=(255,0,0,100))
        bg=Image.new('RGBA',psd.size,(0,0,0,0))
        img.save(f"tmp{i}.png")
        file1 = Image.open(f"tmp{i}.png")
        bg.paste(file1,(text_attrs['position'][0],text_attrs['position'][1]))
        bg.save(f"bg{i}.png")
        file_name_color[i]['file_name']=f"bg{i}.png"
        file_name_color[i]['color']=text_attrs['color']
    except Exception as e:
        print(f"创建文本图像时出错: {str(e)}")
        return None
def save_file(file) -> str:
    """保存上传的文件并返回生成的文件名"""
    # 生成唯一文件名
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    timestamp = datetime.now().strftime('%Y%m%d')
    unique_filename = f"{timestamp}_{uuid.uuid4().hex}.{extension}" if extension else f"{timestamp}_{uuid.uuid4().hex}"
    # 确保上传目录存在
    Image_Path = current_app.config.get('IMAGE_PATH')
    upload_dir = Path(Image_Path)
    date_dir = upload_dir / timestamp
    if not date_dir.exists():
        date_dir.mkdir(parents=True, exist_ok=True)

    # 保存文件
    file_path = date_dir / unique_filename
    file.save(file_path)
    save_file_path= f"{str(Path(timestamp))}/{unique_filename}"
    return save_file_path


def get_file_url(filename: str) -> str:
    """根据文件名生成访问URL"""
    import os
    base_url = current_app.config.get('UPLOADS_URL_PREFIX', '/files')
    # os.path.join(base_url,filename)
    return f"{base_url}{filename}"
# 创建全局的PSD处理器实例
psd_processor = None
@blp.route('/process')
class PSDProcessAPI(MethodView):
    """PSD处理API"""

    @blp.arguments(PSDProcessRequestSchema)
    @blp.response(PSDProcessResponseSchema)
    def post(self, args: dict):
        """处理PSD文件"""
        # try:
        global psd_processor

        # 从请求参数中获取PSD文件路径和新文本
        psd_path = args.get('psd_path', 'jinjiang2.psd')
        new_text = args.get('new_text', '茅台')
        new_text = new_text[::-1]
        new_text=new_text+""+new_text
        # 验证PSD文件是否存在
        if not Path(psd_path).exists():
            return {
                "code": 400,
                "message": f"PSD文件不存在: {psd_path}",
                "data": None
            }

        psd = PSDImage.open(psd_path)
        i:int=0
        layers_to_remove:list = []
        #定义数组存储文件名和颜色 - 修改为字典列表以便修改
        file_name_color:list = [
            {'file_name': 'bg0.png', 'color': (255, 0, 0, 0)},
            {'file_name': 'bg1.png', 'color': (0, 255, 0, 0)},
            {'file_name': 'bg2.png', 'color': (0, 0, 255, 0)},
            {'file_name': 'bg3.png', 'color': (255, 255, 255, 0)}
        ]

        for index,layer in enumerate(psd):
            if layer.kind == "type":
                create_text_image_with_psd_attributes(psd,layer, new_text[i],i,file_name_color)
                layers_to_remove.append(layer)
                i=i+1
            else:
                print(layer.kind,layer.name,index)
        #删除即将覆盖的图层
        for layer1 in layers_to_remove:
            psd.remove(layer1)
        psd.composite().save("background.png")
        bj=Image.open("background.png")
        for item in file_name_color:
            image_obj = Image.open(item['file_name'])
            x = Image.new('RGBA', bj.size, item['color'])
            out0 = Image.composite(x, bj, image_obj)
            bj=out0
        save_path=f"{random.randint(100000,999999)}.png"
        bj.save(save_path)
        file_bak=Image.open(save_path)
        filename = save_file(file_bak)
        file_url = get_file_url(filename)
        return {
            "code": 200,
            "message": f"处理完成! ",
            "data": {"url":file_url}
        }
