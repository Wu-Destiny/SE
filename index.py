#! -*- coding:utf-8 -*-
import jieba
import driver
from bson import ObjectId

dbs = ["pro_tm",
       "pro_jd",
       "pro_ymx"
       ]

stopword = ["【", "】",
            "/", "：", "-",
            "（", "）", ""
            ]

m = driver.Mongo()
m.connect()
count = 0


def index():
    global count
    for db in dbs:
        list = m.findall(db)
        for l in list:
            name = l["name"]
            count = count + 1
            if (count < 5409):
                continue
            seg_list = jieba.cut(name)
            str = ' '.join(seg_list)
            id = l["_id"]
            strs = str.split(" ")
            for s in strs:
                flag = 1
                for w in stopword:
                    if s == w:
                        flag = 0
                if flag == 0:
                    continue
                tag = db + "&&" + id.__str__()
                result = m.findall("index", {"word": s})
                if result.count() == 0:
                    post = {"word": s, "tag": [tag]}
                    m.insert("index", post)
                    print(count, post)
                else:
                    for r in result:
                        fTag = 0
                        tags = []
                        for t in r["tag"]:
                            if t == tag:
                                fTag = 1
                            else:
                                tags.append(t)
                        if fTag == 0:
                            tags.append(tag)
                            m.update("index", {"word": s}, {"$set": {"tag": tags}})
                            print(count, s, tags)


# seg_list = jieba.cut("我来到北京清华大学")
# str = ' '.join(seg_list)
# print (str)


def indexSearch(word):
    seg_list = jieba.cut(word)
    str = ' '.join(seg_list)
    strs = str.split(" ")
    ret = []
    hasharray = {}
    for s in strs:
        list = m.findall("index", {"word": s})
        # print (s)
        for l in list:
            tags = l["tag"]
            for t in tags:
                # ts = t.split("&&")
                # col = ts[0]
                # id = ts[1]
                # fuck = m.findone(col,{"_id":ObjectId(id)})
                if t in hasharray:
                    hasharray[t] = hasharray[t] + 1
                else:
                    hasharray[t] = 1
    hasharray = sorted(hasharray.items(), key=lambda d: d[1], reverse=True)
    i = 0
    for d, x in hasharray:
        ts = d.split("&&")
        col = ts[0]
        id = ts[1]
        fuck = m.findone(col, {"_id": ObjectId(id)})
        ret.append(fuck)
        # print(i,fuck["name"], col)
        i = i + 1
        if i > 99:
            break
    return ret
