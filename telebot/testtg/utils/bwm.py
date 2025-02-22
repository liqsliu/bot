#!/usr/bin/python
# -*- coding: UTF-8 -*-



from BlindWatermark import watermark






def add(img, wm):
    pass


def get(img):
    pass




if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    #嵌入

    bwm1 = watermark(2048,1024,36,25)
    #4399和2333是两个随机种子,36和20是用于嵌入算法的除数,理论上第一个除数要大于第二个,除数越大鲁棒性越强,但是除数越大,输出图片的失真越大,需要权衡后决定
    #这两个随机种子最好对不同图片有不同的取值, 防止种子暴露而使得所有图片失去保护
    #第二个除数可以不加,增加对水印鲁棒性没有明显的提升,但是会一定情况想影响输出图片的质量
    bwm1.read_ori_img("lena.png")
    #读取原图
    bwm1.read_wm("wm.png")
    #读取水印
    bwm1.embed('out.png')
    #在原图中嵌入水印并输出到'out.png'
