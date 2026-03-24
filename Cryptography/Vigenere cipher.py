# Does not work :(

from math import log
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(plaintext, key):
    ciphertext = ""
    for i in range(len(plaintext[i])):
        p = ALPHABET.index(plaintext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p+k)%26
        ciphertext += ALPHABET[c]
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ""
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p-k)%26
        plaintext += ALPHABET[c]
    return plaintext

def tetrafrequency(text):
    tetrafrequencies = [0]*26*26*26*26
    for i in range(len(text)-3):
        x = (ALPHABET.index(text[i])*26*26*26 +
             ALPHABET.index(text[i+1])*26*26 +
             ALPHABET.index(text[i+2])*26 +
             ALPHABET.index[text[i+3]])
        tetrafrequencies[x] += 1
    for i in range(26*26*26*26):
        tetrafrequencies[i] = tetrafrequencies[i] / (len(text)-3)
    return tetrafrequencies

def fitness(text):
    with open("dracula.txt", encoding="utf8") as file:
        dracula = file.read()
        dracula.replace("\\ufeff", "")
        tetrafrequencies = tetrafrequency(file.read())
    result = 0
    for i in range(len(text)-3):
        tetragram = text[i:i+4]
        x = (ALPHABET.index(tetragram[0])*26*26*26 +
             ALPHABET.index(tetragram[1])*26*26 +
             ALPHABET.index(tetragram[2])*26 +
             ALPHABET.index(tetragram[3]))
        y = tetrafrequencies[x]
        if y == 0:
            result += -15
        else:
            result += log(y)
    result = result / (len(text)-3)
    return result


ciphertext = "YOHAPIEVFWWIZBUNWVGJTMZKYFTNIIURDGVIAIRTTNAIJJDOCIJCZWMJYJIIQEOHVWANYZSGHSRGOPHKMEICKJTCOKIRRVZYEYWJHOQSIJDDBKMEWWEIIIUFKTCSSTOFTFZNYPPNSGSJXBJRPNCVBETTNSVMORMFZCJICITCWEPIRCLQDFBFBAIMKMIIURGOPHZYAIRZKIIRZYESHIJMZZPZNGWBJLTHYFTDHTTUGRYFVZPVJNRFZYTZBSDAIMFSEDBDDHJIJJHJZUDOPFTQADAKMAOHYJCCOIFCOSINSOWTXOAHYJTTDVHAIPVZSZRKTIYSEYIAMKMENCLWCZOJYHZHPUERFZYEMKVMOGRZSTCSDFNNWFSSZSDXTJAVYOWSUNVDBRYIJBETTNQZJNXSRSDRWKMOPHDZCCGKWOIUVWEQWUJNXSFKAGWEPBZHNJEIGFREJBVNNHMYTUNSYTLYOEITCSPTUIUDFNDGCJSDKZQLICKJNOSIYADBFWCJCGJRVHVBIOVRSYAIIYHZFZSVZGKNGVHZTNNWYFVZOCWEVRPJXKFVXSZRDDCJBJYEMBRYIJBRYTCSGWONDVHTJTRXCVBUFLYSIFIGWELMTQRRPVWXSFJFJYAOSXTVZFETRVBUNTCCLLHOHYFTTCLZNYSIXTJCUFNYOXWEZRNNTCAVBHTMFZWJICIWVBKYOMSFUEIHYJCVGVBHZBZMAQSJTMPQYYOGCJJAIRNJHVJVSOOVZSGOCXFIITITMDHZHAIBFYUIRVWSOOEIIFBFBTCOKRADGZJHVGSJEIDIJSNWELFJFWZROVVWIIJVXTDURYIJBRSDDHZXCGSRWTCOKXHZKRXDZSGQYYWJYRZGJJDWMKMERVFQEDBTNDZBKXHZZFAENHYJLDPIFRTOEIWJICIDJOEDTCWELTJDITTZQKNTCCNJVZFJMEDGDJRZZPFSZFMFNOCWYHZSJYAOSRSDNIIJLTAPXTVHLXANDIJSZBKTWISILIQSJLRZOKJRRSZLHOHFRYQWVBSVBUBINVVXWCWCJINZVXCGSRWLTHIJSKOJXEYVVXEZAJSOOHFMAQSTFUNSUFNTRRRABSRSDZJVSIAVVBANWEYEIRZSGOCJYEVZWWOHAVMINIEYIHSCDDZOKMFJFVXTVZCJDOVRYPGOEMECOJFLMSRIYKOZITCSGWIXSWTRCWJRINRVJDNOEIIYCETTNSVFNTFVFSJBKTCJBKNNPSKTPJYVFNYDITBZOKBHVHDZSOGLWEGMSJAMCLYIISTFSZWDZSOWEXINHKMAOMFZBMWELAAWEFLCOCYTJMFZRDBMJSOWXFTDCEXAIRCJTCWDWENHZSPZOTJLZHLXNJHZSVDHVLONGZUAOHYNSXFZYIXOCYIHSPTUMGZSFMWVSDNVZURJUVWS"

key = [""] * 5
for key[0] in ALPHABET:
    for key[1] in ALPHABET:
        for key[2] in ALPHABET:
            for key[3] in ALPHABET:
                for key[4] in ALPHABET:
                    pt = decrypt(ciphertext, key)
                    fit = fitness(pt)
                    if fit > -10:
                        break
                else:
                    continue
                break
            else:
                continue
            break
plaintext = decrypt(ciphertext,key)
print("hello?")
print(plaintext)
print("what")