cs_lines = []

types = {
  "noninline": "[Index(true)]",
  "id": "[Index(false)]",
  "1": "float",
  "8": "sbyte",
  "16": "short",
  "32": "int",
  "64": "long",
  "u8": "byte",
  "u16": "ushort",
  "u32": "short",
  "u64": "ulong"
}

strings_without_lang = ["Directory", "InternalName"]

def get_char_index(string, c, i):
    return [pos for pos, char in enumerate(string) if char == c][i]

def compile_dbc(dbc_line):
    cs_line = ""
    cs_type = ""
    buffer = ""
    buffer2 = ""
    arg_line = ""
    two_lines = False
    if "$" in dbc_line:
        two_lines = True
        args_str = dbc_line[1:get_char_index(dbc_line,"$",1)]
        dbc_line = dbc_line[[pos for pos, char in enumerate(dbc_line) if char == "$"][1]+1:]
        args = args_str.split(",")
        arg_line = types[args[0]]
        if not (args[0] == "noninline" and args[1] == "id"):
            two_lines = False
    if "[" in dbc_line:
        two_lines = True
        card_int = dbc_line[get_char_index(dbc_line,"[",0)+1:len(dbc_line)-1]
        arg_line = "[Cardinality("+card_int+")]"
        dbc_line = dbc_line[:get_char_index(dbc_line,"[",0)]
    if "<" in dbc_line:
        cs_type = types[dbc_line[get_char_index(dbc_line, "<", 0)+1:len(dbc_line)-1]]
        dbc_line = dbc_line[:get_char_index(dbc_line, "<", 0)]
    elif "_lang" in dbc_line or dbc_line in strings_without_lang:
        if not dbc_line in strings_without_lang:
            dbc_line = dbc_line[:get_char_index(dbc_line, "_", 0)]
        cs_type = "string"
    else:
        cs_type = "float"
    if "C" in arg_line:
        buffer = "[]"
        buffer2 = " = new "+cs_type+"["+card_int+"]"
    
    cs_line = "public "+cs_type+buffer+" "+dbc_line+buffer2+";"

    return two_lines, arg_line, cs_line
 
# Using readlines()
input_file = open('dbc_structs.txt', 'r')
dbc_lines = input_file.readlines()

# Strips the newline character
for i, line in enumerate(dbc_lines):
    two_lines, arg_line, cs_line = compile_dbc(line.strip())
    if two_lines:
        cs_lines.append(arg_line+"\n")
    new_line_str = "\n"
    if i == len(dbc_lines)-1:
        new_line_str = ""
    cs_lines.append(cs_line+new_line_str)

# writing to file
output_file = open('cs_structs.txt', 'w')
output_file.writelines(cs_lines)
output_file.close()