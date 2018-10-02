#coding:utf-8
"""
author: Allen
email: 1902901293@qq.com
"""

import pygame
import pandas as pd
from io import BytesIO
import time
import os



class AudioObj(object):
    def __init__(self):
        """播放音频"""
        self.pygame_mixer = pygame.mixer
        self.pygame_mixer.init()

    def play(self, audio_bytes):
        """
        传入音频文件字节码，播放音频
        :param audio_bytes:
        :return:
        """
        if audio_bytes is None:
            return
        byte_obj = BytesIO()
        byte_obj.write(audio_bytes)
        byte_obj.seek(0, 0)
        self.pygame_mixer.music.load(byte_obj)
        self.pygame_mixer.music.play()
        while self.pygame_mixer.music.get_busy() == 1:
            time.sleep(0.1)
        self.pygame_mixer.music.stop()


class Dictionary(object):
    def __init__(self):
        self.user_home = os.path.expanduser('~')
        self.dictionary_fn = os.path.join(self.user_home, 'words_dict.pkl')
        self.dictionary_df = pd.read_pickle(self.dictionary_fn)
        self.audio = AudioObj()
        self.audio_byte = None


    def run(self):
        print("欢迎使用小词典，目前词库构建于2018年10月3日，词库根据python3官方文档构建，词库相对较小，可以自己扩展词库后再使用")
        print("按键 s 可以获取语音")
        while 1:
            input_word = input('input enlish word >>>').strip().lower()
            if input_word == 's':
                if self.audio_byte is None:
                    print('没有音频数据...')
                else:
                    self.audio.play(self.audio_byte)
                continue
            if input_word:
                cn_seq, self.audio_byte = self.filter_word(input_word)
                if not cn_seq:
                    print('没有词条数据...')
                else:
                    print(', '.join(cn_seq))


    def filter_word(self, word):
        word = word.lower().strip()
        data = self.dictionary_df[self.dictionary_df['ENGLISH_WORD'] == word].to_dict(orient='record')
        data = data[0] if data else {}
        cn_seq = data.get('CHINESE_SEQ', [])
        audio_byte = data.get('AUDIO', None)
        return cn_seq, audio_byte



if __name__ == '__main__':
    dict_work = Dictionary()
    dict_work.run()