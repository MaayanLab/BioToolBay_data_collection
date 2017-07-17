import pandas as pd
import urllib2

all_articles_tools = pd.read_table('ALL_DATA/BMC/TOOLS/bmc_tools_00_17.txt', keep_default_na=False)
# Add new column to a dataframe for result of checking
all_articles_tools["active"]="NULL"


i=0
for i in range(len(all_articles_tools)):
    link=all_articles_tools["homepage"][i]
    try:
        r = urllib2.urlopen(link)
        if r.getcode() in (200, 401):
            print(i)
            print("works")
            all_articles_tools["active"][i]="TRUE"
        else:
            print("NOT")
    except:
        pass
    i=i+1



all_articles_tools=all_articles_tools[all_articles_tools.active != "NULL"]
all_articles_tools.to_csv("bmc_active_links_00_17.txt",sep='\t', encoding='utf-8')