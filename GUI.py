import data_read
import nlp
from eda import eda_res
import compare
import PySimpleGUI as sg
#首先设置窗口样式
sg.theme('BluePurple')
#布局控件元素
left_text = [
    [sg.Input(size=50),
     sg.FileBrowse("载入文件"),
     sg.Button("确定")],
    [sg.Text("原文文本")],
    [sg.Multiline(size=(60, 35))],
]
right_text = [
    [sg.Multiline(size=(40, 5)),
     sg.Button("上一句"),
     sg.Button("下一句")],
    [sg.Multiline(size=(40, 5)), sg.Button("回译扩增")],
    [sg.Multiline(size=(30, 4)), sg.Button("同义扩增")],
    [sg.Multiline(size=(30, 4))],
    [sg.Multiline(size=(30, 4))],
    [sg.Multiline(size=(30, 4))],
    [sg.Button("回译验证")],
    [sg.Input(size=10)],
    [sg.Button("同义验证")],
    [sg.Input(size=10), sg.Input(size=10)],
    [sg.Input(size=10), sg.Input(size=10)],
]
left_col = sg.Column(left_text)
right_col = sg.Column(right_text)
layout = [
    #每一个列表为一行
    [left_col, right_col],
]
#窗口实例化 并设置窗口名，把布局内容放进去
window = sg.Window('文本扩增', layout)
txt = ""
sentences = []
length = 0
order = 0
#进入窗口循环
while True:
    event, values = window.read()  #读取窗口所有内容，event为动作
    if event is None:  #窗口的右上关闭动作即None
        break
    if event == '确定':
        if len(values[0]) > 0:
            print(values[0])
            txt, sentences = data_read.readFile(values[0])
            length = len(sentences)
            window[1].update(txt)
            window[2].update(sentences[order])
    if event == '下一句' and sentences != []:
        if order < length - 1:
            order += 1
            window[2].update(sentences[order])
            for i in range(3, 13):
                window[i].update('')
    if event == '上一句' and sentences != []:
        if order > 0:
            order -= 1
            window[2].update(sentences[order])
            for i in range(3, 10):
                window[i].update('')
    if event == '回译扩增' and len(values[2]) != 0:
        print(values[2])
        window[3].update(nlp.Nlp(values[2]))
        window[8].update('')
    if event == '同义扩增' and len(values[2]) != 0:
        print(values[2])
        New_sentences = eda_res(values[2])
        for i in range(4):
            window[i + 4].update(New_sentences[i])
            window[i + 9].update('')
    if event == '回译验证' and len(values[2]) > 0 and len(values[3]) > 0:
        window[8].update(compare.compare_res(values[2], values[3]))
    if event == '同义验证' and len(values[2]) > 0 and len(values[4]) > 0:
        for i in range(4):
            window[i + 9].update(compare.compare_res(values[2], values[i + 4]))
window.close()