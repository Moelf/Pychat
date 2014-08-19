def letter_frequency(text):
    text = text.lower()
    resu = []
    for chars in text:
        if text.count(chars) != 0 and chars != " ":
            resu.append({chars:text.count(chars)})
            text = text.replace(chars, "")
    for tt in resu:
        print tt[tt.keys()[0]], resu[-1][resu[-1].keys()[0]]
        if tt[tt.keys()[0]] <= resu[-1][resu[-1].keys()[0]]:
            print resu[0]
            resu.append(tt)
            resu.remove(tt)
    return resu

print letter_frequency("asdasda SHJKHAJKSHDJKA    asdlkjasdklja")