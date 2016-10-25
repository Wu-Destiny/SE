import index
# index.index()

list = index.indexSearch("Chanel/香奈儿炫亮魅力丝绒唇膏3.5g 口红 打造性感美唇43 42")

for l in list:
    print(l["name"],l["url"],l["price"])