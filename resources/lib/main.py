from __future__ import unicode_literals
_AB='plugin.video.jiotv'
_AA='inputstream.adaptive.license_key'
_A9='inputstream.adaptive.manifest_type'
_A8='inputstream.adaptive.stream_headers'
_A7='inputstream'
_A6='IsPlayable'
_A5='properties'
_A4='isCatchupAvailable'
_A3='channel_name'
_A2='episode_desc'
_A1='description'
_A0='showGenre'
_z='mediatype'
_y='episodeguide'
_x='tvshowtitle'
_w='originaltitle'
_v='clearlogo'
_u='clearart'
_t='Languages'
_s='Genres'
_r='/resources/lib/main:show_featured'
_q='utf-8'
_p='JioTV'
_o='mobile'
_n='mpd'
_m='channelCategoryId'
_l='Extra'
_k='languageIdMapping'
_j='channelCategoryMapping'
_i='end'
_h='begin'
_g='programId'
_f=' %I:%M %p ]   %a'
_e='    [ %I:%M %p -'
_d='genre'
_c='enabled'
_b='addonid'
_a='Addons.SetAddonEnabled'
_Z='%Y%m%dT%H%M%S'
_Y='episode_num'
_X='duration'
_W='director'
_V='episode'
_U=False
_T='channelLanguageId'
_S='showtime'
_R='title'
_Q='info'
_P='endEpoch'
_O='fanart'
_N=True
_M='srno'
_L='logoUrl'
_K='params'
_J='thumb'
_I='art'
_H='showname'
_G='episodePoster'
_F=None
_E='icon'
_D='startEpoch'
_C='callback'
_B='label'
_A='channel_id'
from xbmcaddon import Addon
from xbmc import executebuiltin,log,LOGINFO
from xbmcgui import Dialog,DialogProgress
from codequick import Route,run,Listitem,Resolver,Script
from codequick.utils import keyboard
from codequick.script import Settings
from codequick.storage import PersistentDict
from resources.lib.utils import getTokenParams,getHeaders,isLoggedIn,login as ULogin,logout as ULogout,check_addon,sendOTPV2,get_local_ip,getChannelHeaders,quality_to_enum,_setup,kodi_rpc,Monitor,getCachedChannels,getCachedDictionary,cleanLocalCache,getFeatured
from resources.lib.constants import GET_CHANNEL_URL,IMG_CATCHUP,PLAY_URL,IMG_CATCHUP_SHOWS,CATCHUP_SRC,M3U_SRC,EPG_SRC,M3U_CHANNEL,IMG_CONFIG,EPG_PATH
import urlquick
from uuid import uuid4
from urllib.parse import urlencode
import inputstreamhelper,json
from time import time,sleep
from datetime import datetime,timedelta,date
import m3u8,requests,gzip,xml.etree.ElementTree as ET,os
monitor=Monitor()
@Route.register
def root(plugin):
	A='cms/TKSS_Carousal1.jpg';yield Listitem.from_dict(**{_B:'Featured',_I:{_J:IMG_CATCHUP_SHOWS+A,_E:IMG_CATCHUP_SHOWS+A,_O:IMG_CATCHUP_SHOWS+A},_C:Route.ref(_r)})
	for B in [_s,_t]:yield Listitem.from_dict(**{_B:B,_C:Route.ref('/resources/lib/main:show_listby'),_K:{'by':B}})
@Route.register
def show_featured(plugin,id=_F):
	G='showStatus';F='id';D='data'
	for C in getFeatured():
		if id:
			if int(C.get(F,0))==int(id):
				H=C.get(D,[])
				for A in H:
					B={_I:{_J:IMG_CATCHUP_SHOWS+A.get(_G,''),_E:IMG_CATCHUP_SHOWS+A.get(_G,''),_O:IMG_CATCHUP_SHOWS+A.get(_G,''),_u:IMG_CATCHUP+A.get(_L,''),_v:IMG_CATCHUP+A.get(_L,'')},_Q:{_w:A.get(_H),_x:A.get(_H),_d:A.get(_A0),'plot':A.get(_A1),_y:A.get(_A2),_V:0 if A.get(_Y)==-1 else A.get(_Y),'cast':A.get('starCast','').split(', '),_W:A.get(_W),_X:A.get(_X)*60,'tag':A.get('keywords'),_z:'movie'if A.get('channel_category_name')=='Movies'else _V}}
					if A.get(G)=='Now':B[_B]=B[_Q][_R]=A.get(_H,'')+' [COLOR red] [ LIVE ] [/COLOR]';B[_C]=play;B[_K]={_A:A.get(_A)};yield Listitem.from_dict(**B)
					elif A.get(G)=='future':E=datetime.fromtimestamp(int(A.get(_D,0)*0.001)).strftime(_e)+datetime.fromtimestamp(int(A.get(_P,0)*0.001)).strftime(_f);B[_B]=B[_Q][_R]=A.get(_H,'')+' [COLOR green]%s[/COLOR]'%E;B[_C]='';yield Listitem.from_dict(**B)
					elif A.get(G)=='catchup':E=datetime.fromtimestamp(int(A.get(_D,0)*0.001)).strftime(_e)+datetime.fromtimestamp(int(A.get(_P,0)*0.001)).strftime(_f);B[_B]=B[_Q][_R]=A.get(_H,'')+' [COLOR yellow]%s[/COLOR]'%E;B[_C]=play;B[_K]={_A:A.get(_A),_S:A.get(_S,'').replace(':',''),_M:datetime.fromtimestamp(int(A.get(_D,0)*0.001)).strftime('%Y%m%d'),_g:A.get(_M,''),_h:datetime.utcfromtimestamp(int(A.get(_D,0)*0.001)).strftime(_Z),_i:datetime.utcfromtimestamp(int(A.get(_P,0)*0.001)).strftime(_Z)};yield Listitem.from_dict(**B)
		else:yield Listitem.from_dict(**{_B:C.get('name'),_I:{_J:IMG_CATCHUP_SHOWS+C.get(D,[{}])[0].get(_G),_E:IMG_CATCHUP_SHOWS+C.get(D,[{}])[0].get(_G),_O:IMG_CATCHUP_SHOWS+C.get(D,[{}])[0].get(_G)},_C:Route.ref(_r),_K:{F:C.get(F)}})
@Route.register
def show_listby(plugin,by):
	B=getCachedDictionary();E=B.get(_j);F=B.get(_k);C=list(F.values());C.append(_l);G={_s:E.values(),_t:C}
	for A in G[by]:D=IMG_CONFIG[by].get(A,{}).get('tvImg',''),;H=IMG_CONFIG[by].get(A,{}).get('promoImg','');yield Listitem.from_dict(**{_B:A,_I:{_J:D,_E:D,_O:H},_C:Route.ref('/resources/lib/main:show_category'),_K:{'categoryOrLang':A,'by':by}})
@Route.register
def show_category(plugin,categoryOrLang,by):
	B=categoryOrLang;F=getCachedChannels();D=getCachedDictionary();G=D.get(_j);C=D.get(_k)
	def H(x):
		A=by.lower()[:-1]
		if A==_d:return G[str(x.get(_m))]==B
		elif B==_l:return str(x.get(_T))not in C.keys()
		else:
			if str(x.get(_T))not in C.keys():return _U
			return C[str(x.get(_T))]==B
	for A in filter(H,F):
		if A.get('channelIdForRedirect'):continue
		E=Listitem.from_dict(**{_B:A.get(_A3),_I:{_J:IMG_CATCHUP+A.get(_L),_E:IMG_CATCHUP+A.get(_L),_O:IMG_CATCHUP+A.get(_L),_v:IMG_CATCHUP+A.get(_L),_u:IMG_CATCHUP+A.get(_L)},_C:play,_K:{_A:A.get(_A)}})
		if A.get(_A4):E.context.container(show_epg,'Catchup',0,A.get(_A))
		yield E
@Route.register
def show_epg(plugin,day,channel_id):
	D=channel_id;F=urlquick.get(CATCHUP_SRC.format(day,D),max_age=-1).json();G=sorted(F['epg'],key=lambda show:show[_D],reverse=_U);H='[COLOR red] [ LIVE ] [/COLOR]'
	for A in G:
		B=int(time()*1000)
		if not A['stbCatchupAvailable']or A[_D]>B:continue
		I=A[_D]<B and A[_P]>B;E='   '+H if I else datetime.fromtimestamp(int(A[_D]*0.001)).strftime(_e)+datetime.fromtimestamp(int(A[_P]*0.001)).strftime(_f);yield Listitem.from_dict(**{_B:A[_H]+E,_I:{_J:IMG_CATCHUP_SHOWS+A[_G],_E:IMG_CATCHUP_SHOWS+A[_G],_O:IMG_CATCHUP_SHOWS+A[_G]},_C:play,_Q:{_R:A[_H]+E,_w:A[_H],_x:A[_H],_d:A[_A0],'plot':A[_A1],_y:A.get(_A2),_V:0 if A[_Y]==-1 else A[_Y],'cast':A['starCast'].split(', '),_W:A[_W],_X:A[_X]*60,'tag':A['keywords'],_z:_V},_K:{_A:A.get(_A),_S:A.get(_S,'').replace(':',''),_M:datetime.fromtimestamp(int(A.get(_D,0)*0.001)).strftime('%Y%m%d'),_g:A.get(_M,''),_h:datetime.utcfromtimestamp(int(A.get(_D,0)*0.001)).strftime(_Z),_i:datetime.utcfromtimestamp(int(A.get(_P,0)*0.001)).strftime(_Z)}})
	if int(day)==0:
		for C in range(-1,-7,-1):J='Yesterday'if C==-1 else (date.today()+timedelta(days=C)).strftime('%A %d %B');yield Listitem.from_dict(**{_B:J,_C:Route.ref('/resources/lib/main:show_epg'),_K:{'day':C,_A:D}})
@Resolver.register
@isLoggedIn
def play_ex(plugin,dt=_F):
	G='default_logo';F='lUrl';E='drm';D='proto';A=dt;C=inputstreamhelper.Helper(A.get(D,_n),drm=A.get(E))
	if C.check_inputstream():
		H=A.get(F)and A.get(F).replace('{HEADERS}',urlencode(getHeaders())).replace('{TOKEN}',urlencode(getTokenParams()));B={}
		if A.get(G):B[_J]=B[_E]=IMG_CATCHUP+A.get(G)
		return Listitem().from_dict(**{_B:A.get(_B)or plugin._title,_I:B or _F,_C:A.get('pUrl'),_A5:{_A6:_N,_A7:C.inputstream_addon,_A8:A.get('hdrs'),_A9:A.get(D,_n),'inputstream.adaptive.license_type':A.get(E),_AA:H}})
@Resolver.register
@isLoggedIn
def play(plugin,channel_id,showtime=_F,srno=_F,programId=_F,begin=_F,end=_F):
	V='user-agent';U='__hdnea__';T='stream_type';N=showtime;M=channel_id;L='cookie';K='result';F='?';W=inputstreamhelper.Helper(_n,drm='com.widevine.alpha');X=W.check_inputstream()
	if not X:return
	A={_A:int(M),T:'Seek'};O=_U
	if N and srno:O=_N;A[_S]=N;A[_M]=srno;A[T]='Catchup';A[_g]=programId;A[_h]=begin;A[_i]=end;Script.log(str(A),lvl=Script.INFO)
	C=getHeaders();C['channelid']=str(M);C[_M]=str(uuid4())if _M not in A else A[_M];Y=urlquick.post(GET_CHANNEL_URL,json=A,headers=getChannelHeaders(),max_age=-1);G=Y.json();H={};E=G.get(K,'').split(F)[0].split('/')[-1];H[_J]=H[_E]=IMG_CATCHUP+E.replace('.m3u8','.png');P=U+G.get(K,'').split(U)[-1];C[L]=P;B=G.get(K,'');Q=Settings.get_string('quality');R='adaptive'
	if Q=='Manual':R='ask-quality'
	else:
		I={};I[V]=C[V];I[L]=P;Z=urlquick.get(B,headers=I,max_age=-1,raise_for_status=_N);a=Z.text;D=m3u8.loads(a)
		if D.is_variant and(D.version is _F or D.version<7):
			S=quality_to_enum(Q,len(D.playlists))
			if O:
				J=D.playlists[S].uri
				if F in J:B=B.split(F)[0].replace(E,J)
				else:B=B.replace(E,J.split(F)[0])
				del C[L]
			else:B=B.replace(E,D.playlists[S].uri)
	Script.log(B,lvl=Script.INFO);return Listitem().from_dict(**{_B:plugin._title,_I:H,_C:B,_A5:{_A6:_N,_A7:'inputstream.adaptive','inputstream.adaptive.stream_selection_type':R,'inputstream.adaptive.chooser_resolution_secure_max':'4K',_A8:urlencode(C),_A9:'hls',_AA:'|'+urlencode(C)+'|R{SSM}|'}})
@Script.register
def login(plugin):
	G='headers';F='Login';C=Dialog().yesno(F,'Select Login Method',yeslabel='Keyboard',nolabel='WEB')
	if C==1:
		D=Dialog().yesno(F,'Select Login Type',yeslabel='OTP',nolabel='Password')
		if D==1:
			A=Settings.get_string(_o)
			if not A or len(A)!=10:A=Dialog().numeric(0,'Enter your Jio mobile number')
			E=sendOTPV2(A)
			if E:Script.notify('Login Error',E);return
			H=Dialog().numeric(0,'Enter OTP');ULogin(A,H,mode='otp')
		elif D==0:I=keyboard('Enter your Jio mobile number or email');J=keyboard('Enter your password',hidden=_N);ULogin(I,J)
	elif C==0:
		B=DialogProgress();B.create(_p,'Visit [B]http://%s:48996/[/B] to login'%get_local_ip())
		for K in range(120):
			sleep(1)
			with PersistentDict(G)as L:M=L.get(G)
			if M or B.iscanceled():break
			B.update(K)
		B.close()
@Script.register
def setmobile(plugin):A=_AB;B=Addon(A);C=Settings.get_string(_o);D=Dialog().numeric(0,'Update Jio mobile number',C);kodi_rpc(_a,{_b:A,_c:_U});B.setSetting(_o,D);kodi_rpc(_a,{_b:A,_c:_N});monitor.waitForAbort(1);Script.notify('Jio number set','')
@Script.register
def applyall(plugin):A=_AB;kodi_rpc(_a,{_b:A,_c:_U});monitor.waitForAbort(1);kodi_rpc(_a,{_b:A,_c:_N});monitor.waitForAbort(1);Script.notify('All settings applied','')
@Script.register
def logout(plugin):ULogout()
@Script.register
def m3ugen(plugin,notify='yes'):
	I=getCachedChannels();C=getCachedDictionary();D=C.get(_j);E=C.get(_k);F='#EXTM3U x-tvg-url="%s"'%EPG_SRC
	for (J,A) in enumerate(I):
		if str(A.get(_T))not in E.keys():B=_l
		else:B=E[str(A.get(_T))]
		if str(A.get(_m))not in D.keys():G='Extragenre'
		else:G=D[str(A.get(_m))]
		if not Settings.get_boolean(B):continue
		K=B+';'+G;L=PLAY_URL+'channel_id={0}'.format(A.get(_A));H=''
		if A.get(_A4):H=' catchup="vod" catchup-source="{0}channel_id={1}&showtime={{H}}{{M}}{{S}}&srno={{Y}}{{m}}{{d}}&programId={{catchup-id}}" catchup-days="7"'.format(PLAY_URL,A.get(_A))
		F+=M3U_CHANNEL.format(tvg_id=A.get(_A),channel_name=A.get(_A3),group_title=K,tvg_chno=int(A.get('channel_order',J))+1,tvg_logo=IMG_CATCHUP+A.get(_L,''),catchup=H,play_url=L)
	with open(M3U_SRC,'w+')as M:M.write(F.replace('\xa0',' ').encode(_q).decode(_q))
	if notify=='yes':Script.notify(_p,'Playlist updated.')
@Script.register
def epg_setup(plugin):
	H='Epg setup in progress';E='UTF-8';Script.notify('Please wait',H);A=DialogProgress();A.create(H);C=Settings.get_string('epgurl')
	if not C or len(C)<5:C='https://cdn.jsdelivr.net/gh/mitthu786/tvepg/epg.xml.gz'
	I={};J={};K=requests.request('GET',C,headers=J,data=I)
	with open(EPG_PATH,'wb')as B:B.write(K.content)
	A.update(20)
	with gzip.open(EPG_PATH,'rb')as B:L=B.read();M=L.decode(_q);F=ET.fromstring(M)
	A.update(30);A.update(35);A.update(45)
	for D in F.iterfind('.//programme'):N=D.find(_E);O=N.get('src');P=O.rsplit('/',1)[-1];Q=os.path.splitext(P)[0];D.set('catchup-id',Q);G=D.find(_R);G.text=G.text.strip()
	A.update(60);R='<?xml version="1.0" encoding="UTF-8"?>\n';S='<!DOCTYPE tv SYSTEM "xmltv.dtd">\n';T=R.encode(E)+S.encode(E)+ET.tostring(F,encoding=E);U=gzip.compress(T);A.update(80)
	with open(EPG_PATH,'wb')as B:B.write(U)
	A.update(100);A.close();Script.notify(_p,'Epg generated')
@Script.register
def pvrsetup(plugin):
	C='0';executebuiltin('RunPlugin(plugin://plugin.video.jiotv/resources/lib/main/m3ugen/)');B='pvr.iptvsimple'
	def A(id,value):
		A=value
		if Addon(B).getSetting(id)!=A:Addon(B).setSetting(id,A)
	if check_addon(B):A('m3uPathType',C);A('m3uPath',M3U_SRC);A('epgPathType','1');A('epgUrl',EPG_SRC);A('catchupEnabled','true');A('catchupWatchEpgBeginBufferMins',C);A('catchupWatchEpgEndBufferMins',C)
	_setup(M3U_SRC,EPG_SRC)
@Script.register
def cleanup(plugin):urlquick.cache_cleanup(-1);cleanLocalCache();Script.notify('Cache Cleaned','')