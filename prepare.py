import os

folder = "sessions"
for filename in os.listdir(folder):
    infilename = os.path.join(folder, filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.json', '.txt')
    output = os.rename(infilename, newname)


for filename in os.listdir(folder):
    fin = open(folder+"/"+filename, "rt")
    fout = open("sessions-cleaned/"+filename, "wt")

    for line in fin:
        if "}" not in line and "{" not in line:
            output = line.replace('"', "")
            output = output.replace('data:', '')
            output = output.lstrip()
            if len(output) > 2:
                fout.write(output)


