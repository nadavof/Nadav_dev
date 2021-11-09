# Face Recognition

**Usage**
'''
Response:
json

{
  "data": List of 3 closest persons
}

'''

**Definitions**
'Get /persons' 
- fail /sucess 
**Response**
'''json
[
{
  "name": "Name"
  "features": "Features"
}

]
'''

##Add a new person
**Definitions**
'Post / persons'

**Arguments**
- '"name": string' the name of the person
- '"features": np array' vector of features

**Response**

- '201 sucess / fail'

'''json
[
  {
    "name": "Name"
    "features": "Features"
  }, 
  {
    "name": "Name"
    "features": "Features"
  }, 
  
  {
    "name": "Name"
    "features": "Features"
  }



]
'''
