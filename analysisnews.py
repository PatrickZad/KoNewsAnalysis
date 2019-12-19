import re
import os
import konlpy
import pandas as pd

# read file
dir = r'F:\KoNewsAnalysis\news'
givenDict = {u'一带一路': 0, u'人类命运共同体': 0, u'中国梦': 0, u'习近平思想': 0, u'强军思想': 0,
             u'贸易战': 0, u'习近平外交思想': 0, u'习近平新时代中国特色社会主义思想': 0, u'反腐败': 0}
givenRgs = {u'一带一路': [u'.*일 대 일 로'],
            u'人类命运共同体': [u'.*인 류 운 명 공 동 체'],
            u'中国梦': [u'중 국 몽'],
            u'习近平思想': [u'시 진 핑 사 상'],
            u'强军思想': [u'강 군 사 상'],
            u'贸易战': [u'무 역 전', u'무 역 전 쟁', u'무 역 분 쟁', u'무 역 갈 등'],
            u'习近平外交思想': [u'시 진 핑 외 교 사 상'],
            u'习近平新时代中国特色社会主义思想': [u'시 진 핑 신 시 대 중 국 특 색 사 회 주 의',
                                  u'시진핑 신시대 중국 특색 사회주의 사상',
                                  u'신시대 중국 특색 사회주의 사상',
                                  u'시진핑.* 신시대 중국 특색 사회주의 사상',
                                  u'시진핑의 신시대 중국 특색 사회주의 사상'],
            u'反腐败': [u'반 부 패']}
autoDict = {}
kkma = konlpy.tag.Kkma(jvmpath=r'G:\DevBase\java11\bin\server\jvm.dll')
for reglist in givenRgs.values():
    for i in range(len(reglist)):
        reglist[i] = re.compile(u'.*' + reglist[i].replace(' ', r'\s*'))
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    # regex method
    with open(filepath, 'r', encoding='utf-8') as news:
        line = news.readline()
        while len(line) > 0:
            for key, reg in givenRgs.items():
                for pattern in reg:
                    list = pattern.findall(line)
                    givenDict[key] += len(list)
            line = news.readline()
    print(filename+' regex method complete !')
    # nlp method
    with open(filepath, 'r', encoding='utf-8') as news:
        content = news.read()
        content = content.replace(r'\n', '')
        sents = kkma.sentences(content)
        for sent in sents:
            words = kkma.morphs(sent)
            for word in words:
                if word in autoDict:
                    autoDict[word] += 1
                else:
                    autoDict[word] = 1
    print(filename + ' nlp method complete !')

# save as file
data = pd.DataFrame({u'existence': pd.Series(givenDict)})
data.to_csv('given.csv')
data = pd.DataFrame({u'existence': pd.Series(autoDict)})
data.to_csv('auto.csv')
