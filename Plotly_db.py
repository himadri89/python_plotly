import plotly
import plotly.graph_objs as go 
import pandas as pd
import datetime as dt
from datetime import datetime
import os
from base64 import b64encode as ben


os.chdir("Local Directory")
input_df = pd.read_csv('results.csv', sep =",")
logo_left = "logo.png"
logo_right = "logo.png"
logo_watermark = "watermark.png"


ask = input_df['file_server_timestamp'].str.split(' ', expand=True)
ask.columns =['date', 'file_arrival_timestamp']
input_df = input_df.drop('file_server_timestamp', 1)
dft = input_df.join(ask, lsuffix='_df1', rsuffix='_ask')
df = dft[['register_id', 'file_arrival_timestamp', 'date','feed_name']]
df = df.sort_values('file_arrival_timestamp')

df_date1 = df.sort_values('date')
df_date = df_date1['date'].tolist()
df_benchmark = pd.read_csv('comparitive_analysis_benchmark.csv', sep =",")


data1 = []
reg_uni = df['register_id'].unique()
r = df_benchmark['feed_name'].unique().tolist()
#r = df_benchmark['feed_name'].loc[df_benchmark.register_id.isin(reg_id)].dropna().unique().tolist()
#r= reg_id


def to_seconds(date_list):
    seconds_1=[]
    for n in range(len(date_list)):
        seconds = int(date_list[n].hour *3600 +date_list[n].minute*60 + date_list[n].second)
        seconds_1.append(seconds)
    return seconds_1


def time_str_2_timeobj(timef):
    tmobj = []
    for i in range(len(timef)):
        ap = datetime.strptime(timef[i], '%H:%M:%S').time()
        tmobj.append(ap)
    return tmobj


def time_str_3_timeobj(timef):
    tmobj = []
    for i in range(len(timef)):
        ap = datetime.strptime(timef[i], '%H:%M').time()
        tmobj.append(ap)
    return tmobj
    

def add_truefalse(i):
    tflist =[]
    for j in range(len(r)):
        tflist.append(False)
    ss=[]
    for idx in range(len(tflist)):
        tflist[idx]= True
        ss.append(tflist)
        tflist =[]
        for j in range(len(r)):
            tflist.append(False)
    return ss[i-1]


draft=[]
def ret_arg_button(j):
    for i in r:
       f= dict(label = i,method = 'update',args = [{'visible':add_truefalse(r.index(i)+1)}])
       draft.append(f)
    return draft [j] 


def get_c_max(dt1):
    dm=[]
    for i in range(len(dt1)):
        ty = dt1[i] + 90 * 60
        dm.append(ty)
    return dm


def concatenate_list_date(list):
    result_date= []
    for element in list:
        a = str('Date: ') + str(element)
        result_date.append(a)
    return result_date


def concatenate_list_time(list):
    result_time= []
    for element in list:
        a = str('Time: ') + str(element)
        result_time.append(a)
    return result_time


def convert_tuple_to_string(tup):
    return [str(x) for x in tup]


def col_generation(df_new,df_benchmark_1,mid_pt):
    cols =[]    
    mid_pt
    dt1=to_seconds(pd.to_datetime(df_benchmark_1['TIME_BUCKET_30min'], format='%H:%M:%S').dt.time.tolist())
    dt2= get_c_max(dt1)
    sorted_data_time = []
    sorted_data_time= to_seconds(pd.to_datetime(df_new['file_arrival_timestamp'], format='%H:%M:%S').dt.time.tolist())
    cat_time_date_str=[]
    alert=[]
    for i in range(len(df_new)):
        if ((sorted_data_time[i]  > dt1[0] and sorted_data_time[i] < dt2[0]) or (sorted_data_time[i] < dt1[0])):
            cols.append(mid_pt)
            text_d = df_new['date']
            d = concatenate_list_date(text_d)
            text_t = df_new['file_arrival_timestamp']
            t = concatenate_list_time(text_t)
            alert.append(str('Alert: No Alert'))
        elif ( sorted_data_time[i] > dt2[0]):
           cols.append((len(df_new['file_arrival_timestamp'])-1))
           text_d = df_new['date']
           d = concatenate_list_date(text_d)
           text_t = df_new['file_arrival_timestamp']
           t = concatenate_list_time(text_t)
           alert.append(str('Alert: Raised'))
           

    zipped = zip(d, t,alert)
    cat_time_date_tuple = list(zipped)
    cat_time_date_str = convert_tuple_to_string(cat_time_date_tuple)
    cols.append(0)
    cols.append(mid_pt*2)
    print(cols)
    return cols,cat_time_date_str


def img_to64bit(img):
    with open(img, "rb") as image_file:
        encoded_string = ben(image_file.read())  
    img_str = str(encoded_string)
    fixed = img_str[2:]
    lgth = len(fixed)-1
    fixed1 =fixed[:lgth]
    dcd_data = str("data:image/png;base64, ") + fixed1
    return dcd_data


for i in  r:   
    df_new = df.loc[df['feed_name']==i]
    datef = df_new['date'].tolist()
    timef =df_new['file_arrival_timestamp'].tolist()
    timesss = time_str_2_timeobj (timef)
    timefs = to_seconds(timesss)
    df_benchmark_1 = df_benchmark.loc[df_benchmark['feed_name']==i]
    mid_pt = ((len(df_new['file_arrival_timestamp'])-1)/2)
    
   

    if(df_benchmark_1.empty):
        continue;
    else:
        col, txt = col_generation(df_new,df_benchmark_1,mid_pt)
        scattter_data= go.Scatter(
                x=datef,
                y= timefs,
                mode = 'markers',
                marker = dict(
                    size = 10,           
                    color = col,
                    colorbar=dict(title='Benchmark Gradient'),
                    colorscale = 'Rainbow',
                    showscale = False,
                    line = dict(
                                width = 2,
                               )
                             ),
                text= txt,
                hoverinfo = 'text',
                name='',
                )
        data1.append(scattter_data)
        
data2=[]
for i in  r: 
    df_new = df.loc[df['feed_name']==i]
    datef = df_new['date'].tolist()
    df_benchmark_1 = df_benchmark.loc[df_benchmark['feed_name']==i]
    
    line1 = to_seconds(pd.to_datetime(df_benchmark_1['TIME_BUCKET_30min'], format='%H:%M:%S').dt.time.tolist())
    line_min = line1[0]
    line0 = [line_min for i in range(len(df_date))]
    
    if(df_benchmark_1.empty):
        continue;
    else:
        scattter_data_line= go.Scatter(
                x= df_date,
                y= line0,
                mode = 'lines',
                line = dict(color='#b9ffa5',  width=1),
                fill='tonexty',
                text = 'Anticipated Arrival Lower Bound',
                hoverinfo = 'text',
                opacity = 0.0,
                name='',
                )
        data2.append(scattter_data_line)  
        
data3=[]
for i in  r: 
    df_new = df.loc[df['feed_name']==i]
    datef = df_new['date'].tolist()
    df_benchmark_1 = df_benchmark.loc[df_benchmark['feed_name']==i]
    
    line2 = to_seconds(pd.to_datetime(df_benchmark_1['TIME_BUCKET_30min'], format='%H:%M:%S').dt.time.tolist())
    line_max = get_c_max(line2)[0]
    line1 = [line_max for i in range(len(df_date))]
    
    if(df_benchmark_1.empty):
        continue;
    else:
        scattter_data_line2= go.Scatter(
                x= df_date,
                y= line1,
                mode = 'lines',
                line = dict(color='#b9ffa5',  width=1),
                fill='tonexty',
                text = 'Anticipated Arrival Upper Bound',
                hoverinfo = 'text',
                opacity = 0.0,
                name='',
                )
        data3.append(scattter_data_line2)
        
        
        
        
updatemenus = list([
dict(
     active=0,
     buttons=list([ 
        dict(label = 'None',
             method = 'restyle',
             args = [{'visible':[False]}]
             )
    ]),
        direction = 'down',
        pad = {'r': 10, 't': 10, 'l': 146},
        showactive = True,
        x = 0.06,
        xanchor = 'left',
        y = 1.14,
        yanchor = 'top',
        bgcolor = '#FCFCFF',
        borderwidth = 2,
        bordercolor = '#131314'
)
])  

for ind in range(len(r)):            
    updatemenus[0]['buttons'].append(ret_arg_button(ind))
        

# =============================================================================
# Range for x axis       
# =============================================================================
def range_for_x():
    rangex=[]
    dfs = df.sort_values('date')
    ddate= dfs['date'].tolist()
    rangex.append(ddate[0])
    rangex.append(ddate[len(ddate)-1])
    return rangex
# =============================================================================
# Range for y axis: To be used with the layout
# =============================================================================
def range_for_y():
    z =['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    zz = time_str_3_timeobj(z)
    tv = to_seconds(zz)
    tx =['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    ran_e =[tv,tx]
    return ran_e
# =============================================================================
        
layout = go.Layout(
        images=[dict(
                    source= img_to64bit(logo_left),
                    xref="paper", yref="paper",
                    x=0.001, y=1.02,
                    sizex=0.15, sizey=0.15,
                    xanchor="left", yanchor="bottom",
                    opacity = 0.8
                    ),
                dict(
                    source= img_to64bit(logo_right),
                    xref="paper", yref="paper",
                    x=0.9, y=1.02,
                    sizex=0.15, sizey=0.15,
                    xanchor="left", yanchor="bottom",
                    opacity = 0.8
                    ),
                dict(
                    source = img_to64bit(logo_watermark),
                    xref="paper", yref="paper",
                    x=0.25, y=0.45,
                    sizex=0.5, sizey=0.5,
                    xanchor="left", yanchor="bottom",
                    opacity = 0.11
                    )],
                        
        #height=800, width=700,
        #margin=Margin(r=20, l=300, b=75, t=125),
        title='Feed Benchmark Tracking <br> Last 90 Day Records', 
        autosize= True,
        showlegend=False,
        xaxis=dict(title='Date',
                   autorange = False, 
                   range = range_for_x(), 
                   autotick=False,
                   ticks='outside',
                   tickcolor='#000',
                   tickformat ="%Y-%m-%d",
                   tickangle=45,
                   showgrid=True,
                   zeroline=True,
                   showline=True,
                   zerolinewidth=3, 
                   linewidth=2, 
                   tickwidth=1,
                   tickmode='auto',
                   nticks=50,
                   mirror = False),
                   
        yaxis=dict(title = 'Time of Arrival', 
                   rangemode ='tozero',
                   tickmode = 'array',
                   tickvals =range_for_y()[0],
                   ticktext =range_for_y()[1],
                   tickformat ="%H:%M",
                   autotick=True, 
                   showgrid=True, 
                   zeroline=True, 
                   showline=True,
                   zerolinewidth=3, 
                   linewidth=2, 
                   tickwidth=1,
                   mirror = False),
        
        hovermode= 'closest',
        paper_bgcolor='#fcfdff',
        updatemenus=updatemenus
        )


annotations = [dict(text='Feed Name:', x=0.11, y=1.11, xref='paper', yref='paper', align='left', showarrow=False)]
layout['annotations']= annotations
config={'showLink': False, 
        'scrollZoom': True, 
        'displayModeBar': 'hover', 
        'displaylogo': False, 
        'modeBarButtonsToRemove': ['toImage', 'sendDataToCloud', 'zoom2d', 'pan2d', 'lasso2d', 'hoverCompareCartesian', 'hoverClosestCartesian']}

dataz = data1
dataz.extend(data2)
dataz.extend(data3)

fig = dict(data=dataz, layout=layout)
plotly.offline.plot(fig,config=config, filename='benchmark_analysis.html')