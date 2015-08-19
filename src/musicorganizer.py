from fnmatch import fnmatch
import os, string, shutil, threading
import os.path
from tinytag import Flac
from tinytag import ID3
from tinytag import Ogg
from tinytag import StringWalker
from tinytag import TinyTag
from tinytag import Wave
from tkinter import *
from tkinter.filedialog import *

def main():
        
    root = Tk()
    root.title("Music Organizer")
    menuBar = Menu(root)
    
    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="Open folder...", command=open_dir)
    fileMenu.add_command(label="Exit", command=root.quit)
    menuBar.add_cascade(label="File", menu=fileMenu)
    
    
    #scrollbar = Scrollbar(root)
    #scrollbar.pack(side=RIGHT, fill=Y)
    
    global songList
    songList = Listbox(root, width=100)
    songList.pack()
    #songList.bind('<<ListboxSelect>>', on_select)
    
    #songList.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
    #scrollbar.config(command=songList.yview)
    
    global fileCount
    fileCount = Label(root, text="0 item(s)", anchor="w", width=100)
    fileCount.pack()
    
    global artistList
    artistList = Listbox(root, width=100)
    artistList.pack()
    
    global artistCount
    artistCount = Label(root, text="0 artist(s)", anchor="w", width=100)
    artistCount.pack()
    
    moveButton = Button(root, text="Do it!", width=100, command=move_it)
    moveButton.pack()
    
    global messageList
    messageList = Listbox(root, width=100)
    messageList.pack()

    root.config(menu=menuBar)
    root.mainloop()
    
def open_dir():
    t = threading.Thread(target=open_folder)
    t.start()
    
def open_folder():
    
    global parentDir
    parentDir = askdirectory(title='Please select a directory')
    
    artistList.delete(0, artistList.size())
    songList.delete(0, songList.size())
    
    global extensions
    extensions = ['*.mp3', '*.wav', '*.flac', "*.wma"]
    global matches
    matches = []
    global artistArray
    artistArray = []
    
    for path, dirnames, filenames in os.walk(parentDir):
        for extension in extensions:
            for filename in fnmatch.filter(filenames, extension):
                matches.append(os.path.join(path, filename).replace("/", "\\"))
                
    for i in range(len(matches)):
        artist = get_artist(matches[i])
            
        artistArray.append(artist)
        songList.insert(END, "{no}. {artist} - {path}".format(no=i + 1, path=matches[i], artist=artist) + " - %0.1f MB" % (os.path.getsize(matches[i]) / (1024 * 1024.0)))
        songList.yview(END)
        
    artistArray = list(set(artistArray))    
    
    fileCount['text'] = "%d item(s)" % len(matches)
    
    
    for i in range(len(artistArray)):
        artistList.insert(END, artistArray[i])
        artistList.yview(END)
        
    artistCount['text'] = "%d artist(s)" % len(artistArray)

def move_it():
    t = threading.Thread(target=create_artist_folder)
    t.start()
        
def get_artist(path):
    musicMeta = TinyTag.get(path)
    artist = musicMeta.artist
    
    if artist is not None:
        artist = ''.join(i for i in artist if i not in string.punctuation).replace(" ", "")
        
    if artist is None or not artist or artist.isspace():
        return "Unknown"
    else:
        return artist
    
def create_artist_folder():
    for i in range(len(artistArray)):
        path = parentDir + "\\" + artistArray[i]
        
        try:
            os.makedirs(path)
            messageList.insert(END, "Directory %s created!" % artistArray[i])
        except OSError as exception:
            messageList.insert(END, "Directory %s already exists." % artistArray[i])
            
        messageList.yview(END)
    
    t = threading.Thread(target=move_to_folder)
    t.start()
            
def move_to_folder():
    for i in range(len(matches)):
        try:
            folder = get_artist(matches[i])
            shutil.move(matches[i], parentDir + "\\" + folder)
            messageList.insert(END, "{pathTo} moved to folder \"{folderTo}\"!".format(pathTo=os.path.basename(matches[i]), folderTo=folder))
        except OSError as exception:
            messageList.insert(END, "============Something strange happen yo============")
        
        messageList.yview(END)
    
    for path, dirnames, _ in os.walk(parentDir):
        for dirname in dirnames:
            oldDir = parentDir + "/" + dirname
            if not os.listdir(oldDir):
                os.rmdir(oldDir)
            else:
                exist = FALSE
                for i in range(len(artistArray)):
                    if dirname == artistArray[i]:
                        exist = TRUE
                        break
                if exist is FALSE:
                    #messageList.insert(END, oldDir + " is not empty!")
                    shutil.rmtree(oldDir, ignore_errors=True)
        messageList.yview(END)
    
    messageList.insert(END, "=============Move complete==========")
    messageList.yview(END)
        
def on_select(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    os.startfile(matches[index])

if __name__ == "__main__": main()