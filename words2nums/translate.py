#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import logging as log
import re
import string

import coloredlogs

from lang.es import numwords
from lang.es import scales
from lang.es import separator
from lang.es import units

coloredlogs.install(level='INFO')
log = log.getLogger(__name__)
locale.setlocale(locale.LC_ALL, 'es-es')

def is_avo(w=""):
    """
    Detect avo/ava numbers

    :param w: Word to test
    :return: True if is a number in the form of doce/ava/avo
    """
    return True if w.endswith('ava') or w.endswith('avo') else False


def is_numword(x):
    """
    Test if a word is in the numwords dict

    :param x: the word to test
    :return: True exist, false elsewhere
    """
    return True if x in numwords else False


def is_number(x):
    """
    Test if the word is a digit number

    :param x: word to test
    :return: True if it is a number, false elsewhere
    """
    if type(x) == str:
        x = x.replace(',', '')
    try:
        float(x)
    except:
        return False
    return True


def convert_avo(x):
    """
    Convert a /avo, /ava word into its numerical representation

    :param x: word to convert
    :return: Numerical representation, for example: once/avo -> 9.0909
    """
    n = x[:-3]
    try:
        return float(n) if is_number(n) else numwords[n]
    except KeyError:
        return x


_pat = '|'.join(r'%s$' % x for x in units)
_distance = r'(\d+) * metros *(?:y|con)? *(0\.\d+)'
_money = r'(\d+) +y? +(0\.\d+) +euros'

# try:
#     with open('cache.pickle', 'rb') as f:
#         cache = pickle.load(f)
# except FileNotFoundError:
#     cache = {}


# def _query_cache(cache: dict, k: str, v: float) -> dict:
#     k = k
#     if k not in cache:
#         cache[k] = v
#         log.info('New entry in cache %s' % cache)
#     else:
#         log.info('%s already in cache' % k)
#
#     return cache


def _sum_numbers(p: str, msg: str) -> str:
    match = re.search(p, msg, flags=re.I)

    while match:
        decimal = 0
        (ix, iix) = match.span()
        for g in match.groups():
            decimal += float(g)
        msg = '%s %s %s %s' % (msg[:ix], decimal, 'METROS' if 'metros' in p else 'euros', msg[iix:])

        match = re.search(p, msg, flags=re.I)

    return msg


def text2num(msg=""):
    """
    Transforms every number written in text with its numerical representation

    :param msg: The message to transform
    :return: The message with number in its numerical form
    """
    #
    # for i in cache.keys():
    #     msg = msg.replace(i, str(cache[i]))

    result = current = decimal = 0
    innumber = False
    indecimal = False
    prev_was_one = False
    prev_w = ''
    new_str = ''
    tmp = 0
    scale_str = ''
    text_number = ''

    detect_ones = (('un', 'una', 'uno'), ('hectarea', 'hectárea', 'metro', 'decimetro', 'euro', 'centimo', 'peseta'))
    i = 0
    acc = ''

    msg = msg.replace('%', ' PORCENTAJE')
    msg = re.sub(' +', ' ', msg)
    for w in msg.split(' '):
        plain_w = w.translate(w.maketrans('', '', string.punctuation))
        w, wl = w, plain_w.lower()
        if wl in units and not re.search(_pat, msg, flags=re.I):
            scale_str = w
            current += tmp
            tmp = 0
            continue
        if not is_numword(wl) and not prev_was_one:
            if wl == separator:
                if not innumber:
                    new_str = ' '.join([new_str, scale_str, w])
                    scale_str = ''
            elif wl in ('con', ',') and innumber:
                indecimal = True
                decimal = 0
            else:
                if is_avo(wl):
                    n = convert_avo(wl)
                    if is_number(n):
                        new_str = ' '.join([new_str, '%.4f' % (1 / n * 100)])
                    else:
                        new_str = ' '.join([new_str, w])
                else:
                    tmp = result + current + tmp + (decimal / 100 if decimal else 0)
                    resultStr = str(tmp) if tmp else ''
                    resultStr = '%s %s' % (resultStr, scale_str) if scale_str else resultStr
                    scale_str = ''
                    new_str = ' '.join([new_str, resultStr, w])
                    # if text_number:
                    #     _query_cache(cache, text_number, tmp)
                    result = current = tmp = decimal = 0
                    text_number = ''
                innumber = False
                indecimal = False
        else:
            if indecimal and wl in numwords:
                if wl in scales:
                    scale_str = w if scale_str == '' else scale_str
                    decimal = decimal * .1 if wl in ('decímetros', 'decimetros') and decimal < 10 else decimal * .01
                    current += decimal
                    decimal = 0
                    indecimal = False
                    text_number = '%s %s' % (text_number, wl)
                else:
                    decimal += numwords[wl]
                    text_number = '%s %s' % (text_number, wl)
            elif not innumber and wl in detect_ones[i] or prev_was_one:
                prev_was_one = True
                if wl in detect_ones[i]:
                    new_str = ' '.join([new_str, '1'])
                    prev_w = w
                    if i == 1:
                        new_str = ' '.join([new_str, '1', w])
                        i = 0
                    else:
                        i = 1
                elif i == 1 and not wl in scales:
                    new_str = new_str[:-1] + prev_w + ' ' + w
                    i = 0
                    prev_was_one = False
                elif wl in scales:
                    i = 0
                    new_str = new_str[:-1]
                    current += scales[wl]
                    prev_was_one = False
                    text_number = '%s %s' % (text_number, wl)
            elif wl in scales:
                current = current + tmp * scales[wl] if tmp else current + scales[wl]
                tmp = 0
                text_number = '%s %s' % (text_number, wl)
            else:
                # current += numwords[wl]
                tmp += numwords[wl]
                text_number = '%s %s' % (text_number, wl)
            innumber = True

    if current != 0:
        tmp = current + tmp
        new_str = '%s %s' % (new_str, tmp)
        # _query_cache(cache, text_number, tmp)
    elif new_str == '' and not tmp is '':
        new_str = '%s %s' % (new_str, tmp) if tmp else ''
        # _query_cache(cache, text_number, tmp)

    # with open('cache.pickle', 'wb') as f:
    #     pickle.dump(cache, f, pickle.HIGHEST_PROTOCOL)

    new_str = _sum_numbers(_distance, new_str)
    new_str = _sum_numbers(_money, new_str)

    # replace decimal numbers with comma with a dot
    # new_str = re.sub(r'(\d+),(\d+)', r'\1.\2', new_str)
    new_str = re.sub(r'euros? +de +euros?', 'euros', new_str)

    return re.sub(' +', ' ', new_str.strip())


if __name__ == '__main__':
    def test_translate():
        assert '99 PORCENTAJE' == text2num('99%')
        assert '9' == text2num('nueve')
        assert '2013' == text2num('dos mil trece')
        assert 'tengo 2 caballos' == text2num('tengo dos caballos')
        assert 'tengo 2000 casas' == text2num('tengo dos mil casas')
        assert 'unas 2405 propiedades' == text2num('unas dos mil cuatrocientas cinco propiedades')
        assert 'tengo 1800 vinos' == text2num('tengo mil ochocientos vinos')
        assert '1200000 cosas y 3 casas' == text2num('Un millón doscientas mil cosas y tres casas')
        assert '125000 cosas y 3 casas' == text2num('ciento veinticinco mil cosas y tres casas')
        assert '124.3 decimetros, tambien tengo' == text2num(
            'ciento veinticuatro con treinta decimetros, tambien tengo')
        # assert '124.3 metros tambien  tengo' == text2num('ciento veinticuatro metros treinta decimetros, tambien tengo')
        assert 'ghjghjg hj con fecha 26 DE JUNIO DEL AÑO 2013 en Granada' == text2num(
            'ghjghjg hj con fecha VEINTISÉIS DE JUNIO DEL AÑO DOS MIL TRECE en Granada')
        assert 'para responder de 1.250.000 euros de principal; intereses ordinarios durante' == text2num(
            'para responder de 1.250.000 euros de principal; intereses ordinarios durante'
        )
        assert 'de 31.224,16 Euros y demas' == text2num(
            'de 31.224,16 Euros y demas')
        assert 'con fecha 22 de Diciembre de 2010' == text2num('con fecha veintidós de Diciembre de dos mil diez')
        assert '30003' == text2num('tres hectareas y tres centiareas')
        assert 'de 205871.01 EUROS de' == \
               text2num('de DOSCIENTOS CINCO MIL OCHOCIENTOS SETENTA Y UN EUROS CON UN CENTIMO de')


    def test_ordinals():
        assert '47 es 47 aniversario' == text2num('47 es cuadragésimo séptimo aniversario')
        assert '692a es 692 (o para aniversarios: 92 del 6 centenario)' == text2num(
            '692a es sexcentésima nonagésima segunda (o para aniversarios: nonagésimo segundo del sexto centenario)')


    def test_avos():
        assert 'una 9.0909  parte' == text2num('una once/ava parte')
        assert 'una 9.0909  parte' == text2num('una once/avo parte')
        assert 'una 9.0909  parte nava' == text2num('una once/avo parte nava')


    test_translate()
    test_ordinals()
    # test_avos()
