That's a basic word2vec cluster demo. You can run it with :
* step1:
`pip install -r requirements.txt`

* step2:
`python cluster.py w2vecluster --data data/alert_srv_cmd.csv --o output/srv_cmd_5.csv --k 5`

Now, you would see the result of predict. Have fun.

In my sence, i count the cmdline from alert datastets then cluster it. 

```sql
select srv_cmd, count(*) srv_cmd_cnt
from xxxxxxxx.xxxx_alert_log_xxxxx
where ds = max_pt("eleme_auditlog.eleme_alert_log")
group by srv_cmd
order by srv_cmd_cnt desc
limit 10000;
```
so that i can find the problem from millions alerts. Actually, it was useful.(also still have some problem)


![image](https://user-images.githubusercontent.com/12653147/59007370-b6fc5300-8858-11e9-83c7-6f6454cba5a8.png)
![image](https://user-images.githubusercontent.com/12653147/59007395-ca0f2300-8858-11e9-996e-6db84f0a9b43.png)

