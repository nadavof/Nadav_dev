# Face Recognition

**Usage**


**Definitions**
'Get /persons' 
- fail /sucess 
**Response**

{
  "name": "Name"
  "features": "Features"
}

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
