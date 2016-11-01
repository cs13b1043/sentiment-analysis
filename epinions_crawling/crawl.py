from bs4 import BeautifulSoup
import urllib
import re
import simplejson
import os.path

root_url = 'http://www.epinions.com'

root = urllib.urlopen(root_url)
root_soup = BeautifulSoup(root, "lxml")


# list of products in each category which have reviews
def list_products(cat_soup):
	prod_dict = {}
	objs = cat_soup.find_all('li', attrs={"class":'searchRowView'})
	
	for obj in objs:
		#check if it's reviewed
		review = obj.find_all('span', attrs={"class":'readReviewPros'})
		if review:
			product_url = obj.find('a').get('href')
			product_name = obj.find('h3', attrs={"class":"searchResultTitle"}).string.strip()
			prod_dict[product_name] = product_url
	
	nxt = cat_soup.find('li', attrs={"id":'linkMore'})
	
	if not nxt:
		return prod_dict
	else:
		nxt_url = nxt.find('a').get('href')
		nxt_page = urllib.urlopen(nxt_url)
		next_soup = BeautifulSoup(nxt_page, "lxml")
		
		print "Connecting to ... " + nxt_url
		
		prod_dict.update(list_products(next_soup))
		return prod_dict
	
def pros_cons(prod_soup):
	pros = []
	cons = []
	
	revs = prod_soup.find_all('div', attrs={"class":"ui-grid-solo"})
	for rev in revs:
		rev1 = rev.find('div', attrs={"class":"ui-block-a"})
		if rev1:
			p = rev1.find('p')
			if p:
				pc = p.find('strong').string
				
				try:
					content = p.contents[1]
				
					#print "Content : ", unicode(content), type(content)
				
					if pc[0] =='P':
						pros = pros + [unicode(content).encode('ascii','ignore')]
					elif pc[0]=='C':
						cons = cons + [unicode(content).encode('ascii','ignore')]
				except IndexError:
					print "no pros/cons"
				
	return (pros, cons)
	
"""prod_page = urllib.urlopen("http://epinions.com/product/Hewlett_Packard_PW460T_Digital_Camera/101468172")
prod_soup = BeautifulSoup(prod_page, "lxml")
print pros_cons(prod_soup)"""
			
# Crawl web page of each category
li = root_soup.find_all('li', attrs={"data-theme":"d"})

for l in li:
	if l.find('a'):
		
		category = l.find('a').string
		
		#check if it is already crawled
		if os.path.isfile(category+'_pros.txt') and os.path.isfile(category+'_cons.txt'):
			continue
				
		link = l.find('a').get('href')
		
		print category + "\t" + link
		
		cat = urllib.urlopen(root_url + link)
		cat_soup = BeautifulSoup(cat, "lxml")
		
		prod_dict = list_products(cat_soup)
		
		fp=open(category+'_pros.txt', 'a')
		fc=open(category+'_cons.txt', 'a')
		
		for prod_name in prod_dict:
		
			fmeta = open(category+'_meta.txt', 'a+')
		
			prod_lst = fmeta.readlines()
			
			if prod_name in prod_lst:
				continue
			
			prod_url = prod_dict[prod_name]
			
			prod_page = urllib.urlopen(root_url + prod_url)
			prod_soup = BeautifulSoup(prod_page, "lxml")
			
			print 'connecting to.. product ' + prod_url

			#pros and cons of each product
			(pros, cons) = pros_cons(prod_soup) 
			fp.write('<name>'+prod_name.encode('utf-8')+'</name>\n')
			fc.write('<name>'+prod_name.encode('utf-8')+'</name>\n')
			
			for item in pros:
				fp.write('<pros>'+item.encode('utf-8')+'</pros>\n')
				
			for item in cons:
				fc.write('<cons>'+item.encode('utf-8')+'</cons>\n')
			
			fmeta.write(prod_name.encode('utf-8') + '\n')
					
			fmeta.close()
			
		fp.close()
		fc.close()
		
		print "Category : " + category + " done."
