# _*_ coding:utf8 _*_
import json
import os

def json_remove_repeat():
    """
    去除json文件中相同的网页
    :return:
    """
    # 读取json文件
    read_results = []
    with open('data/data.json', encoding='utf-8') as fin:
        read_results = [json.loads(line.strip()) for line in fin.readlines()]
    # 删除重复的内容
    view_url = set()
    results = []
    for res in read_results:
        if res['url'] not in view_url:
            view_url.add(res['url'])
            results.append(res)
    print("Total num:{}, duplication num:{}".format(len(read_results), len(read_results) - len(results)))
    # 写入json文件，仅写入1000条
    line_num = 0
    with open('data/data.json', 'w', encoding='utf-8') as fout:
        for sample in results:
            fout.write(json.dumps(sample, ensure_ascii=False) + '\n')
            line_num += 1
            if line_num == 1000:
                break


def json_statistic():
    """
    对当前 json文件进行统计，记录url数，文件个数
    :return: 返回url集合，文件名字集合
    """
    # 读取json文件
    read_results = []
    with open('data/data.json', encoding='utf-8') as fin:
        read_results = [json.loads(line.strip()) for line in fin.readlines()]
    url = set()     # 记录url集合
    file_name = []  # 记录文件名字
    url_with_file = 0  # 带附件的网页个数
    for res in read_results:
        url.add(res['url'])
        if len(res['file_name']):
            file_name += res['file_name']
            url_with_file += 1
    value = len(read_results), url_with_file, len(file_name), len(set(file_name))
    print("Url: %d, Url_with_file: %d, total file: %d, no duplication file num: %d" % value)
    return url, set(file_name)

def read_json():
    read_results = []
    with open('data.json', encoding='utf-8') as fin:
        read_results = [json.loads(line.strip()) for line in fin.readlines()]
    print(len(read_results))
    file_name = []
    file_num = 0
    view_url = set()
    for res in read_results:
        if res['url'] in view_url:
            print(res['url'])
        view_url.add(res['url'])
        if len(res['file_name']):
            file_num += len(res['file_name'])
            file_name += res['file_name']
    print("view_url: " + str(len(view_url)))
    print(len(file_name))
    print("file_num: " + str(file_num))
    print(file_name[0:4])
    print(len(file_name))
    print(len(set(file_name)))

    # file_name_set = set(file for file in file_name)
    # print(file_name_set)
    # print(len(file_name_set))

def handle_file():
    url_set, file_set = json_statistic()
    path = "File"
    file_list = os.listdir(path)
    # 删除File文件夹中多余的文件
    print("remove redundant file in File folder:")
    for file in file_list:
        if file not in file_set:
            os.remove(path+"/"+file)
            print(file)
    # 删除json 文件中附件不存在的url
    file_list = os.listdir(path)
    print("remove missing file's url in json :")
    # 读取json文件
    read_results = []
    with open('data/data.json', encoding='utf-8') as fin:
        read_results = [json.loads(line.strip()) for line in fin.readlines()]
    results = []
    for res in read_results:
        if len(res['file_name']):
            if set(res['file_name']).issubset(set(file_list)):
                results.append(res)
            else:
                print(res['url'] + str(res['file_name']))
        else:
            results.append(res)
    # 删除json中附件有重复名字的url
    print("remove duplication file's url in json :")
    tmp_file_set = list()
    final_results = []
    for res in results:
        if len(res['file_name']):
            if len([file for file in res['file_name'] if file in tmp_file_set]):
                print(res['url'])
                continue
            tmp_file_set += res['file_name']
        final_results.append(res)
    # 写回json文件
    with open('data/data.json', 'w', encoding='utf-8') as fout:
        for sample in final_results:
            fout.write(json.dumps(sample, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    # read_json()
    json_remove_repeat()
    url_set, file_set = json_statistic()
    handle_file()