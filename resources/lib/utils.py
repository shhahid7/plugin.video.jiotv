from __future__ import unicode_literals
_i='result'
_h='tvYR7NSNn7rymo3F'
_g='plaYtv/7.0.8 (Linux;Android 9) ExoPlayerLib/2.11.7'
_f='usergroup'
_e='osversion'
_d='deviceId'
_c='uniqueid'
_b='userid'
_a='RJIL_JioTV'
_Z='okhttp/4.2.2'
_Y='appname'
_X='number'
_W='username'
_V='Retry after sometime'
_U='Connection error '
_T='message'
_S='user-agent'
_R='crmid'
_Q='ssotoken'
_P='name'
_O='password'
_N='dictionary'
_M='channelList'
_L='version'
_K='ascii'
_J='+91'
_I='headers'
_H='phone'
_G='os'
_F='devicetype'
_E=None
_D='android'
_C='localdb'
_B=True
_A=False
import os,urlquick
from uuid import uuid4
import base64,hashlib,time
from functools import wraps
from distutils.version import LooseVersion
from codequick import Script
from codequick.storage import PersistentDict
from xbmc import executebuiltin
from xbmcgui import Dialog,DialogProgress
from xbmcaddon import Addon
import xbmc,xbmcvfs
from contextlib import contextmanager
from collections import defaultdict
import socket,json
from resources.lib.constants import CHANNELS_SRC,DICTIONARY_URL,FEATURED_SRC
def get_local_ip():
	A=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);A.settimeout(0)
	try:A.connect(('8.8.8.8',80));B=A.getsockname()[0]
	except Exception:B='127.0.0.1'
	finally:A.close()
	return B
def isLoggedIn(func):
	'\n    Decorator to ensure that a valid login is present when calling a method\n    ';B=func
	@wraps(B)
	def A(*C,**D):
		J='RunPlugin(plugin://plugin.video.jiotv/resources/lib/main/login/)';I='Login Error'
		with PersistentDict(_C)as A:E=A.get(_W);F=A.get(_O);G=A.get(_I);H=A.get('exp',0)
		if G and H>time.time():return B(*(C),**D)
		elif E and F:login(E,F);return B(*(C),**D)
		elif G and H<time.time():Script.notify(I,'Session expired. Please login again');executebuiltin(J);return _A
		else:Script.notify(I,'You need to login with Jio Username and password to use this add-on');executebuiltin(J);return _A
	return A
def login(username,password,mode='unpw'):
	S='subscriberId';R='ssoToken';Q='User-Agent';P='androidId';O='platform';N='type';M='info';L='consumptionDeviceName';K='deviceInfo';J='otp';G=mode;F=password;E='user';D='sessionAttributes';B=username;A=_E
	if G==J:T=_J+B;U={_X:base64.b64encode(T.encode(_K)).decode(_K),J:F,K:{L:'unknown sdk_google_atv_x86',M:{N:_D,O:{_P:'generic_x86'},P:str(uuid4())}}};A=urlquick.post('https://jiotvapi.media.jio.com/userservice/apis/v1/loginotp/verify',json=U,headers={Q:_Z,_F:_H,_G:_D,_Y:_a},max_age=-1,verify=_A,raise_for_status=_A).json()
	else:V={'identifier':B if'@'in B else _J+B,_O:F,'rememberUser':'T','upgradeAuth':'Y','returnSessionDetails':'T',K:{L:'ZUK Z1',M:{N:_D,O:{_P:'ham',_L:'8.0.0'},P:str(uuid4())}}};A=urlquick.post('https://api.jio.com/v3/dip/user/{0}/verify'.format(G),json=V,headers={Q:'JioTV','x-api-key':'l7xx75e822925f184370b2e25170c5d5820a','Content-Type':'application/json'},max_age=-1,verify=_A,raise_for_status=_A).json()
	if A.get(R,'')!='':
		W={_Q:A.get(R),_b:A.get(D,{}).get(E,{}).get('uid'),_c:A.get(D,{}).get(E,{}).get('unique'),_R:A.get(D,{}).get(E,{}).get(S),'subscriberid':A.get(D,{}).get(E,{}).get(S)};H={_d:str(uuid4()),_F:_H,_G:_D,_e:'9',_S:_g,_f:_h,'versioncode':'289','dm':'ZUK ZUK Z1'};H.update(W)
		with PersistentDict(_C)as C:
			C[_I]=H;C['exp']=time.time()+31536000
			if G=='unpw':C[_W]=B;C[_O]=F
		Script.notify('Login Success','');return _E
	else:Script.log(A,lvl=Script.INFO);I=A.get(_T,'Unknow Error');Script.notify('Login Failed',I);return I
def sendOTPV2(mobile):
	A=mobile
	if _J not in A:A=_J+A
	B={_X:base64.b64encode(A.encode(_K)).decode(_K)};Script.log(B,lvl=Script.ERROR);C=urlquick.post('https://jiotvapi.media.jio.com/userservice/apis/v1/loginotp/send',json=B,headers={_S:_Z,_G:_D,'host':'jiotvapi.media.jio.com',_F:_H,_Y:_a},max_age=-1,verify=_A,raise_for_status=_A)
	if C.status_code!=204:return C.json().get('errors',[{}])[-1].get(_T)
	return _E
def logout():
	with PersistentDict(_C)as A:del A[_I]
	Script.notify("You've been logged out",'')
def getHeaders():
	with PersistentDict(_C)as A:return A.get(_I,_A)
def getCachedChannels():
	with PersistentDict(_C)as A:
		B=A.get(_M,_A)
		if not B:
			try:C=urlquick.get(CHANNELS_SRC).json().get(_i);A[_M]=C
			except:Script.notify(_U,_V)
		return A.get(_M,_A)
def getCachedDictionary():
	B='utf8'
	with PersistentDict(_C)as A:
		C=A.get(_N,_A)
		if not C:
			try:D=urlquick.get(DICTIONARY_URL).text.encode(B)[3:].decode(B);A[_N]=json.loads(D)
			except:Script.notify(_U,_V)
		return A.get(_N,_A)
def getFeatured():
	try:A=urlquick.get(FEATURED_SRC,headers={_f:_h,_G:_D,_F:_H,'versionCode':'290'},max_age=-1).json();return A.get('featuredNewData',[])
	except:Script.notify(_U,_V)
def cleanLocalCache():
	with PersistentDict(_C)as A:del A[_M];del A[_N]
def getChannelHeaders():A=getHeaders();return{_Q:A[_Q],'userId':A[_b],'uniqueId':A[_c],_R:A[_R],_S:_g,'deviceid':A[_d],_F:_H,_G:_D,_e:'9'}
def getTokenParams():
	def B(x):return base64.b64encode(hashlib.md5(x.encode()).digest()).decode().replace('=','').replace('+','-').replace('/','_').replace('\r','').replace('\n','')
	A=str(int(time.time()+3600*9.2));C=B('cutibeau2ic9p-O_v1qIyd6E-rf8_gEOQ'+A);return{'jct':C,'pxe':A,'st':'9p-O_v1qIyd6E-rf8_gEOQ'}
def check_addon(addonid,minVersion=_A):
	'Checks if selected add-on is installed.';D='Error';B=minVersion;A=addonid
	try:
		C=Script.get_info(_L,A)
		if B and LooseVersion(C)<LooseVersion(B):Script.log("{addon} {curVersion} doesn't setisfy required version {minVersion}.".format(addon=A,curVersion=C,minVersion=B));Dialog().ok(D,'{minVersion} version of {addon} is required to play this content.'.format(addon=A,minVersion=B));return _A
		return _B
	except RuntimeError:
		Script.log('{addon} is not installed.'.format(addon=A))
		if not _install_addon(A):Dialog().ok(D,'[B]{addon}[/B] is missing on your Kodi install. This add-on is required to play this content.'.format(addon=A));return _A
		return _B
def _install_addon(addonid):
	'Install addon.';A=addonid
	try:executebuiltin('InstallAddon({})'.format(A),wait=_B);B=Script.get_info(_L,A);Script.log('{addon} {version} add-on installed from repo.'.format(addon=A,version=B));return _B
	except RuntimeError:Script.log('{addon} add-on not installed.'.format(addon=A));return _A
def quality_to_enum(quality_str,arr_len):
	'Converts quality into a numeric value. Max clips to fall within valid bounds.';B=arr_len;A=quality_str;C={'Best':B-1,'High':4,'Medium+':3,'Medium':2,'Low':1,'Lowest':0}
	if A in C:return min(C[A],B-1)
	return 0
_signals=defaultdict(list)
_skip=defaultdict(int)
def emit(signal,*B,**C):
	A=signal
	if _skip[A]>0:_skip[A]-=1;return
	for D in _signals.get(A,[]):D(*(B),**C)
class Monitor(xbmc.Monitor):
	def onSettingsChanged(A):emit('on_settings_changed')
monitor=Monitor()
def kodi_rpc(method,params=_E,raise_on_error=_A):
	E='error';D=method;A=params
	try:
		B={'jsonrpc':'2.0','id':1};B.update({'method':D})
		if A:B['params']=A
		C=json.loads(xbmc.executeJSONRPC(json.dumps(B)))
		if E in C:raise Exception('Kodi RPC "{} {}" returned Error: "{}"'.format(D,A or'',C[E].get(_T)))
		return C[_i]
	except Exception as F:
		if raise_on_error:raise
		else:return{}
def set_kodi_setting(key,value):return kodi_rpc('Settings.SetSettingValue',{'setting':key,'value':value})
def same_file(path_a,path_b):
	D=path_b;C=path_a
	if C.lower().strip()==D.lower().strip():return _B
	A=os.stat(C)if os.path.isfile(C)else _E
	if not A:return _A
	B=os.stat(D)if os.path.isfile(D)else _E
	if not B:return _A
	return A.st_dev==B.st_dev and A.st_ino==B.st_ino and A.st_mtime==B.st_mtime
def safe_copy(src,dst,del_src=_A):
	B=src;A=dst;B=xbmcvfs.translatePath(B);A=xbmcvfs.translatePath(A)
	if not xbmcvfs.exists(B)or same_file(B,A):return
	if xbmcvfs.exists(A):
		if xbmcvfs.delete(A):Script.log('Deleted: {}'.format(A))
		else:Script.log('Failed to delete: {}'.format(A))
	if xbmcvfs.copy(B,A):Script.log('Copied: {} > {}'.format(B,A))
	else:Script.log('Failed to copy: {} > {}'.format(B,A))
	if del_src:xbmcvfs.delete(B)
@contextmanager
def busy():
	xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
	try:yield
	finally:xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
def _setup(m3uPath,epgUrl):
	N='instance-settings-1.xml';M='.bu';H='enabled';G='addonid';F='Addons.SetAddonEnabled';A=DialogProgress();A.create('PVR Setup in progress');D='pvr.iptvsimple';L=Addon(D);O=L.getAddonInfo(_P);B=xbmcvfs.translatePath(L.getAddonInfo('profile'));I=os.path.join(B,'instance-settings-91.xml');kodi_rpc(F,{G:D,H:_A});A.update(10)
	if LooseVersion(L.getAddonInfo(_L))>=LooseVersion('20.8.0'):
		xbmcvfs.delete(I)
		for C in os.listdir(B):
			if C.startswith('instance-settings-')and C.endswith('.xml'):
				J=os.path.join(B,C)
				with open(J)as E:K=E.read()
				if 'id="m3uPath">{}</setting>'.format(m3uPath)in K or 'id="epgUrl">{}</setting>'.format(epgUrl)in K:xbmcvfs.delete(os.path.join(B,J))
				else:safe_copy(J,J+M,del_src=_B)
		A.update(25);kodi_rpc(F,{G:D,H:_B})
		while not os.path.exists(os.path.join(B,N)):monitor.waitForAbort(1)
		kodi_rpc(F,{G:D,H:_A});monitor.waitForAbort(1);safe_copy(os.path.join(B,N),I,del_src=_B);A.update(35)
		with open(I,'r')as E:K=E.read()
		with open(I,'w')as E:E.write(K.replace('Migrated Add-on Config',O))
		A.update(50)
		for C in os.listdir(B):
			if C.endswith(M):safe_copy(os.path.join(B,C),os.path.join(B,C[:-3]),del_src=_B)
		kodi_rpc(F,{G:D,H:_B});A.update(70)
	else:kodi_rpc(F,{G:D,H:_B});A.update(70)
	set_kodi_setting('epg.futuredaystodisplay',7);set_kodi_setting('pvrmanager.syncchannelgroups',_B);set_kodi_setting('pvrmanager.preselectplayingchannel',_B);set_kodi_setting('pvrmanager.backendchannelorder',_B);set_kodi_setting('pvrmanager.usebackendchannelnumbers',_B);A.update(100);A.close();Script.notify('IPTV setup','Epg and playlist updated');return _B