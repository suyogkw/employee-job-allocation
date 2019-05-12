# employee-job-allocation
This is to solve a simple problem of rotation of employees to different teams based upon their preferences and interview performances.

The problem statement : 
In an organization, the graduates are put into different projects belonging to different verticals. at the end of the year, the graduates have to shift to different project compulsorily called as rotation. The condition is that the next project can not be under same vertical.

There is a list of project and their capacities to absorb graduates along with the vertical it is part of. [Jobs.xlsx]
There is a list of graduates along with n number of preferences they are asked to give. [Graduates.xlsx]

The cases are : 

1) Ordered preferences : where graduates are asked for preferences in the order of their interest to join that project. If graduate is selected in multiple projects by means of interview, he/she will get his/her higher preference.

2) Unordered preferences : where graduates are asked for choices and not peferences. they will provide with n choices and assumed to be happy with getting either of n projects if possible.

Selection process : The list of interviewees is sent to project lead if more than one have applied for the job depending upon the case. the leads will take interviews and report back their preferences. [InterviewResults.xlsx]
Different algorithms will be applied to get different results and will be chosen by the rotation program manager.

The process happens in multiple rounds.
Result are in the form of graduate-job allocations for that round and lists of remaining jobs and graduates.
