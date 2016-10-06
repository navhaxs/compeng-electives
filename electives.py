#!/usr/bin/env python3
from lxml import html
import requests

headings = ["Breadth electives", "Depth electives"]

page = requests.get("https://www.engineering.unsw.edu.au/computer-science-engineering/help-resources/for-students/program-outlines/ug-program-outlines-2014-and-prior/computer-engineeri-1")
tree = html.fromstring(page.content)

#
#with open("raw.html","r") as in_file:
#    raw_html = in_file.read()
#
#tree = html.fromstring(raw_html)

print("# Computer Engineering\n\n2017 elective options\n\n**WARNING** Only applies to *Computer Engineering* students who started in 2014 (i.e. started with my cohort) (http://www.handbook.unsw.edu.au/undergraduate/programs/2014/3645.html).\n\nNote: COMP3211 isn't really a breadth elective as it is core - yes, another one of /those/ courses.\n\n")

# for each of the two tables (breadth and depth)
j = 0
elements = tree.find_class("table table-striped table-course")
for element in elements:

    print("# " + headings[j])
    j = j + 1

    s1_offered = []
    s2_offered = []
    not_offered = []

    for link in element.findall(".//a"):
        course_code = link.text

        f = link.xpath('../following-sibling::td')
        course = f[0].text

        timetable_url = requests.get("http://timetable.unsw.edu.au/2017/" + course_code + ".html")

        subtree = html.fromstring(timetable_url.content)

        e = subtree.xpath('.//*[contains(text(),"offering information for the selected course was not found")]')
        if (len(e) > 0):
            not_offered.append([course_code, course])
        else:
            e = subtree.xpath('.//*[contains(text(),"SEMESTER ONE")]')
            if (len(e) > 0):
                s1_offered.append([course_code, course])
            e = subtree.xpath('.//*[contains(text(),"SEMESTER TWO")]')
            if (len(e) > 0):
                s2_offered.append([course_code, course])

    print("\n### Offered 2017s1:")
    for i in s1_offered:
        print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

    print("\n### Offered 2017s2:")
    for i in s2_offered:
        print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

    print("\n### Not running :(")
    for i in not_offered:
        print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

