utfa
====

**UTF-8 analysis for files and web pages**

utfa.py is a Python script which analyses files or web pages into counts of all UTF-8 characters.  It can also (using -b byte mode) analyse the data into component bytes, e.g. where a file or web page is not encoded using UTF-8.

See the document `ufta.pdf` for background and usage examples using supplied test files `256` and `u256` and various web pages.

utfa.py supports both Python 2.7 and Python 3.x versions.  

Examples:

  * utfa.py u256
```
unicode analysis for u256	(running Python 3)

         0 1 2 3 4 5 6 7 8 9 a b c d e f	-- unicode block -- 	-- characters --

      0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	................
      1  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	................
      2  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	 !"#$%&'()*+,-./
      3  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	0123456789:;<=>?
      4  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	@ABCDEFGHIJKLMNO
      5  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	PQRSTUVWXYZ[\]^_
      6  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	`abcdefghijklmno
      7  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Basic Latin         	pqrstuvwxyz{|}~ 
   0x80  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	................
   0x90  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	................
   0xa0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	 ¡¢£¤¥¦§¨©ª«¬­®¯
   0xb0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	°±²³´µ¶·¸¹º»¼½¾¿
   0xc0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ
   0xd0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß
   0xe0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	àáâãäåæçèéêëìíîï
   0xf0  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1	Latin-1 Supplement  	ðñòóôõö÷øùúûüýþÿ

total bytes      : 384
total characters : 256
```
  * utfa.py -u http://www.bbc.co.uk/news -xm
```
unicode analysis for http://www.bbc.co.uk/news	(running Python 3)

        total	-- unicode block -- 	-- characters --

      0   2538	Basic Latin         	         ..     
      1      0	Basic Latin         	                
      2  71315	Basic Latin         	 !"#$%&'()*+,-./
      3  16958	Basic Latin         	0123456789:;<=>?
      4   2624	Basic Latin         	@ABCDEFGHIJKLMNO
      5   3864	Basic Latin         	PQRSTUVWXYZ[\]^_
      6  66331	Basic Latin         	 abcdefghijklmno
      7  33492	Basic Latin         	pqrstuvwxyz{|}  
   0xa0      1	Latin-1 Supplement  	   £            

total bytes      : 197124
total characters : 197123
```

  * utfa.py -u https://en.wikipedia.org/wiki/UTF-8 -xm
```

unicode analysis for https://en.wikipedia.org/wiki/UTF-8	(running Python 3)

        total	-- unicode block --      	-- characters --

      0   3859	Basic Latin              	................
      1      0	Basic Latin              	................
      2  41378	Basic Latin              	 !"#$%&'()*+,-./
      3  41738	Basic Latin              	0123456789:;<=>?
      4   6756	Basic Latin              	@ABCDEFGHIJKLMNO
      5   5618	Basic Latin              	PQRSTUVWXYZ[\]^_
      6 109134	Basic Latin              	`abcdefghijklmno
      7  48008	Basic Latin              	pqrstuvwxyz{|}~ 
   0xa0     13	Latin-1 Supplement       	 ¡¢£¤¥¦§¨©ª«¬­®¯
   0xb0      4	Latin-1 Supplement       	°±²³´µ¶·¸¹º»¼½¾¿
   0xc0      1	Latin-1 Supplement       	ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ
   0xd0      1	Latin-1 Supplement       	ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß
   0xe0      8	Latin-1 Supplement       	àáâãäåæçèéêëìíîï
   0xf0      8	Latin-1 Supplement       	ðñòóôõö÷øùúûüýþÿ
  0x100     11	Latin Extended-A         	ĀāĂăĄąĆćĈĉĊċČčĎď
  0x120      3	Latin Extended-A         	ĠġĢģĤĥĦħĨĩĪīĬĭĮį
  0x150      2	Latin Extended-A         	ŐőŒœŔŕŖŗŘřŚśŜŝŞş
  0x160      3	Latin Extended-A         	ŠšŢţŤťŦŧŨũŪūŬŭŮů
  0x170      1	Latin Extended-A         	ŰűŲųŴŵŶŷŸŹźŻżŽžſ
  0x250      1	IPA Extensions           	ɐɑɒɓɔɕɖɗɘəɚɛɜɝɞɟ
  0x390      1	Greek and Coptic         	ΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟ
  0x3a0      1	Greek and Coptic         	ΠΡ΢ΣΤΥΦΧΨΩΪΫάέήί
  0x3b0      6	Greek and Coptic         	ΰαβγδεζηθικλμνξο
  0x410      1	Cyrillic                 	АБВГДЕЖЗИЙКЛМНОП
  0x420      4	Cyrillic                 	РСТУФХЦЧШЩЪЫЬЭЮЯ
  0x430     20	Cyrillic                 	абвгдежзийклмноп
  0x440     12	Cyrillic                 	рстуфхцчшщъыьэюя
  0x450      1	Cyrillic                 	ѐёђѓєѕіїјљњћќѝўџ
  0x4d0      1	Cyrillic                 	ӐӑӒӓӔӕӖӗӘәӚӛӜӝӞӟ
  0x5d0      2	Hebrew                   	אבגדהוזחטיךכלםמן
  0x5e0      3	Hebrew                   	נסעףפץצקרשת׫׬׭׮ׯ
  0x620     13	Arabic                   	ؠءآأؤإئابةتثجحخد
  0x630      6	Arabic                   	ذرزسشصضطظعغػؼؽؾؿ
  0x640     13	Arabic                   	ـفقكلمنهوىيًٌٍَُ
  0x6c0      3	Arabic                   	ۀہۂۃۄۅۆۇۈۉۊۋیۍێۏ
  0x6f0      1	Arabic                   	۰۱۲۳۴۵۶۷۸۹ۺۻۼ۽۾ۿ
  0x910      4	Devanagari               	ऐऑऒओऔकखगघङचछजझञट
  0x920     12	Devanagari               	ठडढणतथदधनऩपफबभमय
  0x930      4	Devanagari               	रऱलळऴवशषसहऺऻ़ऽाि
  0x940      8	Devanagari               	ीुूृॄॅॆेैॉॊोौ्ॎॏ
  0xd00      2	Malayalam                	ഀഁംഃഄഅആഇഈഉഊഋഌ഍എഏ
  0xd10      1	Malayalam                	ഐ഑ഒഓഔകഖഗഘങചഛജഝഞട
  0xd20      4	Malayalam                	ഠഡഢണതഥദധനഩപഫബഭമയ
  0xd30      4	Malayalam                	രറലളഴവശഷസഹഺ഻഼ഽാി
  0xd40      2	Malayalam                	ീുൂൃൄ൅െേൈ൉ൊോൌ്ൎ൏
 0x1e40      1	Latin Extended Additional	ṀṁṂṃṄṅṆṇṈṉṊṋṌṍṎṏ
 0x1eb0      1	Latin Extended Additional	ẰằẲẳẴẵẶặẸẹẺẻẼẽẾế
 0x1ec0      1	Latin Extended Additional	ỀềỂểỄễỆệỈỉỊịỌọỎỏ
 0x2000      2	General Punctuation      	           ​‌‍‎‏
 0x2010     55	General Punctuation      	‐‑‒–—―‖‗‘’‚‛“”„‟
 0x2020     64	General Punctuation      	†‡•‣․‥…‧  ‪‫‬‭‮ 
 0x20a0      4	Currency Symbols         	₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯
 0x2210      1	Mathematical Operators   	∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟
 0x4e20      1	CJK Unified Ideographs   	丠両丢丣两严並丧丨丩个丫丬中丮丯
 0x6580      1	CJK Unified Ideographs   	斀斁斂斃斄斅斆文斈斉斊斋斌斍斎斏
 0x65e0      1	CJK Unified Ideographs   	无旡既旣旤日旦旧旨早旪旫旬旭旮旯
 0x6720      1	CJK Unified Ideographs   	朠朡朢朣朤朥朦朧木朩未末本札朮术
 0x8a90      1	CJK Unified Ideographs   	誐誑誒誓誔誕誖誗誘誙誚誛誜誝語誟
 0xad60      1	Hangul Syllables         	굠굡굢굣굤굥굦굧굨굩굪굫구국굮굯
 0xc5b0      1	Hangul Syllables         	얰얱얲얳어억얶얷언얹얺얻얼얽얾얿
 0xd550      1	Hangul Syllables         	핐핑핒핓핔핕핖핗하학핚핛한핝핞핟
 0xfff0      1	Specials                 	￰￱￲￳￴￵￶￷￸￹￺￻￼�￾￿
0x10340      1	Gothic                   	𐍀𐍁𐍂𐍃𐍄𐍅𐍆𐍇𐍈𐍉𐍊𐍋𐍌𐍍𐍎𐍏

total bytes      : 257320
total characters : 256815
```

Usage:

```
usage: utfa.py [-h] [-u URL] [-b] [-e] [-t] [-l] [-n] [-m] [-x] [-o OFFSET]
          [-s SIZE] [-v]
          [file]

file analysis

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url e.g. -u http://bbc.co.uk
  -b, --bytes           analyse 256 possible bit patterns
  -e, --errors          enable unicode error replacement
  -t, --time            show run time
  -l, --legend          disable legend display
  -n, --name            disable unicode block names
  -m, --mask            show only characters present in file/url
  -x, --number          disable individual counts
  -o OFFSET, --offset OFFSET
  -s SIZE, --size SIZE
  -v, --version         python version, encoding and max code point
```
