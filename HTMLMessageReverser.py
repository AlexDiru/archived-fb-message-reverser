from html.parser import HTMLParser
import codecs

HTMLFilename = "x.htm"
OutputFilename = "y.htm"

class Message:
    def __init__(self, name):
        self.Name = name
        self.Content = "[Image]"
        self.Date = ""
        
    def ToHTMLString(self):
        return "<div class=\"message\"><div class=\"message_header\"><span class=\"user\">" + self.Name + "</span><span class=\"meta\">" + self.Date + "</span></div></div><p>" + self.Content + "</p>"
        
    def PrintHTML(self):
        print(self.ToHTMLString())

class MyHTMLParser(HTMLParser):
    
    Messages = []
    InUser = False
    InDate = False
    InContent = False
    
    def handle_starttag(self, tag, attrs):
        if tag == "span":
            if attrs[0][0] == "class":
                if attrs[0][1] == "user":
                    self.InUser = True
                    self.InDate = False
                    self.InContent = False
                elif attrs[0][1] == "meta":
                    self.InUser = False
                    self.InDate = True
                    self.InContent = False
                
        if tag == "p":
            self.InUser = False
            self.InDate = False
            self.InContent = True
            
    def handle_endtag(self, tag):
        if tag == "p" and self.InContent == True:
            self.InUser = False
            self.InContent = False
            self.InDate = False

    def handle_data(self, data):
        if self.InUser == True:
            self.Messages.append(Message(data))
        elif self.InDate == True:
            self.Messages[-1].Date = data
            self.InDate = False
            self.InContent = True
        elif self.InContent == True:
            self.Messages[-1].Content = data
                         
    def OutputMessages(self):
        for message in reversed(self.Messages):
            message.PrintHTML()
            
    def MessagesAsString(self):
        HTMLString = ""
        for message in reversed(self.Messages):
            HTMLString += message.ToHTMLString()
        return HTMLString

HTMLFile = codecs.open(HTMLFilename, "r", encoding='utf-8')
HTMLData = HTMLFile.read()
Parser = MyHTMLParser()

Parser.feed(HTMLData)

OutputHTML = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /><title>Messages</title><link rel=\"stylesheet\" href=\"../html/style.css\" type=\"text/css\" /></head><body>"
OutputHTML += Parser.MessagesAsString()
OutputHTML += "</body></html>"

OutputHTMLFile = codecs.open(OutputFilename, "w", encoding='utf-8')
OutputHTMLFile.write(OutputHTML)



