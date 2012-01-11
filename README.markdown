# Wiki-dumps

Wiki-dumps is a program used to download the most current Wikipedia database 
dumps from [http://wikipedia.c3sl.ufpr.br](http://wikipedia.c3sl.ufpr.br),
generate metadata files, and ingest the database dumps and metadata into
[http://archive.org](http://archive.org).    

## Non Internet Archive Use
The program can easily be modified to suit general needs. Simply ignore
the `perpetual-wiki.php` file and use `wiki-d.py`. A few unecessary 
archive.org files will still be genearated, but the script will still
function properly.    

To prevent `wiki-d.py` from generating the unecessary files simply remove
the following code from `wiki-d.py`:

     ''' <Perpetual Loop Auto-submit business> '''
     list_home = os.getcwd()
     readyListFileName = "ready_list.txt"
     lockFileName = readyListFileName + ".lck"
     ### Exit if last list still pending, wait for it to be renamed/removed.
     if os.access( readyListFileName, os.F_OK ) is True:
         print ( 'ABORT: %s exists (Not picked up yet? Should be renamed'
                 'when retrieved by auto_submit loop!)' % readyListFileName )
         if os.access( lockFileName, os.F_OK ) is True:
             os.remove(lockFileName)
         exit(0)
     ### If lock file exists, another process is already generating the list
     if os.access( lockFileName, os.F_OK ) is True:
         print ( 'ABORT: %s lockfile exists (Another process generating list'
                 'already? Should be deleted when complete!)' % lockFileName )
         exit(0)
     ### Touch a lock and list file.
     touchLi = open(readyListFileName,'wb')
     touchLi.write('')
     touchLi.close()
     touchLo = open(lockFileName, 'wb')
     touchLo.write('')
     touchLo.close()
     ''' <Peprpetual Loop Auto-submit business /> '''

And the following line at the end of the script:

    os.remove(lockFileName)
