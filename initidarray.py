from conf import imdb_id_start_from
from conf import imdb_id_stop_in



def initidarray():
    temparr = []
    idarr = []
    print 'init id array...!this might take some time if the gap is big'
    start = imdb_id_start_from
    stop = imdb_id_stop_in
    for i in xrange(imdb_id_start_from,imdb_id_stop_in):
        temparr.append(start)
        start += 1
        if start == stop:
            temparr.append(start)
            for x in temparr:
                numstr = str(x)
                if len(numstr) == 1:
                    id = '000000'+`x`
                    idarr.append(id)
                if len(numstr) == 2:
                    id = '00000'+`x`
                    idarr.append(id)
                if len(numstr) == 3:
                    id = '0000'+`x`
                    idarr.append(id)
                if len(numstr) == 4:
                    id = '000'+`x`
                    idarr.append(id)
                if len(numstr) == 5:
                    id = '00'+`x`
                    idarr.append(id)
                if len(numstr) == 6:
                    id = '0'+`x`
                    idarr.append(id)
                if len(numstr) == 7:
                    id = ''+`x`
                    idarr.append(id)
            return idarr




#!deprecated!
def initidarr():
  idarr = []
  print '|-->Initializing array...'
  for i in xrange(0,9999999):
    if i < 10:
        idarr.append('000000'+`i`)
    if i >= 10 and i <= 99:
        idarr.append('00000'+`i`)
    if i >= 100 and i <= 999:
        idarr.append('0000'+`i`)
    if i >= 4900 and i <= 9999:
        idarr.append('000'+`i`)
    if i >= 68475 and i <= 99999:
        idarr.append('00'+`i`)
    if i >= 100000 and i <= 999999:
        idarr.append('0'+`i`)
    if i >= 1000000 and i <= 9999999:
        idarr.append(i)
    if i == imdb_id_stop_in+2:
        return idarr
    print i




