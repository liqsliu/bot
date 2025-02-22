# https://github.com/iamwhcn/digital-watermark/blob/main/wm/text2img.py


from PIL import Image, ImageFont, ImageDraw
import os

basedir = os.path.split(os.path.realpath(__file__))[0]

HOME = os.environ.get("HOME")

# need fix https://stackoverflow.com/a/53829424

fonts = {
    'SourceCN': HOME + '/fonts/SourceHanSansCN-Regular.otf', 
    'Source': HOME + '/fonts/SourceHanSans-Regular.ttc', 
    'Noto': '/system/fonts/NotoSansCJK-Regular.ttc', 
    'SimSun': basedir + '/fonts/simsun.ttc', 
    'SimHei': basedir + '/fonts/simhei.ttf',
    'SimKai': basedir + '/fonts/simkai.ttf',
    'Microsoft YaHei': basedir + '/fonts/msyh.ttc'
}


import os.path

for i in fonts.copy():
    if os.path.isfile(fonts[i]):
        pass
    else:
        fonts.pop(i)


if len(fonts) == 0:
    print("E: no font")
    exit()

#from tools import my_exceptions_handler




#@my_exceptions_handler
def textwrap(text, width, font, fs):
    """文本换行
    """
    lines = ['']
    temp = width
    ha = 0
    ha += fs*1.5
    wr = 0
    wrtmp = 0
    for c in text:
        w, _ = font.getsize(c)
        if temp < w:
            ha += fs*1.5
            temp = width
            lines.append('')
            if wrtmp > wr:
                wr = wrtmp
            wrtmp=0
        lines[-1] += c
        temp -= w
        wrtmp += w
    if wrtmp > wr:
        wr = wrtmp
    return lines, int(ha), int(wr)


def textlength(text, font):
    temp = 0
    for c in text:
        w, h = font.getsize(c)
        temp += w
    return temp, h


#@my_exceptions_handler
#def text2img(text, fill=0, size=300, mode='1', fontname=list(fonts.keys())[0], fontsize=30):
def text2img(text, fill=0, width=None, fontsize=64, bg=None, fontname=list(fonts.keys())[0]):
    """文本转图像
    mode='1' 二值图
    mode='RGB' RGB图
    """
    if not text:
        return
#        img = Image.new(mode, size, (255, 255, 255))

    if fill == 0:
        # default
        # font: white
        bg = 1
        mode = "1"
    elif fill == 1:
        bg = 0
        mode = "1"
    elif fill == "#000000":
        if bg is None or bg == 0 or bg == fill:
            bg = 255
        mode = "RGB"
    elif fill == "#FFFFFF":
        if bg is None or bg == 255 or bg == fill:
            bg = 0
        mode = "RGB"
    else:
        mode = "RGB"
        if bg is None:
            bg = 0

    if fontname not in fonts:
        fontname = list(fonts.keys())[0]
    font = ImageFont.truetype(fonts[fontname], fontsize)
    w, h = font.getsize(text[0])
    x_offset = 0
    print(w, h, fontsize)
    if len(text) <= 4:
        a, h = textlength(text, font)
        lines = [text]
#        size = (int(a), int(h*1.25))
        size = (int(a), int(fontsize*1.5))
    elif width is None:
        # prefer
#        width = int((len(text)*3/2)**0.5*w-0.5*w)
#        width = int((len(text)*3/2+(1/4)**2)**0.5*w-0.25*w)
#        lines = textwrap(text, width, font)
        a, h = textlength(text, font)
#        width = int((a*h + (0.25*h)**2)**0.5 - 0.25*h)
        width = int((a*fontsize + (0.25*fontsize)**2)**0.5 - 0.25*fontsize)
        if width < 1024:
            pass
#            size = (width, width)
        else:
            width = 1024
        lines, ha, width = textwrap(text, width, font, fontsize)
        size = (width, ha)
    elif width == 1:
        # force
        a, h = textlength(text, font)
        width = int((a*fontsize + (0.25*fontsize)**2)**0.5 - 0.25*fontsize)
        k = None
        while True:
            lines, ha, wr = textwrap(text, width, font, fontsize)

            if width == ha:
                print("good")
                break

            if not k:
                k = int((ha-width)/2)
                last = k
            print(width, ha, k, last)

            if ha > width:
                if last < 0:
                    if last == -1:
                        print("may be ok")
                        width = int(width)+1
                        break
                    k = int(last/2*(-1))
            else:
                if last > 0:
                    if last == 1:
                        print("may be ok")
                        width = int(width)
                        break
                    k = int(last/2*(-1))

            if k == 0:
                if ha > width:
                    k = 1
                else:
                    k = -1
            width = width+k
            last = k

        size = (width, width)
        if wr < width:
            x_offset = int((width-wr)/2)
    else:
        # custom
        if width < fontsize:
            width = fontsize
        lines, ha, width = textwrap(text, width, font, fontsize)
        size = (width, ha)


    if mode == '1':
        # default
        # font: white
#        img = Image.new(mode, size, 0)
        img = Image.new(mode, size, bg)
        dr = ImageDraw.Draw(img)
        y = 0
        for line in lines:
#            dr.text((0, y), line, font=font, fill=fill)
            dr.text((x_offset, y), line, font=font, fill=fill)
            y += 1.5 * fontsize # 1.5 倍行距
        return img
    elif mode == 'RGB':
        # font: black
#        img = Image.new(mode, size, (255, 255, 255))
        if type(bg) == int:
            img = Image.new(mode, size, (bg, bg, bg))
        else:
            img = Image.new(mode, size, bg)
        dr = ImageDraw.Draw(img)
        y = 0
        for line in lines:
            dr.text((x_offset, y), line, font=font, fill=fill)
            y += 1.5 * fontsize  # 1.5 倍行距
        return img
    else:
        return None

if __name__=='__main__':
#    img = text2img(u"中文字符1234567890ABCDEFGHIJKLMNabcdefghijklmn", 300, mode='RGB', fontname='aaa', fontsize=50)
#    img.show()
#    img = text2img(u"中文字符1234567890ABCDEFGHIJKLMNabcdefghijklmn", size=100, mode='RGB', fontname='aaa', fontsize=50)
    fill = "#000000"
    str = u"中文字符1234567890ABCDEFGHIJKLMNabcdefghijklmn"
    img = text2img(str*10, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test.png")
    img = text2img(str*10, width=1024, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test_1024.png")
    img = text2img(str*10, width=1, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test_f.png")
    img = text2img(u"中文", width=1, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test_s.png")
    img = text2img(u"abc", width=1, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test_sen.png")
    img = text2img(u"برای استفاده از پ", width=1, fill=fill, fontname='aaa', fontsize=50)
    img.save(f"/sdcard/Pictures/test_wtf.png")



