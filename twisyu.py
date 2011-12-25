# -*- coding: utf-8 -*-

# @brief  This script search twit from word and get the user profile.
# @author Yasuharu Shibata <admin@mail.yasuharu.net>

import base64
import simplejson
import urllib2
import urllib
import sys

# @brief 検索結果の個数を指定します
SEARCH_WORD_NUM = 100;

# @brief get user description
# @ret dictionary of description.
def get_users_description(users):
	str_users = "";
	for u in users:
		str_users += u + ",";

	req = urllib2.Request(LOOKUP_URL + str_users);
	con = urllib2.urlopen(req);

	users_desc = {};
	for line in con:
		data = simplejson.loads(line);

		for u in data:
			if u.has_key("description") and u.has_key("screen_name"):
				users_desc[u["screen_name"]] = u["description"];

	return users_desc;

# @brief get dictionary of dedescription.
# @ret history list [[screen_name, text]]
def get_history():
	req = urllib2.Request(SEARCH_URL);
	con = urllib2.urlopen(req);

	ret = [];
	for line in con:
		data = simplejson.loads(line);

		if data.has_key("results") == False:
			return ret;

		for item in data["results"]:
			ret.append([item["from_user"], item["text"], item["created_at"]]);

	return ret;

# @brief gather user name from history.
def gather_user_from_history(history):
	ret = [];
	for item in history:
		user = item[0];
		ret.append(user);

	return ret;

# start main
argvs = sys.argv;
if len(argvs) != 2:
	print "Usage : python twisyu <search word>";
	quit();

# define each URL.
FIND_WORD  = argvs[1];
SEARCH_URL = 'http://search.twitter.com/search.json?q=' + urllib.quote(FIND_WORD);
LOOKUP_URL = 'http://api.twitter.com/1/users/lookup.json?rpp=' + str(SEARCH_WORD_NUM) + '&screen_name=';

history    = get_history();
users      = gather_user_from_history(history);
users_desc = get_users_description(users);

for h in history:
	user        = h[0];
	text        = h[1];
	date        = h[2];

	if users_desc.has_key(user) == False:
		continue;

	description = users_desc[user];

	try:
		print '-----';
		print 'User Name : ' + user.encode('utf-8', 'ignore');
		print 'Profile   : ' + description.encode('utf-8', 'ignore');
		print 'Text      : ' + text.encode('utf-8', 'ignore');
		print 'Date      : ' + date.encode('utf-8', 'ignore');
		print '-----';
	except:
		pass;

