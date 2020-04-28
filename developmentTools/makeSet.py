
with open('preset.class', 'w', encoding='utf-8') as chrome_html:
	with open('preset.txt', 'r', encoding='utf-8') as read_file:
		x = read_file.readline().strip()
		while x:
			chrome_html.write("    @property\n")
			chrome_html.write("    def {}(self):\n".format(x))
			chrome_html.write("        return self._{}\n".format(x))
			chrome_html.write("\n")
			chrome_html.write("    @{}.setter\n".format(x))
			chrome_html.write("    def {}(self, {}):\n".format(x,x))
			chrome_html.write("        self._{} = {}\n".format(x,x))
			chrome_html.write("\n")
			x = read_file.readline().strip()
		
