# -*- coding: utf-8 -*-

# @brief  This script search twit from word and get the user profile.
# @author Yasuharu Shibata <admin@mail.yasuharu.net>

import base64
import simplejson
import urllib2
import urllib
import sys

# @brief 検索結果の個数を指定します
SEARCH_RESULT_NUM = 100;

def get_users_description_divide(str_users, url, users_desc):
	req = urllib2.Request(url + str_users);
	con = urllib2.urlopen(req);

	for line in con:
		data = simplejson.loads(line);

		for u in data:
			if u.has_key("description") and u.has_key("screen_name"):
				users_desc[u["screen_name"]] = u["description"];

	return users_desc;

# @brief get user description
# @ret dictionary of description.
def get_users_description(users, url):
	users_desc = {};
	str_users  = "";
	i          = 0;
	for u in users:
		str_users += u + ",";
		i = i + 1;

		if i == 100:
			get_users_description_divide(str_users, url, users_desc);
			i = 0;
			str_users = "";

	if i > 0:
		get_users_description_divide(str_users, url, users_desc);

	return users_desc;

# @brief get dictionary of dedescription.
# @ret history list [[screen_name, text]]
def get_history(url):
	req = urllib2.Request(url);
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
search_word     = argvs[1];
search_url_base = 'http://search.twitter.com/search.json?rpp=' + str(SEARCH_RESULT_NUM) + '&q=' + urllib.quote(search_word);
user_lookup_url = 'http://api.twitter.com/1/users/lookup.json?screen_name=';

historys = [];
for i in range(10):
	history = get_history(search_url_base + "&page=" + str(i + 1));
	historys.extend(history);

users      = gather_user_from_history(historys);
users_desc = get_users_description(users, user_lookup_url);

for h in historys:
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

