# Trouble Tickets
Get and insert TTs with tags for AWS dev support bjs_ops_dashboard

### Config step
######1. vi ~/.login
```shell
export USERNAME=xxx    
export PASSWORD=xxx
```

######2. crontab -e
```shell
 1 10 * * * ~/tt/TTrun.sh
```

######3. Modify TT search result column:  
[https://tt.amazon.com/search?search=search!&tags=aws-dev-support-cn](https://tt.amazon.com/search?search=search!&tags=aws-dev-support-cn)  
Case ID, Requester Login, Description, Impact, Create Date, Last Modified Date, Status, Resolved Date

######4. Create Grasshopper job
