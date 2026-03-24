ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def tetrafrequency(text):
    tetrafrequencies = [0]*26*26*26*26
    for i in range(len(text)-3):
        x = (ALPHABET.find(text[i])*26*26*26 +
             ALPHABET.find(text[i+1])*26*26 +
             ALPHABET.find(text[i+2])*26 +
             ALPHABET.find[text[i+3]])
        tetrafrequencies[x] += 1
    for i in range(26*26*26*26):
        tetrafrequencies[i] = tetrafrequencies[i] / (len(text)-3)
    return tetrafrequencies

with open("dracula.txt", encoding="utf8") as file:
    # print(file.read())
    dracula = file.read()
    dracula.replace("\\ufeff", "")
    tetrafrequencies = tetrafrequency(file.read())
print(tetrafrequencies)