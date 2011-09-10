import audiofile
import argparse
import sys
import os
from shutil import move

class PAudioOrganizer:
    def __init__(self):
        self.get_args()

    def get_args(self):
        """Get all the arguments from the command line"""
        parser = argparse.ArgumentParser(description="Organizes your library")
        parser.add_argument('-f', '--format', nargs = 1, required=True, help='Enter format for organizing the music') 
        parser.add_argument('-d', '--directory', nargs = '?', default = './', help='Enter the directory root. Default is ./')
        parser.add_argument('-v', '--verbose', action='store_true', help='For more verbose output')
        parser.add_argument('-et', '--edittitle', nargs = 2, help="Replace in Title")
        parser.add_argument('-ea', '--editartist', nargs = 2, help="Replace in Artist")
        parser.add_argument('-eA', '--editalbum', nargs = 2, help="Replace in Album")
        
        self.args = parser.parse_args(sys.argv[1:])
        #Correct the parameters
        if self.args.directory[-1] is not "/": self.args.directory = self.args.directory+"/"
        
        if self.args.verbose:
            print "Directory to work on: " + str(self.args.directory)
            print "Format to use: "+str(self.args.format)
            
    def recurse_directory(self):
        """Recurse the whole music directory so that we can operate on each file"""
        for dirpath, dirnames, filenames in os.walk(str(self.args.directory)):
            print "Now working in directory -> " + dirpath
            for file in filenames:
                src = dirpath+"/"+file
                music_file = audiofile.AudioFile(src)
                
                meta_data = [music_file.getArtist(), music_file.getAlbum(), music_file.getTitle()]
                
                #Replace metadata if required. like the shitty www.songs.pk.
                if self.args.editartist is not None:
                    meta_data[0] = meta_data[0].replace(self.args.editartist[0],self.args.editartist[1])
                if self.args.editalbum is not None:
                    meta_data[1] = meta_data[1].replace(self.args.editalbum[0],self.args.editalbum[1])
                if self.args.edittitle is not None:
                    meta_data[2] = meta_data[2].replace(self.args.edittitle[0],self.args.edittitle[1])
                
                #Making the destination according to format specified.
                dest = self.args.directory+self.args.format[0]+".mp3"
                #Removing / from filenames as its useless.
                dest = dest.replace("%artist%", meta_data[0].replace("/"," "))
                dest = dest.replace("%album%", meta_data[1].replace("/"," "))
                dest = dest.replace("%title%", meta_data[2].replace("/"," "))
                
                if self.args.verbose: print "PERFORMING: " + src + " --> " + dest
                
                self.move_wrapper(src, dest, music_file)
                
                
                                   
    def move_wrapper(self, src, dest, music_file):
        """Wrapper to move a file which handles all conditions"""
        #Strip the directory name.
        #TODO: Assumes that filename doesnt contain "/"
        dest_dir = dest[:dest.rfind("/")]

        #Check if the directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        #Now that we have the directories created. Lets move the file itself
        move(src,dest)
        try:
            #This src[:src.rfind("/")] find the path to the file by searching "/" from the right
            os.rmdir(src[:src.rfind("/")])
        except OSError:
            #Directory not empty so we want to pass it until it gets empty.
            pass

        
    def main(self):
        self.recurse_directory()
        

if __name__ == "__main__":
    app = PAudioOrganizer()
    app.main()
