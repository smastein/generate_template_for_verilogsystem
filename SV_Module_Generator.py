
inputFile = open("example_in.txt", "r")

InputText = [["parameter"], ["clock"], ["reset"], ["input"], ["output"], ["inout"], ["variable"]]
categories = ["parameter", "clock", "reset", "input", "output", "inout", "variable"]
NotesFields = [["//USER PARAMETERS BEGIN","//USER PARAMETERS END"],["//USER PORTS BEGIN","//USER PORTS END"],["//USER VARIABLES BEGIN","//USER VARIABLES END"],["//USER COMB BEGIN","//USER COMB END"],["//USER RESETS BEGIN","//USER RESETS END"],["//USER CLOCK BEGIN","//USER CLOCK END"]]
previousNotes = [[],[],[],[],[],[]]
category = ''


new = False
titleIndex = False
for line in inputFile:
    ModuleIndex = line.find("module")
    if(ModuleIndex != -1):
        titleIndex = True
        counter = 0
        Title = ''
        TitleBeg = False
        for x in range(6, len(line)):
            if((line[x] == ' ' or line[x] == '\t' or line[x] == '\n') and ~TitleBeg):
                continue
            else:
                TitleBeg = True
                Title += line[x]

    else:
        for cat in categories:
            if(line.find(cat) != -1 and line.find(cat) == 0):
                if (line[line.find(cat) + len(cat)] != ":"):
                    raise NameError("there is no parameter: \"" + cat + ":\" in the input file")
                else:
                    category = cat
                    new = True
                    break
        if(new):
            new = False
            continue

        for cell in InputText:
            if (cell[0] == category):
                string = ''
                for i in range(len(line)):
                    if(line[i] != ' ' and line[i] != '\t' and line[i] != '\n'):
                        string += line[i]


                if(len(string)>0):
                    cell.append(string)

inputFile.close()


if (titleIndex == False):
    raise NameError("Plik wejściowy nie zawiera nazwy modułu (np. module test)")
elif(len(Title) == 0):
    raise NameError("Nazwa modułu jest nieprawidłowa")

try:
    file = open(Title + ".sv", "r")
    notesFieldOpen = False
    index = 0
    for category in NotesFields:
        for line in file:
            if(line.find(category[0]) != -1):
                notesFieldOpen = True
                continue
            if(notesFieldOpen):
                if(line.find(category[1]) != -1):
                    notesFieldOpen = False
                    index += 1
                    break
                previousNotes[index].append(line)
except:
    print("Creating new file .sv")

#for cell in InputText:
#    for x in cell:

#        if(x.find(",") != -1 ):
#            cell.remove(x)
#            cell.extend(x.split(","))



#print(InputText)

outputFile = open(Title + ".sv", "w+")

##### Add module name #####

outputFile.write("module "+Title+" # (\n")
for y in categories:
    for x in InputText:
        if(x[0] == y == "parameter"):

            for z in range(1, len(x)):
                if(z == len(x)-1):
                    outputFile.write("\t\t" + x[z] + "\n\n")
                else:
                    outputFile.write("\t\t" + x[z] + ",\n")

            outputFile.write("\t\t//USER PARAMETERS BEGIN\n")
            if (len(previousNotes[0]) > 0):
                for line in previousNotes[0]:
                    outputFile.write(line)
            else:
                outputFile.write("\n")
            outputFile.write("\t\t//USER PARAMETERS END\n\t) (\n")
        elif(x[0] == y == "clock"):
            for z in range(1, len(x)):
                    clk = x[z].split(",")
                    outputFile.write("\t\tinput logic " + clk[0] + ",\n")
        elif (x[0] == y == "reset"):
            for z in range(1, len(x)):
                rst = x[z].split(",")
                outputFile.write("\t\tinput logic " + rst[0] + ",\n\n")
            outputFile.write("\t\t//USER PORTS BEGIN\n")
            if (len(previousNotes[1]) > 0):
                for line in previousNotes[1]:
                    outputFile.write(line)
            else:
                outputFile.write("\n")
            outputFile.write("\t\t//USER PORTS END\n\n")
        elif(x[0] == y == "input"):
            for z in range(1, len(x)):
                if(x[z].find("]") != -1):
                    inp = x[z].split("]")
                    outputFile.write("\t\tinput logic " + inp[0] + "] " + inp[1] + ",\n")
                else:
                    outputFile.write("\t\tinput logic " + x[z] + ",\n")
            outputFile.write("\n")
        elif (x[0] == y == "output"):
            for z in range(1, len(x)):
                if(x[z].find(",") != -1):
                    out = x[z].split(',')
                    if (out[0].find("]") != -1):
                        inp = out[0].split("]")
                        outputFile.write("\t\toutput logic " + inp[0] + "] " + inp[1] + ",\n")
                    else:
                        outputFile.write("\t\toutput logic " + out[0] + ",\n")
                else:
                    if (x[z].find("]") != -1):
                        inp = x[z].split("]")
                        outputFile.write("\t\toutput logic " + inp[0] + "] " + inp[1] + ",\n")
                    else:
                        outputFile.write("\t\toutput logic " + x[z] + ",\n")
            outputFile.write("\n")
        elif (x[0] == y == "inout"):
            for z in range(1, len(x)):
                outputFile.write("\t\tinout logic " + x[z] + ",\n")
            outputFile.write("\n\t};\n\n")
        elif (x[0] == y == "variable"):
            for z in range(1, len(x)):
                if (x[z].find(",") != -1):
                    var = x[z].split(",")
                    if (var[0].find("]") != -1):
                        inp = var[0].split("]")
                        outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + ";\n")
                    else:
                        outputFile.write("\tlogic " + var[0] + ";\n")
                else:
                    if (x[z].find("]") != -1):
                        inp = x[z].split("]")
                        outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + ";\n")
                    else:
                        outputFile.write("\tlogic " + x[z] + ";\n")
            outputFile.write("\n")

############################ generate _nxt
### for output
if(len(InputText[4])>1):
    cell = InputText[4]
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            out = cell[z].split(',')
            if (out[0].find("]") != -1):
                inp = out[0].split("]")
                outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + "_nxt;\n")
            else:
                outputFile.write("\tlogic " + out[0] + "_nxt;\n")
        else:
            if (cell[z].find("]") != -1):
                inp = cell[z].split("]")
                outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + "_nxt;\n")
            else:
                outputFile.write("\tlogic " + cell[z] + "_nxt;\n")
    outputFile.write("\n")

##### for variables
if(len(InputText[6])>1):
    cell = InputText[6]
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            if (var[0].find("]") != -1):
                inp = var[0].split("]")
                outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + "_nxt;\n")
            else:
                outputFile.write("\tlogic " + var[0] + "_nxt;\n")
        else:
            if (cell[z].find("]") != -1):
                inp = cell[z].split("]")
                outputFile.write("\tlogic " + inp[0] + "] " + inp[1] + "_nxt;\n")
            else:
                outputFile.write("\tlogic " + cell[z] + "_nxt;\n")

outputFile.write("\n\t//USER VARIABLES BEGIN\n")
if (len(previousNotes[2]) > 0):
    for line in previousNotes[2]:
        outputFile.write(line)
else:
    outputFile.write("\n")
outputFile.write("\t//USER VARIABLES END\n\n")

#########################################always_comb begin
outputFile.write("\talways_comb begin\n")
######output
if(len(InputText[4])>1):
    cell = InputText[4]
    valDefault = False
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            out = cell[z].split(',')
            for y in out:
                if(y.find("default") != -1):
                    default_val = True
                    val=y.split("=")

            if(valDefault):
                defval = "'h"+val[1]
            else:
                if (out[0].find("]") != -1):
                    defval = inp[1]
                else:
                    defval = out[0]

            if (out[0].find("]") != -1):
                inp = out[0].split("]")
                outputFile.write("\t\t" + inp[1] + "_nxt\t= "+ defval +";\n")
            else:
                outputFile.write("\t\t" + out[0] + "_nxt\t= "+ defval +";\n")
        else:
            if (cell[z].find("]") != -1):
                inp = cell[z].split("]")
                outputFile.write("\t\t" + inp[1] + "_nxt\t= " + inp[1] + ";\n")
            else:
                outputFile.write("\t\t" + cell[z] + "_nxt\t= " + cell[z] + ";\n")
    outputFile.write("\n")

#####variable
if(len(InputText[6])>1):
    cell = InputText[6]
    default_val = False
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            for y in var:
                if(y.find("default_val") != -1):
                    default_val = True
                    val=y.split("=")

            if(default_val):
                defval = "'h"+val[1]
            else:
                if (var[0].find("]") != -1):
                    defval = var[0]
                else:
                    defval = inp[1]

            if (var[0].find("]") != -1):
                inp = var[0].split("]")
                outputFile.write("\t\t"+ inp[1] + "_nxt\t= "+ defval + ";\n")
            else:
                outputFile.write("\t\t" + var[0] + "_nxt\t= "+ defval + ";\n")
        else:
            if (cell[z].find("]") != -1):
                inp = cell[z].split("]")
                outputFile.write("\t\t" + inp[0] + "_nxt\t= " + inp[1] + ";\n")
            else:
                outputFile.write("\t\t" + cell[z] + "_nxt\t= " + cell[z] + ";\n")

outputFile.write("\t\t//USER COMB BEGIN\n")
if (len(previousNotes[3]) > 0):
    for line in previousNotes[3]:
        outputFile.write(line)
else:
    outputFile.write("\n")
outputFile.write("\t\t//USER COMB END\n\tend\n")

############always_ff @
outputFile.write("\n\talways_ff @(")

if(len(InputText[1])>1):
    cell = InputText[1]
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            clk = cell[z].split(",")
            for y in clk:
                if (y.find("edge") != -1):
                    edge = y.split("=")
                    if(edge[1] == "true"):
                        outputFile.write("posedge " + clk[0])
                    elif(edge[1] == "false"):
                        outputFile.write("negedge " + clk[0])
                    else:
                        raise NameError("Podany argument dla 'edge' jest niewlasciwy")
        else:
            outputFile.write("posedge " + clk[0])

####### reset
if(len(InputText[2])>1):
    cell = InputText[2]
    Sign_Param = False
    for z in range(1,len(cell)):
        if(cell[z].find(",") != -1):
            rst = cell[z].split(",")
            for y in rst:
                if(y.find("polarity") != -1):
                    pol = y.split("=")
                    if (pol[1] == "false"):
                        polarity = "negedge "
                        pol_val = "1'b0"
                    elif (pol[1] == "true"):
                        polarity = "posedge "
                        pol_val = "1'b1"
                    else:
                        raise NameError("Podany argument dla 'polarity' jest niewlasciwy")

                elif (y.find("synchronous") != -1):
                    syn = y.split("=")
                    if (syn[1] == "true"):
                        outputFile.write(") begin\n")
                    elif (syn[1] == "false"):
                        outputFile.write(" or "+ polarity + rst[0] + ") begin\n")
        else:
            polarity = "negedge"
            outputFile.write(" or " + polarity + rst[0] + ") begin\n")

outputFile.write("\t\tif(" + rst[0] + " = 1'b0) begin\n")

if(len(InputText[4])>1):
    cell = InputText[4]
    RstDefault = False
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            for y in var:
                if(y.find("reset_val") != -1):
                    RstDefault = True
                    res = y.split("=")

            if(RstDefault):
                reset_val = "'h"+res[1]
            else:
                reset_val = "'h0"

            if(cell[0].find("]") != -1):
                out = cell[0].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + var[0] + "\t<= " + reset_val + ";\n")

        else:
            reset_val = "'h0"
            if (cell[z].find("]") != -1):
                out = cell[z].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + cell[z] + "\t<= " + reset_val + ";\n")

outputFile.write("\n")

if(len(InputText[6])>1):
    cell = InputText[6]
    Sign_Param = False
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            for y in var:
                if(y.find("reset_val") != -1):
                    Sign_Param = True
                    res = y.split("=")

            if(Sign_Param):
                reset_val = "'h"+res[1]
            else:
                reset_val = "'h0"

            if(var[0].find("]") != -1):
                out = var[0].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + var[0] + "\t<= " + reset_val + ";\n")
        else:
            reset_val = "'h0"
            if (cell[z].find("]") != -1):
                out = cell[z].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + cell[z] + "\t<= " + reset_val + ";\n")

outputFile.write("\n\t\t\t//USER RESETS BEGIN\n")
if(len(previousNotes[4])>0 ):
    for line in previousNotes[4]:
        outputFile.write(line)
else:
    outputFile.write("\n")
outputFile.write("\t\t\t//USER RESETS END\n\t\tend\n")
outputFile.write("\t\telse begin\n")

if(len(InputText[4])>1):
    cell = InputText[4]
    RstDefault = False
    reset_val = "'h0"
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            if(var[0].find("]") != -1):
                out = var[0].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + var[0] + "\t<= " + reset_val + ";\n")

        else:
            if(cell[z].find("]") != -1):
                out = cell[z].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + cell[z] + "\t<= " + reset_val + ";\n")

outputFile.write("\n")

if(len(InputText[6])>1):
    cell = InputText[6]
    RstDefault = False
    reset_val = "_nxt"
    for z in range(1, len(cell)):
        if (cell[z].find(",") != -1):
            var = cell[z].split(",")
            if(var[0].find("]") != -1):
                out = var[0].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + out[1] + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + var[0] + "\t<= " + var[0] + reset_val + ";\n")

        else:
            if(cell[z].find("]") != -1):
                out = cell[z].split("]")
                outputFile.write("\t\t\t" + out[1] + "\t<= " + out[1] + reset_val + ";\n")
            else:
                outputFile.write("\t\t\t" + cell[z] + "\t<= " + cell[z] + reset_val + ";\n")

outputFile.write("\n\t\t\t//USER CLOCK BEGIN\n")
if(len(previousNotes[5])>0 ):
    for line in previousNotes[5]:
        outputFile.write(line)
else:
    outputFile.write("\n")
outputFile.write("\t\t\t//USER CLOCK END\n\t\tend\n\tend\nendmodule;\n")
