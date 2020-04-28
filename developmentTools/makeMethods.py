with open('index.txt') as file:
    line = file.readline().strip()
    with open('index.class', 'w') as index:
        while line:
            index.write("\n")
            index.write("    @property\n")
            index.write("    def {}(self):\n".format(line))
            index.write("        return self._{}\n".format(line))
            index.write("\n")
            index.write("    @{}.setter\n".format(line))
            index.write("    def {}(self, {}):\n".format(line, line))
            index.write("        self._{} = ({}, self._{}[1])\n".format(line, line, line))
            index.write("\n")
            index.write("    @{}.getter\n".format(line))
            index.write("    def {}(self):\n".format(line))
            index.write("        return self._{}[0]\n".format(line))
            line = file.readline().strip()
