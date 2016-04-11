# -*- coding: utf-8 -*-
"""
This program converts the cookies obtained as a string from Chrome into dictionary

Created on Thu May 21 11:16:53 2015

@author: SSunshine
"""
import string

def cookie_parser(cookie_string):
    cookie_string = cookie_string+';'
    apostrophe = string.punctuation[6]
    comma = string.punctuation[11]
    colon = string.punctuation[15]
    last_cut = 0
    for i, l in enumerate(cookie_string):
        if l == '=':
            print apostrophe+cookie_string[last_cut:i]+apostrophe+colon,
            last_cut = i+1
        elif l == ';':
            if i < len(cookie_string)-1:
                print apostrophe+cookie_string[last_cut:i]+apostrophe+comma
                last_cut= i+2
            else: 
                print apostrophe+cookie_string[last_cut:i]+apostrophe