 **Task description**
- Find a dataset with weather archive for previuos 10 years
- Parse it
- Design web application which can retrieve weather data and show statistic for desirable period
- Statistic summary should include:
  - Average temperature for the entire period
  - Average temperature for each year
  - Amount of days with/without precipitations and their type
  - Wind speed and directions (deprecated)
  
I wasn't able to find appropriate dataset for this task. Ones of them were without datatypes,
which were necessary for this task.
 The others didn't include desirable range of locations with data presented only in one specific country.

So I decided to use this web service with dedicated api for quering weather archive data:
https://www.ncdc.noaa.gov/cdo-web/webservices/v2

**Encountered issues**

The main trouble I've encoutered was dealing with API. Some issues are described below.

*The main API cons:*


- API has a restriction on amount of requests per second(5 requests per second).
Eventually this affects amount of years for which we could get statistic data.
- API has restriction on time range for daily params. We can retrieve only data for one year per requests.
This complicates program logic too (the main focus of my task was on processing daily data samples and calculate average params)
- For most locations presented only a few datatypes,
  and sometimes it's tricky to understand which ones are available for  a  particular location. \cf3 For example (it's typical) after using specified params to denote the required parameters
  
  - For example, I use this parameter in GET request to get a list of all stations which provide datatypes:
  "datatypeid": ["TAVG", "SNWD", "PRCP"]
  "startdate": "2010-01-01".
  
  - After that I suppose, that all cities in response will have this params, but it's often to face "gaps" in received datasets, especially for small cities.
    
**Implementation details**
I used django 3.1.4 as a backend framework and bootstrap 5 for css styling.
Web service includes:
1) Main page with user greeting, and a button which lead to the next page(2)
2) Page with all accessible countries. A user can choose specific country and get to page(3).
3) Page with all accessible cities which provides "TAVG" datatype (I used a typeid parameter in GET requests but sometimes it doesn't work).
 A user can get to the page (4) to choose data range for retrieving statistic.
4) Page with form for choosing data range which will be used on page (5) to get statistic.
5) Page which run async coroutines which query and calculate statistic data.
   HTML template was designed with taking into account that coroutines can return empty date in case of data absence on chosen station.
   
Pages 2,3 has pagination, and a toolbar with button leading to page(1)


**What I got after completion of this project**

- I've had a lot of practice with Django (working with templates, urls and views)
- I've refreshed knowledge about working with templates html and bootstrap together
- I had to use curl a lot to collect information about API
- Planning a program flow was interesting because of features of API