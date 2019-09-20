import json
import re
import base64
import qrcode
import chardet


def select(prompt1, prompt2, ans_list) -> str:
    while True:
        sel = input(prompt1)
        if sel in ans_list:
            return sel
        else:
            print(prompt2)


def func1():
    print("请选择功能：")
    print("\t1. 加密\t2. 解密")
    sel = select("请输入你的选择(1, 2)：", "请在1-2之间选择。", ['1', '2'])
    if sel == '1':
        plaintext = input("请输入明文：")
        print("结果：", base64.b64encode(plaintext.encode()).decode())
    elif sel == '2':
        while True:
            ciphertext = input("请输入密文：")
            try:
                print("结果：", base64.b64decode(ciphertext).decode())
            except:
                print("密文格式错误。")
            else:
                break


def func2():
    print("请输入字典（格式示例：a:1,b:1,c:2,d:3）:")
    while True:
        input_str = input()
        # 此处假定不存在“I love Python:1”这种含有空格的情况
        if re.match(r"^([^,:\s]+:[^,:\s]+,)*[^,:\s]+:[^,:\s]+$", input_str) != None:
            break
        else:
            print("格式错误！格式示例：a:1,b:1,c:2,d:3（不允许包含空格）")
    dict1 = {x[0]: x[1] for x in [x.split(":") for x in input_str.split(",")]}

    json_str = json.dumps(dict1, indent=4, ensure_ascii=False)
    print("\nJSON字符串:\n", json_str, "\ntype:", type(json_str))

    # 键值反转
    set1 = {dict1[x] for x in dict1}
    dict2 = {x: [y for y in dict1 if dict1[y] == x] for x in set1}
    # 除去只有一项的表
    for k in dict2:
        if len(dict2[k]) == 1:
            dict2[k] = dict2[k][0]
    print("\n新字典:", dict2, "\ntype:", type(dict2))


def func3():
    while True:
        filename = input("请输入文件名（不含“.txt”）：") + ".txt"
        if re.match(r'.*[/\\:*?"<>|]', filename) != None:
            print("文件名格式有误，请检查输入是否正确。")
            continue
        try:
            f = open(filename, "rb")
        except:
            print("文件打开失败，请检查输入是否正确，以及文件是否与程序在同一目录下。")
        else:
            break
    try:
        data = f.read()
        detect_result = chardet.detect(data)
        encoding = detect_result['encoding']
        if float(detect_result['confidence']) < 0.9:
            print("文本过短，无法准确判断编码类型。")
            if(detect_result['language'] == None or detect_result['encoding'] == None):
                print("未检测出结果。")
                sel = 'no'
            else:
                print("检测到语言为：", detect_result['language'])
                print("检测到编码为：", detect_result['encoding'])
                sel = select("是否正确？(yes/no)：", "请输入yes或no", ['yes', 'no'])
            if sel == 'no':
                encoding_list = ['UTF-8', 'GB2312', 'unicode']  # 此处仅为测试通过的编码类型
                print("支持的编码类型有：", encoding_list)
                sel2 = select("请选择编码类型：", "请在列表中选择。", encoding_list)
                encoding = sel2
        data = data.decode(encoding).encode('UTF-8')
        img = qrcode.make(data=data)
        img.save("qrcode.jpg")
    except:
        print("文件操作异常。")
    else:
        print("二维码已生成（./qrcode.jpg）。")
    finally:
        f.close()


running = True
while running:
    print("\n=======欢迎使用本工具箱，请选择功能：=======")
    print("\t1. base64加解密\n\t2. JSON字典及其反转\n\t3. 二维码生成\n\t4. 退出")
    sel = select("请输入你的选择(1,2,3,4)：", "请在1-4之间选择。", ['1', '2', '3', '4'])
    if sel == '1':
        func1()
    elif sel == '2':
        func2()
    elif sel == '3':
        func3()
    elif sel == '4':
        running = False
