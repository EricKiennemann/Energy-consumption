
import os
import html

def is_html_file(filename):
  return filename.endswith(".html")

def createHTML(depts):
    with open("./output/index.html", "w") as f:
        f.write("<html><body><ul>\n")
        f.write(f"<H1>Energy consumption by city</H1>\n")
        for dept in depts:
            f.write(f"<H2>{dept}</H2>\n")
            directories = os.listdir(f"./output/{dept}")
            print(directories)
            for filename in directories:
                if is_html_file(filename):
                    pathname = os.path.join(str(dept),filename)
                    f.write('<li><a href="%s">%s</a></li>\n' %
                            (html.escape(pathname, True), html.escape(os.path.splitext(filename)[0])))
        f.write("</ul></body></html>\n")

if __name__ == '__main__':
    createHTML([75,92,93,94])

