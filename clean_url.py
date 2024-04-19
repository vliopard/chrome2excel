from htmlSupport import parse_url_clean

if __name__ == "__main__":
    with open('links.txt', 'r', encoding='utf-8') as file_lines:
        paramz = []
        lines = file_lines.readlines()
        for line in lines:
            # if not line.startswith('java') and check(line, symb) and check(line, list(dparams)):
            li = parse_url_clean(line)
            if li:
                paramz.append(li)

        sam_list = list(set(paramz))
        sam_list.sort()
        for sam in sam_list:
            print(sam)
