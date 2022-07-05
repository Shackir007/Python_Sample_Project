import os
import html


def list_file_from_direcory(directory_name, html_loc):
    fileList = os.listdir(directory_name)


    #file=os.walk(directory_name)
    print(fileList)

    print(fileList[1:10])

    html_file = open(html_loc + "fileList.html","w")
    html_file.write("""<!DOCTYPE html>
<html>
<head>
<title>File List</title>
</head>
<body>""")

    html_file.write("<table>\n")
    html_file.write("<tr>\n")
    html_file.write("<th>\n")
    html_file.write("FileName\n")
    html_file.write("</th>\n")
    html_file.write("<th>\n")
    html_file.write("FileLink\n")
    html_file.write("</th>\n")
    html_file.write("</tr>\n")

    for i in fileList:
        html_file.write("<tr>\n")
        html_file.write("<td>\n")
        html_file.write(i+"\n")
        html_file.write("</td>\n")
        html_file.write("<td>\n")
        html_file.write("<a href="+directory_name+i+">"+i+"\n")
        html_file.write("</td>\n")
        html_file.write("</tr>\n")

    html_file.write("</table>\n")

    html_file.write("""</body>
</html>\n""")


def test_this_class():
    list_file_from_direcory("C:/Users/user/Documents/","C:/Users/user/Downloads/")


test_this_class()
