#!/usr/bin/env python3
# ...........................................................................
# utfa.py
#
# file or web page analysis
#
# John Taylor (onefouronefour limited)
#
# 2015-11-12 22:00 first version
# 2017-04-20 18:00 -c and -C web arguments
# 2019-12-12 13:00 pre-test 'content-encoding' in response.headers
# 2019-12-12 14:40 update block names to Unicode 12.1
# ...........................................................................

from   __future__ import print_function

import os
import sys
import re
import argparse
from   math import log10
import traceback
import time

# ...........................................................................
# these two imports can be omitted and detected at runtime using tryimport
# the intention is to be python 2.7/3.* compatible
# tryimport gives a more useful error message if module missing
# ...........................................................................
import requests
import six

# ...........................................................................
# try_import
# ...........................................................................
def tryimport( m ):
    try:
        module_obj = __import__(m)
        # create a global object containing module
        globals()[m] = module_obj
    except ImportError:
        sys.exit ("""\nYou need module '%s'\n
install it from http://pypi.python.org/pypi/%s\n
or run 'pip install %s' (use pip3 for python 3.*)\n""" % (m,m,m))
# ...........................................................................

tryimport ('requests')
tryimport ('six')

# ...........................................................................
# read file as bytes
# ...........................................................................
def read_bytes( file_name ):

    global args, source_size

    try:
        if file_name == "-":
            fp = sys.stdin
        else:
            fp = open ( file_name, 'rb')
            fp.seek (args.offset)

        source_size = 0
        file_bytes = b''
        while True:
            # using a fixed chunk size could allow incremental scan to avoid reading entire file
            # into memory. but it would be necessary to detect split unicode characters (future exercise)
            chunk = fp.read (args.size )
            source_size += len( chunk )
            file_bytes = b''.join([file_bytes,chunk])
            if not chunk:
                break

        fp.close()

        return file_bytes

    except:
        traceback.print_exc()
        print ( "cannot open file {0}\n".format(file_name) )
        sys.exit ( 1 )

# ...........................................................................
# count words
#
# note that there is a python 2.7/3.3+ difference see: https://www.python.org/dev/peps/pep-0414/
# test versions and utf-8/binary variants: word_test.sh utfa.py
# arithmetic matches wc
# ...........................................................................
def count_words( source_bytes ):

    global args

    # unicode difference
    if six.PY2:
        if args.bytes:
            s_words = re.split(r"[\s\t]+", source_bytes)
        else:
            s_words = re.split(r"[\s\t]+", source_bytes, flags=re.UNICODE)
    else:
        if args.bytes:
            s_words = re.split(br"[\s\t]+", source_bytes)
        else:
            s_words = re.split(br"[\s\t]+", source_bytes, flags=0)

    word_count = len(s_words) - 1

    return word_count

# ...........................................................................
# populate file_dict from byte values
# ...........................................................................
def gen_dict ( file_bytes ):

    file_dict = {}

    for c in file_bytes:
        if not c in file_dict:
            file_dict[ c ] = 0
        file_dict[ c ] += 1

    return file_dict

# ...........................................................................
# populate file_dict from unicode and rows_dict for ranges of unicode
# ...........................................................................
# noinspection PyCompatibility
def gen_utf8 ( file_bytes ):

    global args

    file_dict = {}
    rows_dict = {}

    # convert to utf-8

    errors = 'strict'
    if args.errors:
        errors = 'replace'

    try:
        file_utf8 = file_bytes.decode('utf-8', errors)
        pass

    except UnicodeDecodeError:
        print ( "file {0} is not valid utf-8, try analysing file as bytes using flag -b or enable error replacement with flag -e\n".format(source))
        sys.exit ( 2 )
    except:
        traceback.print_exc()
        sys.exit ( 1 )

    for c in file_utf8:
        if not c in file_dict:
            file_dict[ c ] = 0
        file_dict[ c ] += 1
        if c > six.unichr(0x7f):
            cp = ord( c )
            cp = ( int( cp / 16 ) ) * 16

            rows_dict[ six.unichr( cp ) ] = True

    return ( file_dict, rows_dict )

# ...........................................................................
# display 256 byte positions
# ...........................................................................
def show_file ( file_dict, word_count ):

    global args, source, source_size

    maxval = max( file_dict.values())

    lmax = int( log10(maxval) ) + 2

    head_format = "{" + ("0:>%d" % lmax) + "s}"
    body_format = "{" + ("0:%d" % lmax) + "d}"

    # print output
    print ( "\nbyte analysis for {0}\n".format(source) )

    print ( "       ", end=''  )
    if args.number:
        for i in range (0,16):
            print ( head_format.format( dx(i) ), end='' )
    else:
        print ( "total", end='' )

    if args.legend:
        print ( "\t\t-- characters --\n" )
    else:
        print ( '\n' )

    for i in range (0,16):
        row_total=0
        print ( "     {0:1s} ".format(dx(i)), end='' )
        legend=''
        for j in range (0,16):

            k = 16*i + j
            cp = k

            if six.PY2:
                s = chr(k)
            else:
                s = k

            if s in file_dict:
                if (i < 2) or (i > 7 and i < 10):
                    legend += '.'
                else:
                    legend += six.unichr(cp)
                num = file_dict[ s ]
                row_total += num
                if args.number:
                    print( body_format.format( num ), end='' )
            else:
                if args.mask:
                    legend += ' '
                else:
                    if (i < 2) or (i > 7 and i < 10):
                        legend += '.'
                    else:
                        legend += six.unichr(cp)
                if args.number:
                    print( body_format.format( 0 ), end='' )

        if not args.number:
            print( body_format.format( row_total ), end='' )

        if i < 8:
            if args.legend:
                print ( "\t\t{0}\n".format(legend), end='' )
            else:
                print ( '\n', end='' )
        else:
            if args.legend:
                value = set_value( legend )
                print ( "\t\t{0}\n".format(value), end='' )
            else:
                print ( '\n', end='' )

    print( "\ntotal bytes : {0:d}".format( source_size ))
    if args.words:
        print( "total words : {0:d}".format( word_count ))
    print ( '\n', end='' )

    return

# ...........................................................................
# display unicode values
# ...........................................................................
def show_utf8 ( file_dict, word_count, rows_dict ):

    global args, source, source_size, block_index

    char_count = 0

    dict_list = list( rows_dict )
    dict_list.sort()

    maxval = max( file_dict.values())

    block_format = ""

    if args.name:
        maxnamelen = max( 20, len(block_name( 0 )))
        for k in ''.join( dict_list ):
            cp = ord( k )
            cp = ( int( cp / 16 ) ) * 16
            code_len=len(block_name( cp ))
            maxnamelen = max( code_len, maxnamelen )

        block_format = "{w}".format( w = maxnamelen )

        # reset index so that block_name() can scan forwards again
        block_index = 0

    lmax = int( log10(maxval) ) + 2

    head_format = "{" + ("0:>%d" % lmax) + "s}"
    body_format = "{" + ("0:%d" % lmax) + "d}"

    # print output
    print ( "\nunicode analysis for {0}\t".format(source), end="" )

    if six.PY2:
        print ( "(running Python 2 : showing Basic Multilingual Plane including surrogate pairs)\n" )
    else:
        print ( "(running Python 3)\n" )

    print ( "        ", end=''  )

    if args.number:
        for i in range (0,16):
            print ( head_format.format( dx(i) ), end='')
    else:
        print ( "total", end='' )

    if args.name:
        print ( ("\t{0:<" + block_format + "}").format("-- unicode block --"), end='')
    if args.legend:
        print ( " \t-- characters --\n" )
    else:
        print ( '\n' )

    # ...........................................................................
    # show characters in range 0x0 to 0x7f
    # ...........................................................................
    for i in range (0,8):

        row_total=0
        legend=''

        print ( "{0:>7} ".format(dx(i)), end='' )

        code_name = block_name( 0 )

        for j in range (0,16):

            s = chr(16*i + j)

            if s in file_dict:
                if i < 2:
                    legend += '.'
                else:
                    # test for delete
                    if s == chr(127):
                        legend += ' '
                    else:
                        legend += s

                num = file_dict[ s ]
                char_count += num
                row_total += num
                if args.number:
                    print( body_format.format(num), end='' )
            else:
                if args.mask:
                    legend += ' '
                else:
                    if i < 2:
                        legend += '.'
                    else:
                        # test for delete
                        if s == chr(127):
                            legend += ' '
                        else:
                            legend += s

                if args.number:
                    print( body_format.format( 0 ), end='' )

        if not args.number:
            print( body_format.format(row_total), end='' )

        if args.name:
            print ( ("\t{0:<" + block_format + "}").format(code_name), end='')
        if args.legend:
            value = set_value( legend )
            print ( " \t{0}\n".format(value), end='' )
        else:
            print ( '\n', end='' )

    # ...........................................................................
    # show characters above 0x7f
    # ...........................................................................
    for k in ''.join( dict_list ):
        legend=''
        row_total = 0
        cp = ord( k )
        cp = ( int( cp / 16 ) ) * 16

        print ( "{0:>7} ".format(str( hex (cp) )), end='' )

        code_name = block_name( cp )

        for j in range (cp,cp+16):

            s = six.unichr(j)

            if s in file_dict:
                if s < six.unichr(0xa0):
                    legend += '.'
                else:
                    legend += s

                num = file_dict[ s ]
                char_count += num
                row_total += num
                if args.number:
                    print( body_format.format( num ), end='' )
            else:
                if args.mask:
                    legend += ' '
                else:
                    if s < six.unichr(0xa0):
                        legend += '.'
                    else:
                        legend += s
                if args.number:
                    print( body_format.format( 0 ), end='' )

        if not args.number:
            print( body_format.format( row_total ), end='' )

        if args.name:
            print ( ("\t{0:<" + block_format + "}").format(code_name), end='')
        if args.legend:
            value = set_value( legend )
            print ( " \t{0}\n".format(value), end='' )
        else:
            print ( '\n', end='' )

    print( "\ntotal bytes      : {0:d}".format( source_size ))
    if args.words:
        print( "total words      : {0:d}".format( word_count ))
    print( "total characters : {0:d}\n".format( char_count ))

    return

# ...........................................................................
# display unicode values according to python version
# ...........................................................................
def set_value ( legend ):
    if six.PY2:
        value = legend.encode("utf-8")
    else:
        value = legend
    return value

# ...........................................................................
# lookup code block name
# ...........................................................................
def block_name( cp ):

    global blocks, block_index

    code_name = ''

    if cp == None:
        code_name = 'No_Block'
    else:
        code_tuple = blocks[block_index]
        if cp >= code_tuple[ 0 ] and cp < code_tuple[ 1 ]:
            code_name  = code_tuple[2]
        else:
            # only go forward
            while True:
                block_index = block_index + 1
                code_tuple = blocks[block_index]
                if cp >= code_tuple[ 0 ] and cp < code_tuple[ 1 ]:
                    code_name  = code_tuple[2]
                    break

    return code_name

# ...........................................................................
# 2019-05-07 populate block name Unicode 12.1.0 : http://unicode.org/versions/Unicode12.1.0/
# 2020-03-10 populate block name Unicode 13.0.0 : http://unicode.org/versions/Unicode13.0.0/
# ...........................................................................
def populate_block_name():

    global blocks

    # @missing: 0000..10FFFF; No_Block

    blocks = [
                (0x0000,0x007F,"Basic Latin"),
                (0x0080,0x00FF,"Latin-1 Supplement"),
                (0x0100,0x017F,"Latin Extended-A"),
                (0x0180,0x024F,"Latin Extended-B"),
                (0x0250,0x02AF,"IPA Extensions"),
                (0x02B0,0x02FF,"Spacing Modifier Letters"),
                (0x0300,0x036F,"Combining Diacritical Marks"),
                (0x0370,0x03FF,"Greek and Coptic"),
                (0x0400,0x04FF,"Cyrillic"),
                (0x0500,0x052F,"Cyrillic Supplement"),
                (0x0530,0x058F,"Armenian"),
                (0x0590,0x05FF,"Hebrew"),
                (0x0600,0x06FF,"Arabic"),
                (0x0700,0x074F,"Syriac"),
                (0x0750,0x077F,"Arabic Supplement"),
                (0x0780,0x07BF,"Thaana"),
                (0x07C0,0x07FF,"NKo"),
                (0x0800,0x083F,"Samaritan"),
                (0x0840,0x085F,"Mandaic"),
                (0x08A0,0x08FF,"Arabic Extended-A"),
                (0x0900,0x097F,"Devanagari"),
                (0x0980,0x09FF,"Bengali"),
                (0x0A00,0x0A7F,"Gurmukhi"),
                (0x0A80,0x0AFF,"Gujarati"),
                (0x0B00,0x0B7F,"Oriya"),
                (0x0B80,0x0BFF,"Tamil"),
                (0x0C00,0x0C7F,"Telugu"),
                (0x0C80,0x0CFF,"Kannada"),
                (0x0D00,0x0D7F,"Malayalam"),
                (0x0D80,0x0DFF,"Sinhala"),
                (0x0E00,0x0E7F,"Thai"),
                (0x0E80,0x0EFF,"Lao"),
                (0x0F00,0x0FFF,"Tibetan"),
                (0x1000,0x109F,"Myanmar"),
                (0x10A0,0x10FF,"Georgian"),
                (0x1100,0x11FF,"Hangul Jamo"),
                (0x1200,0x137F,"Ethiopic"),
                (0x1380,0x139F,"Ethiopic Supplement"),
                (0x13A0,0x13FF,"Cherokee"),
                (0x1400,0x167F,"Unified Canadian Aboriginal Syllabics"),
                (0x1680,0x169F,"Ogham"),
                (0x16A0,0x16FF,"Runic"),
                (0x1700,0x171F,"Tagalog"),
                (0x1720,0x173F,"Hanunoo"),
                (0x1740,0x175F,"Buhid"),
                (0x1760,0x177F,"Tagbanwa"),
                (0x1780,0x17FF,"Khmer"),
                (0x1800,0x18AF,"Mongolian"),
                (0x18B0,0x18FF,"Unified Canadian Aboriginal Syllabics Extended"),
                (0x1900,0x194F,"Limbu"),
                (0x1950,0x197F,"Tai Le"),
                (0x1980,0x19DF,"New Tai Lue"),
                (0x19E0,0x19FF,"Khmer Symbols"),
                (0x1A00,0x1A1F,"Buginese"),
                (0x1A20,0x1AAF,"Tai Tham"),
                (0x1AB0,0x1AFF,"Combining Diacritical Marks Extended"),
                (0x1B00,0x1B7F,"Balinese"),
                (0x1B80,0x1BBF,"Sundanese"),
                (0x1BC0,0x1BFF,"Batak"),
                (0x1C00,0x1C4F,"Lepcha"),
                (0x1C50,0x1C7F,"Ol Chiki"),
                (0x1CC0,0x1CCF,"Sundanese Supplement"),
                (0x1CD0,0x1CFF,"Vedic Extensions"),
                (0x1D00,0x1D7F,"Phonetic Extensions"),
                (0x1D80,0x1DBF,"Phonetic Extensions Supplement"),
                (0x1DC0,0x1DFF,"Combining Diacritical Marks Supplement"),
                (0x1E00,0x1EFF,"Latin Extended Additional"),
                (0x1F00,0x1FFF,"Greek Extended"),
                (0x2000,0x206F,"General Punctuation"),
                (0x2070,0x209F,"Superscripts and Subscripts"),
                (0x20A0,0x20CF,"Currency Symbols"),
                (0x20D0,0x20FF,"Combining Diacritical Marks for Symbols"),
                (0x2100,0x214F,"Letterlike Symbols"),
                (0x2150,0x218F,"Number Forms"),
                (0x2190,0x21FF,"Arrows"),
                (0x2200,0x22FF,"Mathematical Operators"),
                (0x2300,0x23FF,"Miscellaneous Technical"),
                (0x2400,0x243F,"Control Pictures"),
                (0x2440,0x245F,"Optical Character Recognition"),
                (0x2460,0x24FF,"Enclosed Alphanumerics"),
                (0x2500,0x257F,"Box Drawing"),
                (0x2580,0x259F,"Block Elements"),
                (0x25A0,0x25FF,"Geometric Shapes"),
                (0x2600,0x26FF,"Miscellaneous Symbols"),
                (0x2700,0x27BF,"Dingbats"),
                (0x27C0,0x27EF,"Miscellaneous Mathematical Symbols-A"),
                (0x27F0,0x27FF,"Supplemental Arrows-A"),
                (0x2800,0x28FF,"Braille Patterns"),
                (0x2900,0x297F,"Supplemental Arrows-B"),
                (0x2980,0x29FF,"Miscellaneous Mathematical Symbols-B"),
                (0x2A00,0x2AFF,"Supplemental Mathematical Operators"),
                (0x2B00,0x2BFF,"Miscellaneous Symbols and Arrows"),
                (0x2C00,0x2C5F,"Glagolitic"),
                (0x2C60,0x2C7F,"Latin Extended-C"),
                (0x2C80,0x2CFF,"Coptic"),
                (0x2D00,0x2D2F,"Georgian Supplement"),
                (0x2D30,0x2D7F,"Tifinagh"),
                (0x2D80,0x2DDF,"Ethiopic Extended"),
                (0x2DE0,0x2DFF,"Cyrillic Extended-A"),
                (0x2E00,0x2E7F,"Supplemental Punctuation"),
                (0x2E80,0x2EFF,"CJK Radicals Supplement"),
                (0x2F00,0x2FDF,"Kangxi Radicals"),
                (0x2FF0,0x2FFF,"Ideographic Description Characters"),
                (0x3000,0x303F,"CJK Symbols and Punctuation"),
                (0x3040,0x309F,"Hiragana"),
                (0x30A0,0x30FF,"Katakana"),
                (0x3100,0x312F,"Bopomofo"),
                (0x3130,0x318F,"Hangul Compatibility Jamo"),
                (0x3190,0x319F,"Kanbun"),
                (0x31A0,0x31BF,"Bopomofo Extended"),
                (0x31C0,0x31EF,"CJK Strokes"),
                (0x31F0,0x31FF,"Katakana Phonetic Extensions"),
                (0x3200,0x32FF,"Enclosed CJK Letters and Months"),
                (0x3300,0x33FF,"CJK Compatibility"),
                (0x3400,0x4DBF,"CJK Unified Ideographs Extension A"),
                (0x4DC0,0x4DFF,"Yijing Hexagram Symbols"),
                (0x4E00,0x9FFF,"CJK Unified Ideographs"),
                (0xA000,0xA48F,"Yi Syllables"),
                (0xA490,0xA4CF,"Yi Radicals"),
                (0xA4D0,0xA4FF,"Lisu"),
                (0xA500,0xA63F,"Vai"),
                (0xA640,0xA69F,"Cyrillic Extended-B"),
                (0xA6A0,0xA6FF,"Bamum"),
                (0xA700,0xA71F,"Modifier Tone Letters"),
                (0xA720,0xA7FF,"Latin Extended-D"),
                (0xA800,0xA82F,"Syloti Nagri"),
                (0xA830,0xA83F,"Common Indic Number Forms"),
                (0xA840,0xA87F,"Phags-pa"),
                (0xA880,0xA8DF,"Saurashtra"),
                (0xA8E0,0xA8FF,"Devanagari Extended"),
                (0xA900,0xA92F,"Kayah Li"),
                (0xA930,0xA95F,"Rejang"),
                (0xA960,0xA97F,"Hangul Jamo Extended-A"),
                (0xA980,0xA9DF,"Javanese"),
                (0xA9E0,0xA9FF,"Myanmar Extended-B"),
                (0xAA00,0xAA5F,"Cham"),
                (0xAA60,0xAA7F,"Myanmar Extended-A"),
                (0xAA80,0xAADF,"Tai Viet"),
                (0xAAE0,0xAAFF,"Meetei Mayek Extensions"),
                (0xAB00,0xAB2F,"Ethiopic Extended-A"),
                (0xAB30,0xAB6F,"Latin Extended-E"),
                (0xABC0,0xABFF,"Meetei Mayek"),
                (0xAC00,0xD7AF,"Hangul Syllables"),
                (0xD7B0,0xD7FF,"Hangul Jamo Extended-B"),
                (0xD800,0xDB7F,"High Surrogates"),
                (0xDB80,0xDBFF,"High Private Use Surrogates"),
                (0xDC00,0xDFFF,"Low Surrogates"),
                (0xE000,0xF8FF,"Private Use Area"),
                (0xF900,0xFAFF,"CJK Compatibility Ideographs"),
                (0xFB00,0xFB4F,"Alphabetic Presentation Forms"),
                (0xFB50,0xFDFF,"Arabic Presentation Forms-A"),
                (0xFE00,0xFE0F,"Variation Selectors"),
                (0xFE10,0xFE1F,"Vertical Forms"),
                (0xFE20,0xFE2F,"Combining Half Marks"),
                (0xFE30,0xFE4F,"CJK Compatibility Forms"),
                (0xFE50,0xFE6F,"Small Form Variants"),
                (0xFE70,0xFEFF,"Arabic Presentation Forms-B"),
                (0xFF00,0xFFEF,"Halfwidth and Fullwidth Forms"),
                (0xFFF0,0xFFFF,"Specials"),
                (0x10000,0x1007F,"Linear B Syllabary"),
                (0x10080,0x100FF,"Linear B Ideograms"),
                (0x10100,0x1013F,"Aegean Numbers"),
                (0x10140,0x1018F,"Ancient Greek Numbers"),
                (0x10190,0x101CF,"Ancient Symbols"),
                (0x101D0,0x101FF,"Phaistos Disc"),
                (0x10280,0x1029F,"Lycian"),
                (0x102A0,0x102DF,"Carian"),
                (0x102E0,0x102FF,"Coptic Epact Numbers"),
                (0x10300,0x1032F,"Old Italic"),
                (0x10330,0x1034F,"Gothic"),
                (0x10350,0x1037F,"Old Permic"),
                (0x10380,0x1039F,"Ugaritic"),
                (0x103A0,0x103DF,"Old Persian"),
                (0x10400,0x1044F,"Deseret"),
                (0x10450,0x1047F,"Shavian"),
                (0x10480,0x104AF,"Osmanya"),
                (0x10500,0x1052F,"Elbasan"),
                (0x10530,0x1056F,"Caucasian Albanian"),
                (0x10600,0x1077F,"Linear A"),
                (0x10800,0x1083F,"Cypriot Syllabary"),
                (0x10840,0x1085F,"Imperial Aramaic"),
                (0x10860,0x1087F,"Palmyrene"),
                (0x10880,0x108AF,"Nabataean"),
                (0x10900,0x1091F,"Phoenician"),
                (0x10920,0x1093F,"Lydian"),
                (0x10980,0x1099F,"Meroitic Hieroglyphs"),
                (0x109A0,0x109FF,"Meroitic Cursive"),
                (0x10A00,0x10A5F,"Kharoshthi"),
                (0x10A60,0x10A7F,"Old South Arabian"),
                (0x10A80,0x10A9F,"Old North Arabian"),
                (0x10AC0,0x10AFF,"Manichaean"),
                (0x10B00,0x10B3F,"Avestan"),
                (0x10B40,0x10B5F,"Inscriptional Parthian"),
                (0x10B60,0x10B7F,"Inscriptional Pahlavi"),
                (0x10B80,0x10BAF,"Psalter Pahlavi"),
                (0x10C00,0x10C4F,"Old Turkic"),
                (0x10E60,0x10E7F,"Rumi Numeral Symbols"),
                (0x10E80,0x10EBF,"Yezidi"),
                (0x11000,0x1107F,"Brahmi"),
                (0x11080,0x110CF,"Kaithi"),
                (0x110D0,0x110FF,"Sora Sompeng"),
                (0x11100,0x1114F,"Chakma"),
                (0x11150,0x1117F,"Mahajani"),
                (0x11180,0x111DF,"Sharada"),
                (0x111E0,0x111FF,"Sinhala Archaic Numbers"),
                (0x11200,0x1124F,"Khojki"),
                (0x112B0,0x112FF,"Khudawadi"),
                (0x11300,0x1137F,"Grantha"),
                (0x11480,0x114DF,"Tirhuta"),
                (0x11580,0x115FF,"Siddham"),
                (0x11600,0x1165F,"Modi"),
                (0x11680,0x116CF,"Takri"),
                (0x118A0,0x118FF,"Warang Citi"),
                (0x11AC0,0x11AFF,"Pau Cin Hau"),
                (0x12000,0x123FF,"Cuneiform"),
                (0x12400,0x1247F,"Cuneiform Numbers and Punctuation"),
                (0x13000,0x1342F,"Egyptian Hieroglyphs"),
                (0x16800,0x16A3F,"Bamum Supplement"),
                (0x16A40,0x16A6F,"Mro"),
                (0x16AD0,0x16AFF,"Bassa Vah"),
                (0x16B00,0x16B8F,"Pahawh Hmong"),
                (0x16F00,0x16F9F,"Miao"),
                (0x1B000,0x1B0FF,"Kana Supplement"),
                (0x1BC00,0x1BC9F,"Duployan"),
                (0x1BCA0,0x1BCAF,"Shorthand Format Controls"),
                (0x1D000,0x1D0FF,"Byzantine Musical Symbols"),
                (0x1D100,0x1D1FF,"Musical Symbols"),
                (0x1D200,0x1D24F,"Ancient Greek Musical Notation"),
                (0x1D300,0x1D35F,"Tai Xuan Jing Symbols"),
                (0x1D360,0x1D37F,"Counting Rod Numerals"),
                (0x1D400,0x1D7FF,"Mathematical Alphanumeric Symbols"),
                (0x1E800,0x1E8DF,"Mende Kikakui"),
                (0x1EE00,0x1EEFF,"Arabic Mathematical Alphabetic Symbols"),
                (0x1F000,0x1F02F,"Mahjong Tiles"),
                (0x1F030,0x1F09F,"Domino Tiles"),
                (0x1F0A0,0x1F0FF,"Playing Cards"),
                (0x1F100,0x1F1FF,"Enclosed Alphanumeric Supplement"),
                (0x1F200,0x1F2FF,"Enclosed Ideographic Supplement"),
                (0x1F300,0x1F5FF,"Miscellaneous Symbols and Pictographs"),
                (0x1F600,0x1F64F,"Emoticons"),
                (0x1F650,0x1F67F,"Ornamental Dingbats"),
                (0x1F680,0x1F6FF,"Transport and Map Symbols"),
                (0x1F700,0x1F77F,"Alchemical Symbols"),
                (0x1F780,0x1F7FF,"Geometric Shapes Extended"),
                (0x1F800,0x1F8FF,"Supplemental Arrows-C"),
                (0x1F900,0x1F9FF,"Supplemental Symbols and Pictographs"),
                (0x1FA00,0x1FA6F,"Chess Symbols"),
                (0x1FA70,0x1FAFF,"Symbols and Pictographs Extended-A"),
                (0x1FB00,0x1FBFF,"Symbols for Legacy Computing"),
                (0x20000,0x2A6DF,"CJK Unified Ideographs Extension B"),
                (0x2A700,0x2B73F,"CJK Unified Ideographs Extension C"),
                (0x2B740,0x2B81F,"CJK Unified Ideographs Extension D"),
                (0x2B820,0x2CEAF,"CJK Unified Ideographs Extension E"),
                (0x2CEB0,0x2EBEF,"CJK Unified Ideographs Extension F"),
                (0x2F800,0x2FA1F,"CJK Compatibility Ideographs Supplement"),
                (0x30000,0x3134F,"CJK Unified Ideographs Extension G"),
                (0xE0000,0xE007F,"Tags"),
                (0xE0100,0xE01EF,"Variation Selectors Supplement"),
                (0xF0000,0xFFFFF,"Supplementary Private Use Area-A"),
                (0x100000,0x10FFFF,"Supplementary Private Use Area-B")
             ]

# ...........................................................................
# lookup hex string
# ...........................................................................
def dx(d):
    return "0123456789abcdef"[d:d+1]

# ...........................................................................
# main()
# ...........................................................................
def main():

    global args, source, source_size, file_dict, block_index

    time_start = time.time()

    populate_block_name()
    block_index = 0

    parser = argparse.ArgumentParser(description='file analysis')
    parser.add_argument("-u", "--url",     action="store",                      help="url e.g. -u http://bbc.co.uk")
    parser.add_argument("-c", "--code",    action="store_true",  default=False, help="show web encoding")
    parser.add_argument("-C", "--xcode",   action="store_true",  default=False, help="show extra web headers")
    parser.add_argument("-b", "--bytes",   action="store_true",  default=False, help="analyse 256 possible bit patterns")
    parser.add_argument("-e", "--errors",  action="store_true",  default=False, help="enable unicode error replacement")
    parser.add_argument("-t", "--time",    action="store_true",                 help="show run time")
    parser.add_argument("-w", "--words",   action="store_true",                 help="show word count")
    parser.add_argument("-l", "--legend",  action="store_false", default=True,  help="disable legend display")
    parser.add_argument("-n", "--name",    action="store_false", default=True,  help="disable unicode block names")
    parser.add_argument("-m", "--mask",    action="store_true",  default=False, help="show only characters present in file/url")
    parser.add_argument("-x", "--number",  action="store_false", default=True,  help="disable individual counts")
    parser.add_argument("-o", "--offset",  action="store",       type=int, default=0)
    parser.add_argument("-s", "--size",    action="store",       type=int, default=-1)
    parser.add_argument("-v", "--version", action="store_true",  default=False, help="python version, encoding and max code point")
    parser.add_argument( 'file', nargs='?', default=None )

    args = parser.parse_args()

    if args.version:
        print ("\n{0}".format(sys.version_info))
        print ("default encoding {0}".format(sys.getdefaultencoding()))
        print ("maximum Unicode code point {0}".format(hex(sys.maxunicode)))

    # ...........................................................................
    # analyse url or file
    # ...........................................................................
    if args.url:

        response = requests.get(args.url)
        source_bytes = response.content
#       source_bytes = response.text
#       enc = response.encoding

        if args.code or args.xcode:
            print("\n         encoding : {0}".format(response.encoding))
            print("apparent encoding : {0}".format(response.apparent_encoding))
            if 'content-encoding' in response.headers:
                print(  " content encoding : {0}".format(response.headers['content-encoding']))

            if args.xcode:
                print("")
                for rkey in sorted(response.headers):
#                   if not rkey.lower() == 'content-encoding':
                    print("  response header : {0} : {1}".format(rkey,response.headers[rkey]))

        source = args.url
        source_size=len(source_bytes)

    else:
        if args.file == None:
            print ("no filename given, pwd = ", os.getcwd())
            sys.exit ( 1 )

        source = args.file
        source_bytes = read_bytes(args.file)

    # ...........................................................................

    word_count = -1
    if args.words:
        word_count = count_words( source_bytes )

    # ...........................................................................

    if args.bytes:
        file_dict = gen_dict(source_bytes)
        show_file(file_dict, word_count)
    else:
        (file_dict, rows_dict) = gen_utf8(source_bytes)
        show_utf8(file_dict, word_count, rows_dict)

    time_end = time.time()

    if args.time:
        print ( "{0:0.2f} seconds".format(time_end - time_start))

# ...........................................................................

if __name__ == '__main__':
    main()

# ...........................................................................
