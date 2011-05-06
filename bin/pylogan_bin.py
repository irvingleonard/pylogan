#!/usr/bin/python
# -*- coding: utf-8 -*-

import pylogext.input
import pylogext.process
import pylogext.output

#Need of a configuration file, this variables should be stored there
syslog_path='syslog'
out_path='webroot/'

page_title='Utilización del Proxy Squid'
page_users_block_title='Tráfico por Usuarios'
page_domains_block_title='Tráfico por Dominios'
page_navigations_block_title='Tráfico por Navegaciones'
page_traffic_heading='Tráfico'
page_user_heading='Usuario'
page_domain_heading='Dominio'
page_navigation_heading='Navegación'

test_log=pylogext.input.Syslog()
#test_log.dbg=True
test_log.SourceFile(syslog_path)
test_log.PopulateLines()
squid=pylogext.process.Squid()
squid.UseSyslog(test_log)
print squid.Consumption()
  #if resu:
    ##print resu
    #pass



#The first step is to read the file (just syslog fromat at the moment).
#There is just one implemented process, and is for squid because I could'nt find a log analyzer for squid capable of use syslog (there is modlogan but is cryptic and discontinued)
#input_log=pylogan.input.Squid()
#input_log.SourceFile(syslog_path)
#lines=input_log.Lines()

#Fill the 'holes' in the timelines
#users=pylogan.process.GetUsers(lines)
#for user in users.keys():
  #users[user]=pylogan.process.CompleteData(users[user])
#users=pylogan.process.SumSizes(users)
#users=pylogan.process.SanitizeSizes(users)
#users.insert(0,(page_user_heading,page_traffic_heading))

#domains=pylogan.process.TopDomains(lines)
#for domain in domains.keys():
  #domains[domain]=pylogan.process.CompleteData(domains[domain])
#domains=pylogan.process.SumSizes(domains)
#domains=pylogan.process.SanitizeSizes(domains)
#domains.insert(0,(page_domain_heading,page_traffic_heading))

#navigations=pylogan.process.TopNavigations(lines)
#for navigation in navigations.keys():
  #navigations[navigation]=pylogan.process.CompleteData(navigations[navigation])
#navigations=pylogan.process.SumSizes(navigations)
#navigations=pylogan.process.SanitizeSizes(navigations)
#navigations.insert(0,(page_navigation_heading,page_traffic_heading))

#Build graphs
#users_graph=pylogan.output.RRDTool('users',out_path)
#users_graph.GraphTimelines(users,True)
#domains_graph=pylogan.output.RRDTool('domains',out_path)
#domains_graph.GraphTimelines(pylogan.process.EscapeNames(domains),True)
#navigations_graph=pylogan.output.RRDTool('navigations',out_path)
#navigations_graph.GraphTimelines(pylogan.process.EscapeNames(navigations),True)

##Build the XHTML page
#page=pylogan.output.XHTML(out_path)
#page.SetTitle(page_title)
#page.CreateBlock('users',page_users_block_title)
##page.IncludeImage('users',users_graph.graphfile)
#page.IncludeTable('users',users)
#page.CreateBlock('domains',page_domains_block_title)
###page.IncludeImage('domains',domains_graph.graphfile)
#page.IncludeTable('domains',domains)
#page.CreateBlock('navigations',page_navigations_block_title)
###page.IncludeImage('navigations',navigations_graph.graphfile)
#page.IncludeTable('navigations',navigations)
#page.BuildContent()
#page.WriteFile()

#End
