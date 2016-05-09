#!/usr/bin/env python3
from lxml import html
import requests
page = requests.get("http://www.cse.unsw.edu.au/studying-at-unsw/undergraduate/program-options/computer-engineering/elective-list/")

#with open("raw.html","r") as in_file:
#    raw_html = in_file.read()

tree = html.fromstring(page.content)

print("# Computer Engineering\n\n2016 elective options\n\n**WARNING** Only applies to *Computer Engineering* students enrolled in the [old program prior 2015](http://www.handbook.unsw.edu.au/undergraduate/programs/2014/3645.html).\n\n")

elements = tree.find_class("paragraph")
for element in elements:

    print("# " + element.find('h2').text)

    s1_offered = []
    s2_offered = []
    not_offered = []

    for link in element.findall(".//a"):
        course_code = link.text

        f = link.xpath('../following-sibling::td')
        course = f[0].text

        timetable_url = requests.get("http://timetable.unsw.edu.au/2016/" + course_code + ".html")

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

    print("\n### Offered 2016s1:")
    for i in s1_offered:
        print('[{0}](http://timetable.unsw.edu.au/2016/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2016/{0}.html)\n'.format(i[0], i[1]))

    print("\n### Offered 2016s2:")
    for i in s2_offered:
        print('[{0}](http://timetable.unsw.edu.au/2016/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2016/{0}.html)\n'.format(i[0], i[1]))

    print("\n### Not running :(")
    for i in not_offered:
        print('[{0}](http://timetable.unsw.edu.au/2016/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2016/{0}.html)\n'.format(i[0], i[1]))

