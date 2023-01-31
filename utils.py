from PySide2.QtWidgets import QFileDialog
import re

import json
import json5
import os


KEYPRIVATE = "w09f*1l.kl~7tl-t0hmc-eizlsk3jo*+b72wjz*!"

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)
def parse_json(filename):
    # start = time.time()
    """ Parse a JSON file
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    # print(filename)
    with open(filename, 'r', encoding="utf-8", errors='ignore') as f:
    #     # content = f.readlines()
    #     # print(content)
        content = ''.join(f.readlines())
        ## Looking for comments
        # match = comment_re.search(content)
        # while match:
        #     # single line comment
        #     content = content[:match.start()] + content[match.end():]
        #     match = comment_re.search(content)
        # Return json file
    # print(filename, time.time()-start)
    # f=open(filename,'rb')
    # f_read=f.read()
    # import ipdb
    # ipdb.set_trace()
    # f_chaInfo=chardet.detect(f_read)
    # final_data=f_read.decode(f_chaInfo['encoding'], errors='ignore')
    # f.close()
    # content = ''.join(final_data)
    return json5.loads(content)



def fast_parse_json(filename):
    # start = time.time()
    """ Parse a JSON file
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    # print(filename)
    with open(filename, 'r', encoding="utf-8", errors='ignore') as f:
    #     # content = f.readlines()
    #     # print(content)
        content = ''.join(f.readlines())
        ## Looking for comments
        # match = comment_re.search(content)
        # while match:
        #     # single line comment
        #     content = content[:match.start()] + content[match.end():]
        #     match = comment_re.search(content)
        # Return json file
    # print(filename, time.time()-start)
    # f=open(filename,'rb')
    # f_read=f.read()
    # import ipdb
    # ipdb.set_trace()
    # f_chaInfo=chardet.detect(f_read)
    # final_data=f_read.decode(f_chaInfo['encoding'], errors='ignore')
    # f.close()
    # content = ''.join(final_data)
    return json.loads(content)




def write_json(json_data,json_name):
    # Writing JSON data
    with open(json_name, 'w', encoding="utf-8") as f:
        json.dump(json_data, f,indent=4)

def enctry(s, k = KEYPRIVATE):
    encry_str = ""
    for i,j in zip(s,k):
        temp = str(ord(i)+ord(j))+'_'
        encry_str = encry_str + temp
    return encry_str

def dectry(p, k = KEYPRIVATE):
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k):
        temp = chr(int(i) - ord(j))
        dec_str = dec_str+temp
    return dec_str

def get_mac_address():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def choose_file(ui_,info,ename,file_path = "./"):
    selected_file_path, _ = QFileDialog.getOpenFileName(ui_,
                                        info,
                                        file_path,
                                        ename)
    return selected_file_path

def choose_folder(ui_,info,file_path = "./"):
    directory = QFileDialog.getExistingDirectory(ui_, info, file_path)
    return directory

def list_find_files(path, target, filepath):
    files = os.listdir(path);
    for f in files:
        npath = os.path.join(path, f)
        if(os.path.isfile(npath)):
            if f.endswith(target):
                key = os.path.splitext(f)[0]
                filepath[key] = npath
        else:
            list_find_files(npath, target, filepath)
    return filepath
