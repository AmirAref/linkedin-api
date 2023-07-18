# custom exceptions
class PageNotFound(Exception) :
    """ an exception raised when the page is not exists ! """
    pass
class PostNotFound(Exception) :
    """ an exception raised when the specific post section is not exists ! """
    pass