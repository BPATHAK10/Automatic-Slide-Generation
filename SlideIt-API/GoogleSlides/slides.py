from __future__ import print_function

from googleapiclient import discovery

#For authorized data access, we need additional resources http and oauth2client
from httplib2 import Http
from oauth2client import file, client, tools

#SCOPES is a critical variable: it represents the set of scopes of authorization an app wants to obtain (then access) on behalf of user(s). 
SCOPES = 'https://www.googleapis.com/auth/presentations',
CLIENT_SECRET= 'credential.json'

def doEverything():
    # Once the user has authorized access to their personal data by your app, a special "access token" is given to your app.
    #This precious resource must be stored in storage.json here

    store = file.Storage('./storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        #creds variables are attempting to get a valid access token with which to make an authorized API call.
        creds = tools.run_flow(flow, store)


    #To create a service endpoint for interacting with an API, authorized or otherwise.
    SLIDES = discovery.build('slides', 'v1', http=creds.authorize(Http()))

    #To create a presentation, we need to create a presentation object.
    print('** Create new slide deck')
    DATA = {'title': 'Slides text formatting DEMO'}
    rsp = SLIDES.presentations().create(body=DATA).execute()

    # THis is the unique presentation id of the presentation created
    deckID = rsp['presentationId']
    
    titleSlide = rsp['slides'][0]

    titleID = titleSlide['pageElements'][0]['objectId']

    subtitleID = titleSlide['pageElements'][1]['objectId']

    print('** Create "main point" layout slide & add titles')
    reqs = [
        {'createSlide': {'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'}}},
        {'insertText': {'objectId': titleID, 'text': 'About Nepal'}},
        {'insertText': {'objectId': subtitleID, 'text': 'via the Google Slides API'}},
    ]

    # Creating the slides one by one
    rsp = SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute().get('replies')
    slideID = rsp[0]['createSlide']['objectId']

    print('** Fetch "main point" slide title (textbox) ID')
    rsp = SLIDES.presentations().pages().get(presentationId=deckID,
            pageObjectId=slideID).execute().get('pageElements')
    textboxID = rsp[0]['objectId']

    #text bhitra bullet points ma rakne chij rakhne ho text[0] euta sentence text[1] arko and likewise..
    text=['Enchanting lakes', 'Panoramic views of mountains', 'Temples with gorgeous architecture','Birth place of Buddha','Ever flowing rivers']
    print('** Insert text & perform various formatting operations')

    #Next slide
    reqs = [
        # add 7 paragraphs
        {'insertText': {
            'text': f'{text[0]} \n{text[1]} \n{text[2]}  \n{text[3]} \n{text[4]}',
            'objectId': textboxID,
        }},
        # shrink text from 48pt ("main point" textbox default) to 32pt
        {'updateTextStyle': {
            'objectId': textboxID,
            'style': {'fontSize': {'magnitude': 25, 'unit': 'PT'}},
            'textRange': {'type': 'ALL'},
            'fields': 'fontSize',
        }},
        # change word 1 in para 1 ("Bold") to bold
        {'updateTextStyle': {
            'objectId': textboxID,
            #'style': {'bold': True},
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 0, 'endIndex': 5},
            'fields': 'bold',
        }},
        # change word 1 in para 2 ("Ital") to italics
        {'updateTextStyle': {
            'objectId': textboxID,
            #'style': {'italic': True},
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 7, 'endIndex': 11},
            'fields': 'italic'
        }},
        # change word 1 in para 6 ("Mono") to Courier New
        {'updateTextStyle': {
            'objectId': textboxID,
            #'style': {'fontFamily': 'Courier New'},
            'textRange': {'type': 'FIXED_RANGE', 'startIndex': 36, 'endIndex': 40},
            'fields': 'fontFamily'
        }},
        
        # bulletize everything
        {'createParagraphBullets': {
            'objectId': textboxID,
            'textRange': {'type': 'ALL'}},
        },
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute()


    #Next slide

    reqs=[
        {
            "createSlide":{
                "insertionIndex":2,
                "slideLayoutReference": {'predefinedLayout': 'TITLE_AND_BODY'}
            }
        },
        
    ]

    rsp = SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute().get('replies')
    slideID2 = rsp[0]['createSlide']['objectId']
    print('** Fetch "main point" slide title (textbox) ID')
    rsp = SLIDES.presentations().pages().get(presentationId=deckID,
            pageObjectId=slideID2).execute().get('pageElements')
    textboxID2 = rsp[0]['objectId']
    textboxID3 = rsp[1]['objectId']
    reqs = [
        # add 7 paragraphs
        {'insertText': {
            'text': 'Religions in Nepal',#hamro heading yeta
            'objectId': textboxID2,
        }},
        {'insertText': {
            'text': 'The main religions followed in Nepal are Hinduism, Buddhism, Islam, Kirat, and Christianity. As per the census of 2011, 81.3% of the Nepalese population is Hindu, 9.0% is Buddhist 4.4% is Muslim, 3.0% is Kirant/Yumaist, 1.4% is Christian, and 0.9% follows other religions', #hamro body yeta
            'objectId': textboxID3,
        }},
    ]

    SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute()


    #next slide

    reqs=[
        {
            "createSlide":{
                "insertionIndex":3,
                "slideLayoutReference": {'predefinedLayout': 'MAIN_POINT'}
            }
        },
        
    ]
    rsp = SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute().get('replies')
    slideID = rsp[0]['createSlide']['objectId']

    print('** Fetch "main point" slide title (textbox) ID')
    rsp = SLIDES.presentations().pages().get(presentationId=deckID,
            pageObjectId=slideID).execute().get('pageElements')
    textboxID4 = rsp[0]['objectId']

    text2=['Nepal is the smallest country in South Asia','It is a beautiful country']
    print('** Insert text & perform various formatting operations')

    #Next slide
    reqs = [
        # add 7 paragraphs
        {'insertText': {
            'text': f'{text2[0]} \n{text2[1]}',
            'objectId': textboxID4,
        }},
        # shrink text from 48pt ("main point" textbox default) to 32pt
        {'updateTextStyle': {
            'objectId': textboxID4,
            'style': {'fontSize': {'magnitude': 25, 'unit': 'PT'}},
            'textRange': {'type': 'ALL'},
            'fields': 'fontSize',
        }},
        # bulletize everything
        {'createParagraphBullets': {
            'objectId': textboxID4,
            'textRange': {'type': 'ALL'}},
        },
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=deckID).execute()

    my_presentation = SLIDES.presentations().get(presentationId=deckID).execute()
    # print(my_presentation)

    print('** Done!')

    return deckID

def generateSlidesFromAPI(content):
    return "this is slide"

if __name__=="__main__":
    doEverything()