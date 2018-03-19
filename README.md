# plotly_dashboard
Plotly dashboard

Without explaining the business ideas behind this which I prepared for a company. I am writing a bit about the work done here. This basically plots the time on 
y axis against date against x axis. The dash board changes from the menu button which has the feed_id, by which the charts are filtered.

I had created a sample file for this. The data had register_id, feed_name and date_timestamp columns. The original data had like around 65000 rows, but I had 
prepared a small dataset based on the columns I need to work with.

Some key points:
i) I was facing some issues on y axis labels as all the timestamp was not shown. Only those available corresponding to the datapoints are shown. So I made a list 
of timestamp from 1:00:00 to 23:00:00 and converted them to seconds using to_seconds method and I plotted the corresponding seconds on y axis from the method 
range_for_y. So now to display the text on y axis as timestamp instead of the converted seconds I have used the attribute ticktext which goes with the tickvals 
in which the seconds list is stored.

ii) The images have to be encoded into base64 before it can be used.

iii) Two files were used . One containing the raw data. And the other containing the benchmark timestamp for every register_id.

Attached two files:
i) results.csv: main file
ii) comparitive_analysis_benchmark.csv: the calculated benchmark file