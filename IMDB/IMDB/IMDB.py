import urllib2from BeautifulSoup import BeautifulSoupfrom mechanize import Browserimport re def getunicode(soup):	body=''	if isinstance(soup, unicode):		soup = soup.replace('&#39;',"'")		soup = soup.replace('&quot;','"')		soup = soup.replace('&nbsp;',' ')		body = body + soup	else:		if not soup.contents:			return ''		con_list = soup.contents		for con in con_list:			body = body + getunicode(con)	return body  def main(d,control):	f = open("ids.txt", 'r')	g=open("final_output3.txt","a")	file1 = f.readlines()	counter =0	for line in file1:		counter += 1		if (counter <= control):			print "%d processing:"%counter+line.split()[1]			imdb_dict = {}			url='http://www.imdb.com/title/'+line.split()[1]+'/'			page=urllib2.urlopen(url)			soup=BeautifulSoup(page.read())			movie_title = "%s"%soup.h1.find('span',itemprop='name').contents 						rate = soup.find('span',itemprop='ratingValue')			rating = ''#we used some conditional if since some movies do not have all information like rating,...on IMDB			if(rate):				rating = getunicode(rate)			actors=[]			actors_soup = soup.findAll('a',itemprop='actors')			for i in range(len(actors_soup)):				actors.append(getunicode(actors_soup[i]))			#des = soup.find('meta',{'name':'description'})['content']			genre=[]			infobar = soup.find('div',{'class':'infobar'})			r = ''			if (infobar.find('',{'title':True})!=None):				r = infobar.find('',{'title':True})['title']			genrelist = infobar.findAll('a',{'href':True})			for i in range(len(genrelist)-1):				genre.append(getunicode(genrelist[i]))						release_date =''			for i in soup.findAll((lambda tag: len(tag.attrs) == 1),attrs={"class" : "txt-block"}):				if (i.h4 and str(i.h4.contents).find("Release Date:")!=-1):					release_date =  i.contents[2].split('\n')[0]							director = soup.find('div',{'class':'rec-director rec-ellipsis'})			director1 =''			if (director):				director1=getunicode(director)			actor = soup.find('div',{'class':'rec-actor rec-ellipsis'})			actor1 = ''			if (actor):				actor1=getunicode(actor)			rev = soup.find('p',itemprop='reviewBody')#reviews			review = ''			if (rev):				review=getunicode(rev)			actors2=[]			actors_soup2 = soup.findAll('span',{'class':'itemprop'},{'itemprop':'name'})#actors			for i in range(len(actors_soup2)):				actors2.append(getunicode(actors_soup2[i]))                        if(soup.find('h4', attrs={"class" :"inline"}, text = 'Budget:')):#budget, gross has been crawled in the separate file since we needed to go another link                                budget = soup.find('h4', attrs={"class" :"inline"}, text = 'Budget:')                                budget=budget.next                              							imdb_dict ['id'] = str(line.split()[1])			imdb_dict ['film_name'] = movie_title			imdb_dict ['producer'] = line.split()[2]			imdb_dict ['rating'] = rating			imdb_dict ['Relase Date'] = release_date[3:25]			imdb_dict ['Rated'] = r			imdb_dict ['Genre'] = "["+', '.join(genre)+"]"			#tweet_dict ['Actor'] = ', '.join(actors2)			imdb_dict ['budget'] = budget[8:20]                        			#tweet_dict ['Description'] = des			d.append(imdb_dict)			#print "director1:"+director1			#print "actor1:"+actor1			#print "rev:"+str(rev)			#print "length:%d"%len(actor1)			                        g.write('[%s] %s [%s] [%s] %s [%s]   \n'%(imdb_dict ['id'],imdb_dict ['film_name'],imdb_dict ['rating'],imdb_dict ['Relase Date'],imdb_dict ['Genre'],imdb_dict ['budget'] ))        g.close 	    if __name__ == '__main__':	d=[]	main(d,1901)#1901 is number of ids	for each in d:		print "id: "+each['id']		print "film name: "+each['film_name']		print "producer: "+each['producer']		print "rating: "+each['rating']		print "Realease Date: "+each['Relase Date']		print "Rated: "+each['Rated']		print "Genre: "+each['Genre']		#print "Actor: "+each['Actor']		print "budget:"+each['budget']                		#print "Description: "+each['Description']		print ''		