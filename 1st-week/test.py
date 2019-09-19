import json
import re
import base64
import qrcode


def func1():
    print("请选择功能：")
    print("\t1. 加密\t2. 解密")
    while True:
        selection = input("请输入你的选择(1, 2)：")
        if selection == '1':
            plaintext = input("请输入明文：")
            print("结果：", base64.b64encode(plaintext.encode()).decode(), "\n")
            break
        elif selection == '2':
            while True:
                ciphertext = input("请输入密文：")
                try:
                    print("结果：", base64.b64decode(ciphertext).decode(), "\n")
                    break
                except:
                    print("密文格式错误。")
            break
        else:
            print("请在1-2之间选择。")


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
    print("\n新字典:", dict2, "\ntype:", type(dict2), "\n")


def func3():
    while True:
        filename = input("请输入文件名（不含“.txt”）：") + ".txt"
        if re.match(r'.*[/\\:*?"<>|]', filename) != None:
            print("文件名格式有误，请检查输入是否正确。")
            continue
        try:
            f = open(filename)
            break
        except:
            print("文件打开失败，请检查输入是否正确，以及文件是否与程序在同一目录下。")
    try:
        data = f.read()
        f.close()
        img = qrcode.make(data=data)
        img.save("qrcode.jpg")
    except:
        print("文件操作异常。\n")
    else:
        print("二维码已生成（./qrcode.jpg）。\n")


running = True
while running:
    print("=======欢迎使用本工具箱，请选择功能：=======")
    print("\t1. base64加解密\n\t2. JSON字典及其反转\n\t3. 二维码生成\n\t4. 退出")
    while True:
        selection = input("请输入你的选择(1,2,3,4)：")
        if selection == '1':
            func1()
            break
        elif selection == '2':
            func2()
            break
        elif selection == '3':
            func3()
            break
        elif selection == '4':
            running = False
            break
        else:
            print("请在1-4之间选择。")
