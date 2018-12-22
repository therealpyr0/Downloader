from multiprocessing.dummy import Pool as ThreadPool
from config import *
import argparse,urllib2,base64,time

class Downloader():

    def getfilesize(self,url,username="",password=""):
        self.request=urllib2.Request(self.url)
        base64string=base64.b64encode('%s:%s' % (username,password))
        self.request.add_header("Authorization", "Basic %s" % base64string)
        result=urllib2.urlopen(self.request)
        size=result.headers['content-length']
        size=int(size)
        return size


    def downloadchunks(self,chunk):
        print(chunk)
        b="bytes=%s-%s"%(chunk[0],chunk[1])
        request=self.request
        request.add_header('Range',b)
        result=urllib2.urlopen(request)
        #data=result.read()
        f=open(os.path.join(self.tempfilelocation,str(chunk[2])+".temp"),"wb")
        buff=2048*10
        while True:
            data=result.read(buff)
            if not data :
                break
            f.write(data)
        f.close()
        return 0


    def createFolders(self):
        folders=[self.downloadlocation,self.tempfilelocation]
        for folder in folders:
            try:
                os.makedirs(folder)
            except:
                pass
        
    def parseargs(self):
        parser = argparse.ArgumentParser(description='A Multithreaded Downloader')
        parser.add_argument('--url', '-u', required=True, type=str, help='url')
        parser.add_argument('--username', '-o', required=True, type=str, help='username')
        parser.add_argument('--password', '-p', required=True, type=str, help='password')
        self.args = parser.parse_args()
        self.url = self.args.url
        self.username = self.args.username
        self.password = self.args.password
        self.filename=self.url.split("/")[-1]


    def __init__(self):
        self.threadcount=THREAD_COUNT
        self.downloadlocation=DOWNLOAD_LOCATION
        self.tempfilelocation=TEMP_FILE_LOCATION
        self.tempindentifier=str(time.time())
        self.tempfilelocation=os.path.join(self.tempfilelocation,self.tempindentifier)
        self.createFolders()

        

    def dividefileparts(self,size):
        achunk=size/self.threadcount
        apair=[]
        chunkslist=[]
        initial=0
        final=achunk
        if (2*self.threadcount)>size:
            return [[0,size]]
        for i in xrange(self.threadcount-1):
            apair.append(initial)
            apair.append(final)
            apair.append(i+1)
            chunkslist.append(apair)
            initial=final+1
            final+=achunk
            apair=[]
        chunkslist.append([initial,size,self.threadcount])
        return chunkslist


    def threadpooler(self,chunkslist):
        pool = ThreadPool(self.threadcount)
        results = pool.map(self.downloadchunks,chunkslist)
        pool.close()
        pool.join()
        return results


    def mergefiles(self):
        fmain=open(os.path.join(self.downloadlocation,self.filename),"wb")
        print(self.downloadlocation,self.filename)
        for i in range(self.threadcount):
            print("reading file ",i+1)
            f=open(os.path.join(self.tempfilelocation,str(i+1)+".temp"),"rb")
            data=f.read()
            fmain.write(data)
            f.close()
        fmain.close()

    def main(self):
        self.parseargs()
        self.filesize=self.getfilesize(self.url,self.username,self.password)
        chunkslist=self.dividefileparts(self.filesize)
        print self.threadpooler(chunkslist)
        self.mergefiles()


if __name__ == "__main__":
    obj=Downloader()
    obj.main()