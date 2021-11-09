# Face Recognition

## Usage
- Post a person to a DB
- For an input person, get the 3 most similar persons in DB.

## Description

### Add a new person

**Definitions**
'Post / persons'

**Arguments**
- '"name": string' the name of the person
- '"features": np array' vector of features

**Response**
- '201, SUCESS / 400, FAIL'

### Get most similar persons in DB

**Definitions**
'Get / persons'

**Arguments**
- '"features": np array' vector of features
- 
**Response**
3 most similar person by a dot product 
{
  "SUCESS": (Name, Features)
}



