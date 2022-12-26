Take me to the [project proposal](#proposal)

Take me to the [installation instructions](#installation)

# BostonCrimeDashboard
### This the final project for a DS2000 course at Northeastern University. It was recently completed.

Given a data set (selected by student groups), create descriptive graphs and generate insights. The students are to explain the topic and why it is significant. To be significant, the project should address some issue or topic that is important scientifically or culturally.

Below is a part of the submitted propoal for the project
<a name="proposal"></a>
> DS2000 Project Proposal: Crime Rates in Boston Dashboard
> 
> Introduction: 
> Our topic focuses on crime incidents in the city of Boston. We chose this topic because of its importance in creating a safe environment for the residents of Boston neighborhoods. Having easy access to information about the frequency, location, and type of crime is vital for the residents of Boston to ensure their own safety. On top of that, exploring crime rates in Boston is significant to the lawmakers and law enforcement in terms of them deciding where reform is needed and where resources can be better allocated.
> 
> Project Goals:  
> For this project, our goals are to visualize different aspects of the crime rates in Boston on a single dashboard. In this dashboard, we hope to create a scatterplot map of the concentration of crimes in order to evaluate which parts of Boston experience the highest crime rates. We also hope to create a visualization of when these crimes are most prevalent (time of day, day of week, month, year, etc.), and use that to compare when crimes are most likely to be violent. 
> For functionality, we hope to build an easy-to-navigate dashboard that enables the user to filter crimes by several different kinds of categories. This includes, but may not be limited to, the following criteria: time of day, day of the week, month, year, location of crime, and type of crime. This dashboard will include a map of boston where all of the filtered data will be displayed, as well as relevant data visualizations (e.g. bar chart, pie graph) of selected criteria.
> 
> Data Sources: 
> The data source that we will be using can be accessed [here](https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system/resource/313e56df-6d77-49d2-9c49-ee411f10cf58) (or below if the link doesn’t work). It shows the crime incident reports in Boston since August 2015 — 2022. There are over 59,000 data entries and they are provided by the Boston Police Department. The data source includes the following information: the incident number, offense code, offense description districts in Boston, reporting area, shootings, when and where it occurred. In regards to when it happens, the data source provides the specific date and time of when the crime occured so we can use it to create a visualization of when these crimes happen and test our hypothesis. It also provides the longitude and latitude, so we can use that data to create a scatterplot map of where crime is concentrated the most in Boston. 
> 
> Data Source: https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system/resource/313e56df-6d77-49d2-9c49-ee411f10cf58

<a name="installation"></a>
### Installation
Since this project is aimed at beginner programmers, I will describe how to complete the setup necessary to run this code. First, you will need to install the dependencies of the program. The following instructions are for Mac users.
1. First, enter your virtual environment. If using the *anaconda* distribution, you can do this with the following command in your terminal window:
```
conda activate YourVirtualEnvironmentNameGoesHere
```
2. Install the packages! Copy and paste the below commands, one at a time into terminal. If you're using the Anaconda distribution, you should already have Pandas installed automatically, so you don't need to install it.
```
conda install -c conda-forge dash
```
```
conda install -c plotly plotly=5.11.0
```
```
conda install -c conda-forge shapely
```

3. Download the app.py file to a place of your choosing.

4. Run the app.py file.
- Note: The dashboard should update automatically upon saving the file. If you try running *app.py* in Spyder or another IDE multiple times, you may get an error message that the link is already busy. To get around this, you can run the file in terminal instead.

5. Visit the provided link in your web browser!
