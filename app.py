import re
from googleapiclient.discovery import build
from datetime import timedelta
from flask import Flask, request, render_template, redirect
app = Flask(__name__)

#Enter your YouTube API key in developerKey='' and run the code

@app.route('/', methods=['GET','POST'])
def pl_length():
    to_print = ""
    if request.method == 'POST':
    
        youtube = build('youtube', 'v3', developerKey='')
    
        link = request.form['link']

        link_pattern = re.compile("list=[a-zA-Z0-9_-]*")

        link_checking = link_pattern.findall(link)

        if link_checking == []:
            to_print += "Sorry! This video does not belong to a playlist!!"
            # return redirect("/")
            return render_template('index.html',to_print=to_print)
    
        playlistId = str(link_checking[0][5:]) 


        hours_pattern = re.compile("\d*H")
        minutes_pattern = re.compile("\d*M")
        seconds_pattern = re.compile("\d*S")


        total_time = 0

        nextPageToken = None
        while True:
            pl_request = youtube.playlistItems().list(

                part='contentDetails',
                playlistId=playlistId,
                maxResults=50,
                pageToken=nextPageToken
            )

            vid_ids = []
            response = pl_request.execute()
            for item in response['items']:
                vid_ids.append(item['contentDetails']['videoId'])

            vid_ids = ','.join(vid_ids)

            #print(vid_ids)

            vid_request = youtube.videos().list(
                    part="ContentDetails",
                    id=vid_ids

            )

            vid_response = vid_request.execute()


            for item in vid_response['items']:

                duration = item['contentDetails']['duration']
                #print(duration)
                
                hours = hours_pattern.findall(duration)
                minutes = minutes_pattern.findall(duration)
                seconds = seconds_pattern.findall(duration)

                if (hours != []):
                    hours = int(hours[0][:-1])
                else:
                    hours = 0

                if (minutes != []):
                    minutes = int(minutes[0][:-1])
                else:
                    minutes = 0

                if (seconds != []):
                    seconds = int(seconds[0][:-1])
                else:
                    seconds = 0

                
                video_seconds = timedelta(
                        hours = hours,
                        minutes = minutes,
                        seconds = seconds
                ).total_seconds()

                total_time += video_seconds
            
            nextPageToken = response.get('nextPageToken')

            if nextPageToken == None:
                break
            

        #print(total_time)
        # A colon is added at the end only so that I can run 
        # the regular expression final_pattern can be matched
        # Only for convenience
        final_time = str(timedelta(seconds=total_time)) + ":"

        #print(final_time, "\n")


        final_pattern_days = re.compile("\d+ day[s]?")
        final_pattern = re.compile("(\d*:)")

        final_time_days = final_pattern_days.findall(final_time)
        final_time = final_pattern.findall(final_time)

        #print(final_time_days, "\n")

        li = ['hour', 'minute', 'second']


        

        if not final_time_days == []:
            to_print += final_time_days[0] + " "
            #print(final_time_days[0], end=" ")

        
        for ind, time in enumerate(final_time):
            if int(time[:-1]) != 0:
                to_print += time[:-1] + " " + li[ind]
                if int(time[:-1]) != 1:
                    to_print += "s "
                else:
                    to_print += " "
                #print(time[:-1] + " " + li[ind], end=" ")
            else:
                continue
        
        #return redirect("/")
        #return render_template('index.html', to_print=to_print)
    
    return render_template('index.html',to_print=to_print)
if __name__=="__main__":
    app.run(debug=True)