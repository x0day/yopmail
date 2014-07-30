#coding = utf-8
_author_ = "DM_"

import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'
}

class yopmail():
	def __init__(self, user):
		self.user = user
		self.maildict = dict()
		self.maillst = self._getmaillst()

	def _getmaillst(self):
		loginurl = "http://m.yopmail.com/en/inbox.php?login=%s&yp=DAQL0AwV0ZwD2BGD1AmHjAj&yj=TZmR1AQL2AwpkBGVlAQRkAj&v=2.4" % self.user
		html = requests.get(loginurl, headers=headers).content
		try:
			maillst = re.findall('<div   class="um"><a class="lm_m" href="(?P<from>[\s\S]+?)">'
	                             '<span class="lmfd"><span class="lmh">(?P<time>[\s\S]+?)</span>'
	                             '<span  class="lmf">(?P<titile>[\s\S]+?)</span></span>'
	                             '<span class="lms_m">([\s\S]+?)</span>'
	                             '</a></div>', html)
		except:
			maillst = []

		for lst in maillst:
			maillink = "http://m.yopmail.com/" + lst[0]
			mailtime = lst[1]
			mailfrom = lst[2]
			mailtitle = lst[3]
			self.maildict[mailtitle] = dict()
			self.maildict[mailtitle]['from'] = mailfrom
			self.maildict[mailtitle]['link'] = maillink
			self.maildict[mailtitle]['time'] = mailtime

	def getmailcnt(self, title):
		if title in self.maildict.keys():
			link = self.maildict[title]["link"]

			try:
				html = requests.get(link, headers=headers).content
				mailcnt = re.findall('<div style=" overflow:scroll; width:100%; "  class="f20">([\s\S]+?)</div>', html)[0]
			except:
				mailcnt = ""	

			return mailcnt
