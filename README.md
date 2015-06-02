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

<table>
  <tr>
    <td>Case ID</td>
    <td>Requester Login</td>
    <td>Description</td>
    <td>Impact</td>
    <td>Create Date</td>
    <td>Last Modified Date</td>
    <td>Status</td>
    <td>Resolved Date</td>
  </tr>
</table>

######4. Create two Grasshopper job

######5. Copy job ids to TTrun.sh
