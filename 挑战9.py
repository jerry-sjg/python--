# 求1到100的和
shu = int(input("请输入一个数:"))
he = 0
jiashu = 1
while jiashu <= shu: 
    he = he + jiashu
    print("加数:",jiashu,"和:",he)
    jiashu = jiashu + 1
print("和:",he)