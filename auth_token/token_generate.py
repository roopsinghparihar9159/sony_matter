from __future__ import unicode_literals
import yt_dlp as youtube_dl
import cms_edgeauth
import conf

try:
    token = cms_edgeauth.ExportToken.token
    URL = f"{conf.baseurl}{conf.uri}?hdnea={token}"
    print(f"token: {token}")
    print(URL)
    print('---------')
    print(token)
        
except Exception as e:
    print(e)
