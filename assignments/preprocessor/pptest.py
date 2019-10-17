import sys, re


def get_par(args):
    parameters = {}
    last = ""
    for i in range(1, len(args)):
        if args[i][0:2:] == "--" and i != len(args) - 1:
            parameters[args[i][2::]] = args[i + 1]
            last = args[i + 1]
        elif args[i] != last:
            print("Ignored argument:", args[i])
    return parameters


def check_par(parameters):
    tag_input, tag_output, tag_operation, tag_left, tag_right, tag_adaptor = False, False, False, False, False, False
    pos_operations = ["rc", "trim", "adaptor_removal"]
    for k, v in parameters.items():
        if k == "input":
            try:
                f = open(v,"rt")
                f.close()
            except:
                print("Input file was not found.")
        elif k == "output":
            tag_output = True
        elif k == "operation":
            if v in pos_operations:
                tag_operation = True
            else:
                print("Invalid operation:", v + ".\n\trc, trim or adaptor_removal is expected.")
        elif k == "trim-left":
            try:
                if int(v) > 0:
                    tag_left = True
                else:
                    raise()
            except:
                print("Invalid trim-left value. A >0 value is expected.")
        elif k == "trim-right":
            try:
                if int(v) > 0:
                    tag_right = True
                else:
                    raise()
            except:
                print("Invalid trim-right value. A >0 value is expected.")
        elif k == "adaptor":
            if re.search(r'\A[ACGTNacgtn]*\Z', v):
                tag_adaptor = True
            else:
                print("Adaptor sequence is not valid. Only [ACGTNacgtn] bases are allowed.")
        else:
            print("Ignored argument:", k, v)
    if (tag_input, tag_output, tag_operation) == (True, True, True):
        if parameters["operation"] == "adaptor" and tag_adaptor is True:
            return True
        elif parameters["operation"] == "trim" and (tag_left is True or tag_right is True):
            return True
        else:
            return True
    return False


def get_format(input_file):
    fp = open(input_file, "r")
    for line in fp:
        if line[0] == ">":
            file_format = "FASTA"
        elif line[0] == "@":
            file_format = "FASTQ"
        else:
            file_format = False
        break
    fp.close()
    return file_format


def revcomp(input_file, output_file, file_format):
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}
    new_file = open(output_file, "wt")
    with open(input_file, "r") as fp:
        while True:
            tag = fp.readline().rstrip()
            if not tag:
                break
            sequence = fp.readline().rstrip()
            try:
                revcomp = "".join(comp_dic[base] for base in sequence[::-1])
                new_file.write(tag + "\n" + revcomp + "\n")
                if file_format == "FASTQ":
                    fp.readline()
                    qual = fp.readline().rstrip()
                    revqual = "".join(qual[::-1])
                    new_file.write("+\n" + revqual + "\n")
            except:
                print(tag, "could not be processed.")
                if file_format == "FASTQ":
                    fp.readline()
                    fp.readline()


def trim(input_file, output_file, file_format, left, right):
    print("haha")
    return "okay"


def adaptor_removal(file, tag):
    print("hihi")
    return "okay"


test_arguments = ["name.py", "--input", "mbio.sample.fastq", "--output", "output_file.fastq", "--operation", "trim",
                  "jeje", "--probe", "wrong", "--adaptor", "ACGTT", "--trim-left", "2", "--trim-right", "5"]

parameters = get_par(test_arguments)

if check_par(parameters) == False:
    print("Invalid arguments used. Exiting.")
    exit(1)

file_format = get_format(parameters["input"])

if file_format == False:
    print("Invalid file format. Exiting.")
    exit(1)

if parameters["operation"] == "rc":
    revcomp(parameters["input"], parameters["output"], file_format)

