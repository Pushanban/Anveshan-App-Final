import tkinter as tk
import requests
from datetime import date, timedelta


def response_dec(active, recovered, deaths):
    try:
        desc = "Following is Covid Data Till Today:"
        finCountry = active[-1]['Country']
        confirmedCases = active[-1]['Cases']
        recoveredCases = recovered[-1]['Cases']
        diedCases = deaths[-1]['Cases']
        activeCases = confirmedCases - recoveredCases

        final_str = 'Country: %s \n %s \nConfirmed %s \nActive: %s \nRecovered: %s \nDeaths: %s' % (
            finCountry, desc, confirmedCases, activeCases, recoveredCases, diedCases)
    except:
        final_str = 'There was a problem retrieving that information'

    return final_str


def CovData_final(country):
    temptime = "T00:00:00Z"
    today = date.today()
    yester = today - timedelta(days=1)
    yesterStr = yester.strftime('%y-%m-%d')
    dateStr = yesterStr + temptime
    tdyStr = today.strftime('%y-%m-%d') + temptime

    finalDateStr = "20" + dateStr + '&to=' + "20" + tdyStr

    apiSub = "https://api.covid19api.com/total/country/"
    apiSubCases = "/status/confirmed?from="
    apiSubRecov = "/status/recovered?from="
    apiSubDeaths = "/status/deaths?from="

    casesUrl = apiSub + str(country) + apiSubCases + finalDateStr
    recovUrl = apiSub + str(country) + apiSubRecov + finalDateStr
    deathsUrl = apiSub + str(country) + apiSubDeaths + finalDateStr

    headers = {}
    payload = {}

    activeRes = requests.request(
        "GET", casesUrl, headers=headers, data=payload)
    active = activeRes.json()

    recovRes = requests.request("GET", recovUrl, headers=headers, data=payload)
    recovered = recovRes.json()

    deathRes = requests.request(
        "GET", deathsUrl, headers=headers, data=payload)
    deaths = deathRes.json()

    lbl['text'] = response_dec(active, recovered, deaths)


body = tk.Tk()
body.title('Covidata')

canvas = tk.Canvas(body, height=500, width=600)
canvas.pack()

bg_img = tk.PhotoImage(file="bg.png")
bg_lbl = tk.Label(body, image=bg_img)
bg_lbl.place(relwidth=1, relheight=1)

frame = tk.Frame(body, bg='#090979', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Status", font=40,
                   command=lambda: CovData_final(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lwr_frame = tk.Frame(body, bg='#090979', bd=10)
lwr_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

lbl = tk.Label(lwr_frame)
lbl.place(relwidth=1, relheight=1)

body.mainloop()
