
import os.path
import collections
import xml.dom.minidom

import pylogan.output
import pylogan.output.utils

class SquidResume:
	"""Class for the squid HTTP proxy traffic reports
	
	Its a container for squid related reports.
	"""
	
	def __init__(self, output_path = None):
		# TODO: Implement theming
		self.theme_path = os.path.abspath(os.path.join(pylogan.output.__path__[0], "themes", "simple.xhtml"))
		css_path = os.path.abspath(os.path.join(pylogan.output.__path__[0], "themes", "pylogan.css"))
		css = open(css_path)
		self.css = css.read()
		css.close()
		
		if not output_path:
			output_path = '.'
		self.output_path = os.path.abspath(os.path.join(output_path, "index.xhtml"))
	
	def out(self, dates, users, domains, navigations):
		"""The first report to be made
		
		Reports top ten users, domains and navigations.
		"""
		
		# TODO: use tuples and lists, the sorting is a processing element
		users = collections.OrderedDict(sorted(users.items(), key=lambda t: t[1], reverse = True))
		domains = collections.OrderedDict(sorted(domains.items(), key=lambda t: t[1], reverse = True))
		
		dates = list(dates)
		
		# TODO: use a validating DOM implementation, use getElementById or XPath; XSLT or XQuery implementation is even better
		the_dom = xml.dom.minidom.parse(self.theme_path)
		
		# TODO: the theming thing
		the_dom.documentElement.firstChild.getElementsByTagName('style').item(0).appendChild(the_dom.createTextNode(self.css))
		
		# The ugly DOM work (minidom is really mini)
		h2s = the_dom.documentElement.lastChild.getElementsByTagName('h2')
		for i in range(h2s.length):
			if h2s.item(i).getAttribute('id') == 'time_span':
				try:
					date_difference = dates[1] - dates[0]
					if date_difference.days == 0:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%I:%M%p') + " - " + dates[1].strftime('%I:%M%p') + ")"))
					elif date_difference.days < 28:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%d %I:%M%p') + " - " + dates[1].strftime('%d %I:%M%p') + ")"))
					elif date_difference.days < 365:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%m/%d %I:%M%p') + " - " + dates[1].strftime('%m/%d %I:%M%p') + ")"))
					else:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%Y/%m/%d %I:%M%p') + " - " + dates[1].strftime('%Y/%m/%d %I:%M%p') + ")"))
				except AttributeError:
					pass
				except TypeError:
					pass
		
		divs = the_dom.documentElement.lastChild.getElementsByTagName('div')
		for i in range(divs.length):
			if divs.item(i).getAttribute('id') == 'users':
				for user in list(users.keys())[:10]:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(user))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','size')
					value.appendChild(the_dom.createTextNode(pylogan.output.utils.readeable_size(users[user])))
					
			elif divs.item(i).getAttribute('id') == 'domains':
				for domain in list(domains.keys())[:10]:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(domain))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','size')
					value.appendChild(the_dom.createTextNode(pylogan.output.utils.readeable_size(domains[domain])))
			elif divs.item(i).getAttribute('id') == 'navigations':
				for navigation in navigations[:10]:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					for data in navigation:
						element = the_dom.createElement('td')
						row.appendChild(element)
						element.appendChild(the_dom.createTextNode(str(data)))
					element.replaceChild(the_dom.createTextNode(pylogan.output.utils.readeable_size(navigation[-1])), element.firstChild)
					element.setAttribute('class', 'size')
		
		#File output
		index = open(self.output_path, mode = 'w', encoding = 'utf-8')
		the_dom.writexml(index)
		index.close()
