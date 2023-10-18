import os
"""存放所有.py 文件路径的列表"""
py_files=[]

def get_py(dirpath):
   
    fileList = os.listdir(dirpath)  # 获取path目录下所有文件
    for filename in fileList:
        pathTmp = os.path.join(dirpath, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 如果是目录
            get_py(pathTmp)  # 则递归查找
        elif filename[-3:].upper() == '.PY':  # 如果不是目录，则比较后缀名
            py_files.append(pathTmp)


# get_py(r'd:\PythonProjects\Python-CIA')
# for file in py_files:
#     print(file)



