#!/usr/bin/python
# -*- coding: UTF-8 -*-


if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
elif __package__ != "":
    print('{} 运行 in package: {}'.format(__file__, __package__))
else:
    print('{} 运行'.format(__file__))

