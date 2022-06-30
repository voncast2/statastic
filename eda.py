# -*- coding: utf-8 -*-
import jieba
import synonyms
import random
from random import shuffle
import sys
import os
import time


class convertText(object):
    def edaRepalcement(self, text, stop_words, replace_num):
        #        中文同义词词典 synonyms 中文近义词工具包，可以用于自然语言理解的很多任务：文本对齐，推荐算法，相似度计算，语义偏移，关键字提取，概念提取，自动摘要，搜索引擎等。
        new_words = text.copy()
        random_word_list = list(set([word for word in text if word not in stop_words]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonym_list = synonyms.nearby(random_word)[0]  # 返回的是近义词列表 nearby 返回[[近义词],[相似值]]
            if len(synonym_list) >= 1:
                synonym = random.choice(synonym_list)  # 随机选取一个近义词
                new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
            if num_replaced >= replace_num:
                break
        sentence = ' '.join(new_words)
        sentence = sentence.strip()
        new_words = sentence.split(' ')
        return new_words  # 返回的是替换后的词的列表

    def _add_words(self, new_words):
        synonym = []
        count = 0
        while len(synonym) < 1:
            random_word = new_words[random.randint(0, len(new_words) - 1)]
            synonym = synonyms.nearby(random_word)[0]
            count += 1
            # 如果10次还没有同义词的，就返回
            if count >= 10:
                return
        random_sysnonym = random.choice(synonym)
        random_index = random.randint(0, len(new_words) - 1)
        new_words.insert(random_index, random_sysnonym)

    def edaRandomInsert(self, text, insert_num):
        new_words = text.copy()
        for num in range(insert_num):
            self._add_words(new_words)

        return new_words

    def _swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words) - 1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words) - 1)
            counter += 1
            if counter > 3:
                return new_words
            new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words

    def edaRandomSwap(self, text, swap_num):
        '''
        随即交换
        '''
        new_words = text.copy()
        for index in range(swap_num):
            new_words = self._swap_word(new_words)
        return new_words

    def edaRandomDelete(self, text, p):
        if len(text) == 1:
            return text
        new_words = []
        for word in text:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(word)
        if len(new_words) == 0:
            rand_int = random.randint(0, len(text) - 1)
            return [text[rand_int]]
        return new_words

    def load_stop_word(self, path):
        stop_words = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                stop_words.append(line)

        return stop_words

    def eda(self, text, replace_rate, add_rate, swap_rate, delete_rate):
        segment_words = jieba.lcut(text)
        num_words = len(segment_words)
        #        stop_words_path = os.path.join(sys.path[0], 'stop_words.txt')
        #        stop_words = self.load_stop_word(stop_words_path)
        stop_words = []
        replace_num = max(1, int(replace_rate * num_words))
        swap_num = max(1, int(swap_rate * num_words))
        add_num = max(1, int(add_rate * num_words))

        text_augment = []

        text_replace = ''.join(self.edaRepalcement(segment_words, stop_words, replace_num))
        text_add = ''.join(self.edaRandomInsert(segment_words, add_num))
        text_swap = ''.join(self.edaRandomSwap(segment_words, swap_num))
        text_delete = ''.join(self.edaRandomDelete(segment_words, delete_rate))

        text_augment.append(text_replace)
        text_augment.append(text_add)
        text_augment.append(text_swap)
        text_augment.append(text_delete)

        return text_augment


def eda_res(str):
    eda = convertText()
    b = random.random()
    c = random.random()
    d = random.random()
    return eda.eda(str, 0.1, b, c, d)

# test
#print(eda_res("我轻轻地走了正如我轻轻地来"))
