# Mood API

### Endpoints

GET: /teams/ 
```
[{
    id: <int>,
    name: <string>,
    slug: <string>,
    description: <string>,
},{
    ...
]}
```

POST/PUT: /teams/ (Create a new team)  
```
{
    id: <int>,
    name: <string>,
    slug: <string>,
    description: <string>,
}
```

DELETE: /teams/{id}  
(Return status 200 or error status code + message)

GET: /users/  
```
[{
    id: <int>,
    name: <string>,
    slug: <string>,
    email: <string>,
},{
    ...
]}
```

POST/PUT: /users/ (Create a new person)  
```
{
    id: <int>,
    name: <string>,
    slug: <string>,
    email: <string>,
}
```

DELETE: /user/{id}  
(Return status 200 or error status code + message)

GET: /moods/?{start_date}=<date>&{end_date}=<date>&{team_id}=<int>&{user_id}=<int>

/team/1/moods


### Models

#### Team
```
{
    id: <int>,
    name: <string>,
    slug: <string>,
    description: <string>,
    created_on: <date time>,
    created_by: <int> (user id),
    modified_on: <date time>,
    modified_by: <int> (user id),
}
```

#### User
```
{
    id: <int>,
    name: <string>,
    slug: <string>,
    email: <string>,
    created_on: <date time>,
    created_by: <int> (user id),
    modified_on: <date time>,
    modified_by: <int> (user id),
}
```

#### Mood
```
{
    id: <int>,
    timestamp: <timestamp>,
    label: <string> (emoji),
    value: <int>,
    user_id: <int>,
    created_on: <date time>,
    created_by: <int> (user id),
    modified_on: <date time>,
    modified_by: <int> (user id),
}
```