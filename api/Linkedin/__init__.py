from bs4 import BeautifulSoup
import requests
import json
from .errors import *



class LinkedinPost():
    def __init__(self, url : str) -> None:
        self.url = url
        self.text : str = None
        self.reactions : int = 0 
        self.comments : int = 0
        self.images : list[str]= []
        self.document : Document = None
        self.videos : list[str]= []
    
    # functions
    def get_post_data(self, document_pages_limit : int = 15):
        #send request
        response = requests.get(self.url)
        # check status
        if response.status_code in range(400, 500):
            raise PageNotFound("Page not found error !")
        # parse the response
        soup = BeautifulSoup(response.content, "html.parser")
        
        # check the post section is exists
        post_section = soup.find('article')
        if not post_section:
            raise PostNotFound('post not exists !')
        
        # post text
        self.text = post_section.find('p', class_='attributed-text-segment-list__content').text
        
        # get post details
        post_detail = post_section.find('div', class_='main-feed-activity-card__social-actions')
        if post_detail:
            # get count of reactions and comments
            _reactions = post_detail.find(attrs={'data-id':'social-actions__reactions'})
            self.reactions = int(_reactions['data-num-reactions']) if _reactions else 0
            _reactions = post_detail.find(attrs={'data-id':'social-actions__comments'})
            self.comments = int(_reactions['data-num-comments']) if _reactions else 0
            
        # extract the post images
        _image_list = post_section.find('ul', attrs={'class':'feed-images-content'})
        if _image_list:
            self.images = [item['data-delayed-url'] for item in _image_list.find_all('img')]
        
        # extract the document
        _document = post_section.find('iframe', attrs={'data-id':'feed-paginated-document-content'})
        # extarct the images from document 
        if _document:
            _document = json.loads(_document['data-native-document-config'])
            # extract
            self.document = Document()
            self.document.title = _document['doc']['title']
            self.document.document = requests.get(_document['doc']['url']).json()['transcribedDocumentUrl']
            
        
        # get the video links
        _json_data = post_section.find('video')
        if _json_data:
            _json_data = json.loads(_json_data['data-sources'])
            self.videos = [item for item in _json_data]

    def to_dict(self):
        return vars(self)
    
class Document:
    def __init__(self) -> None:
        self.title : str = None
        self.document : str = None