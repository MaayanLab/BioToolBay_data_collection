import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re
import string
from string import digits #library for regular expression helpers


#read in BMC data
journal_data=pd.read_table('ALL_DATA/BMC/TXT/bmc_00_17.txt', keep_default_na=False)

#Connect all journals together:


#Add additional columns for extracted info:
journal_data['name_tool']="NULL"
journal_data['homepage']="NULL"
journal_data['info']="NULL"



#Regular Expression
#Matches the words before the colon and search for it in links. If found sets it as a link to a tool
#Regular Expression
#Matches the words before the colon and search for it in links. If found sets it as a link to a tool
find_name = re.compile(r"^[^:]+\s*")#  a word before colon
letters_mix=re.compile('.*[A-Z].*[A-Z].*')# a word with more than one capital letter
paranthesis =re.compile('\(|\)')
comma=re.compile(',')
additional_info=re.compile('web-server|simulation|software|database|R package|repository|app|toolbox|algorithm|platform')
data_length=len(journal_data)
success=False
for i in range (data_length):
    title_search=journal_data['title'][i]
    print (title_search)
    print(journal_data['all_links'][i])
    old_links=[]
    old_links=journal_data['all_links'][i].split(',')
    # A word before colon in the title of the article
    if re.search(':', title_search):
        tool_name=re.search(find_name, title_search).group(0)
        print("Colon before ", tool_name)
        tool_name_parts=[]
        tool_name_parts=tool_name.split('-')
        tool_links=[]
        for name_part in tool_name_parts:
            print(name_part)
            translator=str.maketrans('','',string.punctuation)
            name_part2=name_part.translate(translator)
            remove_digits = str.maketrans('', '', digits)
            name_part2d= name_part2.translate(remove_digits)
            for link in old_links:
                try:
                    if re.search(name_part2, link,re.IGNORECASE):
                        #add bew column with data being the link to tool but now confirmed-homepage
                        if len(tool_name)<50:#long description and then colon- not a tool
                            if tool_name.endswith(':'):
                                tool_name=tool_name[:-1]
                            journal_data['name_tool'][i]=tool_name
                            tool_links.append(link)
                            success=True
                        else:
                            pass
                    if success==False:
                        if re.search(name_part2d, link,re.IGNORECASE):
                            #add bew column with data being the link to tool but now confirmed-homepage
                            if len(tool_name)<50:#long description and then colon- not a tool
                                if tool_name.endswith(':'):
                                    tool_name=tool_name[:-1]
                                journal_data['name_tool'][i]=tool_name
                                tool_links.append(link)
                                success=True
                            else:
                                pass
                except:
                    pass
        if re.search(additional_info, title_search):
            journal_data['info'][i]=re.search(additional_info, title_search).group(0)
        if len(tool_links)>0:
            if success== True:
                journal_data['homepage'][i]=tool_links[0]
                journal_data['link_to_tools']=','.join(tool_links)
                tool_name1=journal_data['name_tool'][i]
                tool_name2=re.sub(paranthesis, "",tool_name1)
                tool_name2=re.sub(comma, "",tool_name2)
                journal_data['name_tool'][i]=tool_name2     
    # A word than has more than one capital letter in the title
    if success==False: #second attempt: capital/small letter regex
        tem_title=[]
        tool_links=[]
        tem_title=title_search.split()
        for word in tem_title:
            if success==False:#do not overwrite first good match
                if re.search(letters_mix, word):
                    tool_name=re.search(letters_mix, word).group(0)
                    print("Name with mix letters: ", tool_name)
                    tool_name_parts=[]
                    tool_name_parts=tool_name.split('-')
                    for name_part in tool_name_parts:
                        print(name_part)
                        translator=str.maketrans('','',string.punctuation)
                        name_part2=name_part.translate(translator)
                        remove_digits = str.maketrans('', '', digits)
                        name_part2d= name_part2.translate(remove_digits)
                        if re.search('RNA|DNA|HIV|seq|ATP|CHIP|protein', name_part2, re.IGNORECASE):
                            pass
                        else:
                            if len(name_part2)<3:# 2 letters- not enough info to match name( avoid false positive)
                                pass
                            else:
                                for link in old_links:
                                    try:#exception from regex
                                        if re.search(name_part2, link,re.IGNORECASE):
                                            if tool_name.endswith(':'):
                                                tool_name=tool_name[:-1]
                                            journal_data['name_tool'][i]=tool_name
                                            tool_links.append(link)
                                            success=True
                                        if success==False:
                                            if re.search(name_part2d, link,re.IGNORECASE):
                                        #add new column with data being the link to tool but now confirmed-homepage
                                                if tool_name.endswith(':'):
                                                    tool_name=tool_name[:-1]
                                                journal_data['name_tool'][i]=tool_name
                                                tool_links.append(link)
                                            else:
                                                pass
                                    except:
                                        pass
            else:
                pass                              
        if re.search(additional_info, title_search):
            journal_data['info'][i]=re.search(additional_info, title_search).group(0)
        tool_links_set=set(tool_links)
        if len(tool_links)>0:
            if success==True:
                journal_data['homepage'][i]=tool_links[0]
                journal_data['link_to_tools']=','.join(tool_links)
                tool_name1=journal_data['name_tool'][i]
                tool_name2=re.sub(paranthesis, "",tool_name1)
                tool_name2=re.sub(comma, "",tool_name2)
                journal_data['name_tool'][i]=tool_name2                    
    success=False

# Blacklist the tags that are not needed:
tag_blacklist=['CORRIGENDUM', 'MESSAGE FROM THE ISCB ', 'EDITORIAL','AUTHOR INDEX', 'RECOMB-SEQ/RECOMB-CBB 2016', 'ERRATUM', 'RECOMB-CG 2016', 'ECCB 2016 ORGANIZATION',
                   'ERRATA', 'ECCB 2016: THE 15TH EUROPEAN CONFERENCE ON COMPUTATIONAL BIOLOGY', 'ECCB 2014 ORGANISATION', 'MESSAGE FROM ISCB', 'LETTER TO THE EDITOR',
                   'ISMB 2016 PROCEEDINGS JULY 8 TO JULY 12, 2016, ORLANDO, FLORIDA', 'REVIEW' # tags for BIOINFORMATICS
#TAGS for NAR
                'ERRATUM', 'EDITORIAL', 'EXPRESSION OF CONCERN', 'RETRACTION', 'CORRIGENDA', 'SURVEY AND SUMMARIES', 'EDITORIAL EXPRESSION OF CONCERN', 'EDITORIAL: NAR AWARDS 2013 ',
                'NAR AWARDS 2014','EDITORIAL: NAR SURVEYS THE PAST, PRESENT AND FUTURE OF RESTRICTION ENDONUCLEASES', 'NULL', 'ANNOUNCEMENT', 'OBITUARY',
#TAGS FOR BIOI more
                'RECOMB-SEQ/RECOMB-CBB 2016', 'RECOMB-CG 2016', 'ISMB/ECCB 2013 PROCEEDINGS PAPERS COMMITTEE','ECCB 2016: THE 15TH EUROPEAN CONFERENCE ON COMPUTATIONAL BIOLOGY', 'ECCB 2016 ORGANIZATION',
                'ISMB 2014 PROCEEDINGS PAPERS COMMITTEE','ISMB 2016 PROCEEDINGS JULY 8 TO JULY 12, 2016, ORLANDO, FLORIDA','ECCB 2014 ORGANISATION',
#Tags for DATABASE
                'FRONT MATTER/BACK MATTER', 'DATABASE UPDATES ']



# Drop the data with the blacklist tags
journal_data = pd.DataFrame([rowData for index, rowData in journal_data.iterrows() if rowData['tag'] not in tag_blacklist])

Tool_ready=DataFrame()
Tool_ready=journal_data[journal_data.name_tool != "NULL"]
Tool_ready2=Tool_ready[Tool_ready.homepage != "NULL"]



Tool_ready2.to_csv("bmc_tools_00_17.txt",sep='\t', encoding='utf-8')
