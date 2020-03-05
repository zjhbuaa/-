# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:04:49 2019

@author: zjh
"""

import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import re
import webbrowser
import time
import wordcloud
from PIL import Image,ImageTk

#计时功能
start=time.perf_counter()
#主程序
top = tk.Tk()   #Toplevel
top.geometry("625x600")
top.resizable(False,False)
top.title("简易的文本编辑器")
#创建文本框
textbox = tk.Text(top,undo=True,maxundo=20)
textbox.place(x=5,y=50,width=600,height=500)

#插入一个分隔符到存放操作记录的栈中，用于表示已经完成一次完整的操作
textbox.edit_separator()
#将键盘鼠标操作事件“<Key><Button-1>”与回调函数***_callback绑定
textbox.bind("<Key>",key_callback)
#textbox.bind("<Button-1>",left_callback)
#链接效果163
textbox.tag_bind("link163","<Enter>",show_hand_cursor)
textbox.tag_bind("link163","<Button-1>",click163)
textbox.tag_bind("link163","<Leave>",show_arrow_cursor)
#链接效果126
textbox.tag_bind("link126","<Enter>",show_hand_cursor)
textbox.tag_bind("link126","<Button-1>",click126)
textbox.tag_bind("link126","<Leave>",show_arrow_cursor)

ybar=tk.Scrollbar(top,orient=tk.VERTICAL)
ybar.config(command=textbox.yview)
textbox.config(yscrollcommand=ybar.set) 
ybar.pack(side=tk.RIGHT,fill=tk.Y)

#创建导入文本按钮
ReadBtn=tk.Button(top,
                  text="导入文本",
                  command=originaltext)
ReadBtn.place(x=5,y=10,width=60,height=30)
#创建清除文本按钮
clearBtn=tk.Button(top,
                   text="标准模式",
                   command=lambda:modifiedtext(text))
clearBtn.place(x=80,y=10,width=60,height=30)
#创建词频统计按钮
wordfreBtn=tk.Button(top,
                     text="词频统计",
                     command=lambda:frequency(text))  #lambad传入参数是lambda
wordfreBtn.place(x=155,y=10,width=60,height=30)
#绘图按钮
drawBtn=tk.Button(top,
                  text="绘制图形",
                  command=lambda:draw(text,stopwords))
drawBtn.place(x=230,y=10,width=60,height=30)
#词云按钮
cloudBtn=tk.Button(top,
                   text="生成词云",
                   command=lambda:drawcloud(text))
cloudBtn.place(x=305,y=10,width=60,height=30)
#高亮按钮
lightBtn=tk.Button(top,
                   text="高亮文本",
                   command=highlight)
lightBtn.place(x=380,y=10,width=60,height=30)
#取消高亮按钮
cancellightBtn=tk.Button(top,
                         text="取消高亮",
                         command=cancellight)
cancellightBtn.place(x=455,y=10,width=60,height=30)
#查找按钮
searchBtn=tk.Button(top,
                    text="标记单词",
                    command=searchword)
searchBtn.place(x=530,y=10,width=60,height=30)
labelIntro=tk.Label(top,
                    text="注:除保存文本&导入文本,其余对文本内容的操作需先保存,后分析",
                    justify=tk.RIGHT,
                    width=1000) 
labelIntro.place(x=-125,y=575,width=1000,height=20)
#添加菜单功能
menubar = tk.Menu(top)  #创建一个顶级菜单
#filemenu1创建主菜单和子菜单
c1 = [originaltext,save,undo_callback,redo_callback,clear,lambda:modifiedtext(text),onSave]
i = 0
filemenu1 = tk.Menu(menubar,tearoff = 0)
for item in ['导入文本','文件保存','撤销操作','恢复操作','清空文本','标准模式','导出文本']:
    filemenu1.add_command(label = item,command = c1[i])
    filemenu1.add_separator()  #加分割线
    i = i + 1
#filemenu2创建主菜单和子菜单
c2 = [strlong,wordlong,lambda:frequency(text),lambda:draw(text,stopwords),lambda:drawcloud(text)]
i = 0
filemenu2 = tk.Menu(menubar,tearoff = 0)
for item in ['字符统计','词数统计','词频统计','绘柱状图','绘制云图']:
    filemenu2.add_command(label = item,command = c2[i])
    filemenu2.add_separator()  #加分割线
    i = i + 1
#filemenu3创建主菜单和子菜单
c3 = [highlight,cancellight,searchword,searchword0,lambda:change(text)]
i = 0
filemenu3 = tk.Menu(menubar,tearoff = 0)
for item in ['高亮文本','取消高亮','标记单词','查找单词','修改单词']:
    filemenu3.add_command(label = item,command = c3[i])
    filemenu3.add_separator()  #加分割线
    i = i + 1
#filemenu4创建主菜单和子菜单
c4 = [link163,link126]
i = 0
filemenu4 = tk.Menu(menubar,tearoff = 0)
for item in ['163邮箱','126邮箱']:
    filemenu4.add_command(label = item,command = c4[i])
    filemenu4.add_separator()  #加分割线
    i = i + 1
#filemenu5创建主菜单和子菜单
c5 = [caltime]
i = 0
filemenu5 = tk.Menu(menubar,tearoff = 0)
for item in ['时间统计']:
    filemenu5.add_command(label = item,command = c5[i])
    filemenu5.add_separator()  #加分割线
    i = i + 1
#指定主菜单和子子菜单的级联关系
#将menubar的menu属性指定为filemenu，即filemenu为menubar的下拉菜单
menubar.add_cascade(label = '文件编辑',menu = filemenu1)
menubar.add_cascade(label = '统计功能',menu = filemenu2)
menubar.add_cascade(label = '文件显示',menu = filemenu3)
menubar.add_cascade(label = '发送邮件',menu = filemenu4)
menubar.add_cascade(label = '时间管理',menu = filemenu5)
top['menu'] = menubar
tk.mainloop()