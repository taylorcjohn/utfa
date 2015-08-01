utfa
====

**UTF-8 analysis for files and web pages**

utfa.py is a Python script which analyses files or web pages into counts of all UTF-8 characters.  It can also (using -b byte mode) analyse the data into component bytes if a file or web page is not encoded using UTF-8.

I hope it will be useful for you.  Please let me know of any problems or suggestions for improving the script.  

John  

**Description**

Years ago I wrote a simple utility to analyse a file into its byte components.  I find it very useful and always bring it to each new system I work on, together with some elementary test files; for example a file `256` containing 256 bytes, one of each bit pattern.  Where necessary I have rewritten the utility in C, Java, Perl and awk.

As a first examination of a file, it easy to tell whether a text file is *probably* DOS- or Unix-formatted by looking at the counts of new line (0x0a) and carriage return (0x0d) characters.  Often, problems are resolved by checking whether a file contains tabs, nulls, delete and other unprintables.  In text files, characters above 0x7f may represent accented characters or other special values.

However, nowadays many files are encoded in UTF-8 (and most web pages too).  Simply adding counts of all bit patterns is not sufficient to understand the large “alphabet” of Unicode characters which are represented in 1, 2, 3 or 4 bytes.

I have rewritten the program again, now in python (utfa.py), this time including support for all UTF-8 characters and adding a mechanism to read web pages.  Since the two widely used versions of python (2.x and 3.x) handle unicode differently, I wrote the program to detect which version of python is in use and to handle unicode characters appropriately.

See the document `ufta.pdf` for background and usage examples using supplied test files `256` and `u256` and various web pages.

**Usage**

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

**Examples**

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

  * utfa.py u256 -b

The same file viewed as byte counts
```
byte analysis for u256

         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f		-- characters --

     0   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		................
     1   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		................
     2   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		 !"#$%&'()*+,-./
     3   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		0123456789:;<=>?
     4   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		@ABCDEFGHIJKLMNO
     5   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		PQRSTUVWXYZ[\]^_
     6   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		`abcdefghijklmno
     7   1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1		pqrstuvwxyz{|}~
     8   2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2		................
     9   2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2		................
     a   2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2		 ¡¢£¤¥¦§¨©ª«¬­®¯
     b   2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2		°±²³´µ¶·¸¹º»¼½¾¿
     c   0  0 64 64  0  0  0  0  0  0  0  0  0  0  0  0		ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ
     d   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0		ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß
     e   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0		àáâãäåæçèéêëìíîï
     f   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0		ðñòóôõö÷øùúûüýþÿ

total bytes : 384
```

  * utfa.py -u http://www.bbc.co.uk/news -xm

Note that flag -x disables individual character counts, shown here for brevity:

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

  * utfa.py -mxu https://en.wikipedia.org/wiki/Braille

```
unicode analysis for https://en.wikipedia.org/wiki/Braille	(running Python 3)

        total	-- unicode block --                 	-- characters --

      0   3761	Basic Latin                         	         ..     
      1      0	Basic Latin                         	                
      2  57116	Basic Latin                         	 !"#$%&'()*+,-./
      3  43999	Basic Latin                         	0123456789:;<=>?
      4  11502	Basic Latin                         	 ABCDEFGHIJKLMNO
      5   8056	Basic Latin                         	PQRSTUVWXYZ[\]^_
      6 145627	Basic Latin                         	 abcdefghijklmno
      7  62938	Basic Latin                         	pqrstuvwxyz{ }  
   0xa0      1	Latin-1 Supplement                  	              ® 
   0xb0      1	Latin-1 Supplement                  	             ½  
   0xc0     11	Latin-1 Supplement                  	À Â Ä  ÇÈÉÊË ÍÎÏ
   0xd0      7	Latin-1 Supplement                  	  Ò Ô Ö× Ù ÛÜ   
   0xe0     38	Latin-1 Supplement                  	àáâ äå çèéêëìíîï
   0xf0     32	Latin-1 Supplement                  	 ñòóô ö  ùúûü   
  0x100     26	Latin Extended-A                    	 ā ă        Čč  
  0x110      2	Latin Extended-A                    	   ē ĕ          
  0x120     10	Latin Extended-A                    	           ī    
  0x130      1	Latin Extended-A                    	 ı              
  0x140      2	Latin Extended-A                    	             ō  
  0x150      2	Latin Extended-A                    	          Ś     
  0x160      4	Latin Extended-A                    	 š              
  0x170      3	Latin Extended-A                    	   ų            
  0x250      2	IPA Extensions                      	         ə      
  0x260      2	IPA Extensions                      	          ɪ     
  0x2b0      2	Spacing Modifier Letters            	              ʾʿ
  0x2c0      2	Spacing Modifier Letters            	        ˈ       
  0x390      3	Greek and Coptic                    	     Ε    Κ Μ   
  0x3a0      2	Greek and Coptic                    	            ά   
  0x3b0     12	Greek and Coptic                    	 α γδ  η ικλ ν  
  0x3c0      4	Greek and Coptic                    	πρς           ώ 
  0x410      9	Cyrillic                            	 Б          М   
  0x420      7	Cyrillic                            	РСТУ   ЧШ       
  0x430     83	Cyrillic                            	абвгде зийкл ноп
  0x440     52	Cyrillic                            	рстуфх чш ъыь  я
  0x450      3	Cyrillic                            	       їј       
  0x4d0      1	Cyrillic                            	 ӑ              
  0x530      1	Armenian                            	  Բ             
  0x540      1	Armenian                            	Հ               
  0x560      8	Armenian                            	 ա գ ե     իլ   
  0x570      3	Armenian                            	     յն         
  0x580      4	Armenian                            	ր               
  0x5d0      8	Hebrew                              	 ב       י כל   
  0x5e0      5	Hebrew                              	  ע     ר ת     
  0x620     13	Arabic                              	       ابة  ج  د
  0x630     11	Arabic                              	 ر س     ع      
  0x640     11	Arabic                              	 ف  لمن و ي     
  0x670      2	Arabic                              	         ٹ    پ 
  0x6c0      5	Arabic                              	            ی   
  0x920     11	Devanagari                          	ठ   त दधन प ब म 
  0x930     11	Devanagari                          	र ल      ह    ाि
  0x940      9	Devanagari                          	ी      े     ्  
  0x980      2	Bengali                             	  ং    ই        
  0x9a0      6	Bengali                             	    ত দধ  প ব   
  0x9b0      6	Bengali                             	র ল           াি
  0x9c0      3	Bengali                             	       ে     ্  
  0xa10      1	Gurmukhi                            	            ਜ   
  0xa20      3	Gurmukhi                            	          ਪ ਬ   
  0xa30      3	Gurmukhi                            	ਰ ਲ           ਾ 
  0xa40      2	Gurmukhi                            	ੀ      ੇ        
  0xa70      1	Gurmukhi                            	ੰ               
  0xb90      1	Tamil                               	               ட
  0xba0      6	Tamil                               	    த     ப   மய
  0xbb0      3	Tamil                               	    ழ          ி
  0xbc0      7	Tamil                               	 ு    ெ ை    ்  
  0xc10      1	Telugu                              	       గ        
  0xc20      4	Telugu                              	    త     ప బ  య
  0xc30      7	Telugu                              	ర ల            ి
  0xc40      6	Telugu                              	ీు    ె      ్  
  0xd00      1	Malayalam                           	  ം             
  0xd20      5	Malayalam                           	          പ ബ മയ
  0xd30      8	Malayalam                           	ര ലള          ാി
  0xd40      2	Malayalam                           	      െ      ്  
  0xd70      1	Malayalam                           	             ൽ  
  0xe00      1	Thai                                	 ก              
  0xe10      2	Thai                                	       ท  บ     
  0xe20      7	Thai                                	  ยร ล   ษ   อ  
  0xe30      1	Thai                                	 ั              
  0xe40      3	Thai                                	เ   ไ       ์   
 0x1000      4	Myanmar                             	က   င           
 0x1010     10	Myanmar                             	တ   န   ဘမ    သ 
 0x1020      3	Myanmar                             	            ာ   
 0x1030      9	Myanmar                             	 ေ       ္်ျြ   
 0x10d0     11	Georgian                            	აბ     თი ლ     
 0x10e0      9	Georgian                            	რსტუფქ  შ       
 0x1e00      3	Latin Extended Additional           	             ḍ ḏ
 0x1e20      1	Latin Extended Additional           	     ḥ          
 0x1e40      5	Latin Extended Additional           	   ṃ   ṇ        
 0x1e60      2	Latin Extended Additional           	             ṭ  
 0x1eb0      1	Latin Extended Additional           	               ế
 0x1ec0      1	Latin Extended Additional           	       ệ        
 0x1ee0      2	Latin Extended Additional           	               ữ
 0x2010    110	General Punctuation                 	‐  –—    ’      
 0x2190      1	Arrows                              	  →             
 0x27e0      8	Miscellaneous Mathematical Symbols-A	        ⟨⟩      
 0x2800    138	Braille Patterns                    	⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏
 0x2810    109	Braille Patterns                    	⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟
 0x2820     90	Braille Patterns                    	⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯
 0x2830     86	Braille Patterns                    	⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿
 0x2840     32	Braille Patterns                    	⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏
 0x2850     32	Braille Patterns                    	⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟
 0x2860     32	Braille Patterns                    	⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯
 0x2870     32	Braille Patterns                    	⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿
 0x2880     32	Braille Patterns                    	⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏
 0x2890     32	Braille Patterns                    	⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟
 0x28a0     32	Braille Patterns                    	⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯
 0x28b0     32	Braille Patterns                    	⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿
 0x28c0     32	Braille Patterns                    	⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏
 0x28d0     32	Braille Patterns                    	⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟
 0x28e0     32	Braille Patterns                    	⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯
 0x28f0     32	Braille Patterns                    	⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿
 0x4e20      1	CJK Unified Ideographs              	             中  
 0x51f0      1	CJK Unified Ideographs              	        凸       
 0x5b50      2	CJK Unified Ideographs              	       字        
 0x6580      4	CJK Unified Ideographs              	       文        
 0x65e0      1	CJK Unified Ideographs              	     日          
 0x6720      1	CJK Unified Ideographs              	            本   
 0x70b0      1	CJK Unified Ideographs              	         点      
 0x76f0      2	CJK Unified Ideographs              	  盲             
 0x7cb0      1	CJK Unified Ideographs              	     粵          
 0x8a00      1	CJK Unified Ideographs              	言               
 0x8a90      2	CJK Unified Ideographs              	              語 
 0xad60      1	Hangul Syllables                    	             국  
 0xc5b0      1	Hangul Syllables                    	    어           
 0xc790      1	Hangul Syllables                    	자               
 0xc810      1	Hangul Syllables                    	점               
 0xd550      1	Hangul Syllables                    	            한   

total bytes      : 337190
total characters : 334528
```
  * utfa.py bom -m  

Note that the byte order mark (bom) comprises three bytes to form one UTF-8 character which is (curiously) the last character of the unicode block `Arabic Presentation Forms-B` and also serves as `Zero Width Non-Breaking Space (ZWNBSP)`.
```
unicode analysis for bom	(running Python 3)

         0 1 2 3 4 5 6 7 8 9 a b c d e f	-- unicode block --        	-- characters --

      0  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      1  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      2  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      3  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      4  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      5  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      6  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
      7  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0	Basic Latin                	                
 0xfef0  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1	Arabic Presentation Forms-B	               ﻿

total bytes      : 3
total characters : 1
```

**Invoking utfa**

For convenience I have made the first line of utfa.py:

`#!/usr/bin/env python3`

on the assumption that the file will have execute (e.g. 755) permissions.  But of course the file can be invoked using a python interpreter:

`python utfa.py...`

`python3 utfa.py...`

or via a copy or symbolic link with a different name if `utfa.py` is just too many character to type (it's too many for me...)

**Module imports**

These two import statements (used to help with python2/python3 compatibility)

`import requests`  
`import six`

could cause problems.  It may be necessary to add one or both to the python installation with pip or pip3 e.g.

`pip install requests`

**Copyright**

Copyright (c) 2015 John Taylor

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
