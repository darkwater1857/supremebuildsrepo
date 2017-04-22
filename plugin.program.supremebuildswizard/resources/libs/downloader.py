################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcgui, urllib, sys, time, uservar
from urllib import FancyURLopener
import socket
import wizard as wiz

timeout = 180
socket.setdefaulttimeout(timeout)
ADDONTITLE     = uservar.ADDONTITLE
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2

class customdownload(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'


def download(url, dest, dp = None):
	if not dp:
		dp = xbmcgui.DialogProgress()
		dp.create(ADDONTITLE ,"Downloading Content",' ', ' ')
	dp.update(0)
	start_time=time.time()
	customdownload().retrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, dp, start_time))


def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR orange]%.02f MB[/COLOR] of [B]%.02f MB[/B]' % (currently_downloaded, total)
            e = '[COLOR white][B]Speed: [/B][/COLOR][COLOR orange]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            e += '[COLOR white][B]ETA: [/B][/COLOR][COLOR orange]%02d:%02d' % divmod(eta, 60)  + '[/COLOR]'
            dp.update(percent, mbs, e)
	except Exception, e:
		wiz.log("ERROR Downloading: %s" % str(e), xbmc.LOGERROR)
		return str(e)
	if dp.iscanceled(): 
		dp.close()
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Download Cancelled[/COLOR]" % COLOR2)
		sys.exit()