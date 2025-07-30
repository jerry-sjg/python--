# 求1到100的偶数和奇数
xunhuan = False
while xunhuan == False:
    xuanze = int(input("请选择:1.偶数 2.奇数\n"))
    if xuanze == 1:
        for num in range(0,101,2):
            print("偶数:",num)
            xunhuan = True
    elif xuanze == 2:
        for num in range(1,101,2):
            print("奇数:",num)
            xunhuan = True
    else:
        print("输入错误")
    if xunhuan == True:
        print("程序结束")
        break