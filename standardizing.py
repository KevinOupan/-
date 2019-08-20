import jieba
from gensim import corpora, models, similarities
import numpy as np


class Sim():
    def __init__(self, str_single, str_group, y_stan):
        """读取文件，得到词组"""
        self.str_single = str_single
        self.str_group = str_group
        self.y_stan = y_stan
        self.str_goal = jieba.cut(self.str_single)
        self.word_goal = ""
        self.m = len(self.str_group)
        for word in self.str_goal:
            self.word_goal += word + " "
        self.word_group = []
        for i in range(self.m):
            words = jieba.cut(str(np.array(self.str_group)[i]))
            some = ""
            for word in words:
                some += word + " "
            self.word_group.append(some)

    def word_list(self):
        """分词得到词库"""
        self.texts = [[word for word in document.split()] for document in self.word_group]
        self.dictionary = corpora.Dictionary(self.texts)
        return self.dictionary

    def simi_compute(self):
        """计算str_single分别与str_group中每个元素的相似度"""
        new_xs = self.dictionary.doc2bow(self.word_goal.split())
        corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        tfidf = models.TfidfModel(corpus)
        featurenum = len(self.dictionary.token2id.keys())
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featurenum)
        self.sim = list(index[tfidf[new_xs]])

    def standard(self):
        """匹配非标准数据中最大相似度的标准值"""
        value = max(self.sim)
        index = self.sim.index(value)
        self.y_fore = np.array(self.y_stan)[index]

    def run(self):
        """类中主程序"""
        self.word_list()
        self.simi_compute()
        self.standard()
        return self.y_fore

