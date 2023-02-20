import os

def create_markdown(doc):
    noOfSLides = len(doc['summary'])

    md = """"""
    f = open("slidegen/theme.md", "r")
    atext = f.read()
    f.close()
    md += atext+"\n"
    md += create_home_slide(doc)

    for i in range(noOfSLides):
        md += create_new_slide(doc,i)

    return md

def create_home_slide(doc):
    # Create a home slide
    text = "\n# " + doc['title'] + "\n" + doc['author'][0] + "\n\n"
    if doc['bgimage'] != '':
        text += "---\n![bg]({})\n".format(doc['bgimage'])
    return text


def create_new_slide(doc,slideNum):
    # Create a new slide
    contents = doc['summary'][slideNum]
    text = ''

    # adding the title
    titles = list(doc['summary'].keys())
    text += "\n---\n# " + str(titles[slideNum]) + "\n"

    # adding the bullet points
    for content in contents:
        text += "\n- " + content + "\n"

    return text

def generateSlides(doc):
    print ("generating slides...")
    # Create a markdown object
    md = create_markdown(doc)
    f = open('output.md', 'w')
    f.write(md)
    f.close()
    #marp should have executable permissions
    print ("hello from md")
    os.system('./marp output.md --pdf')
