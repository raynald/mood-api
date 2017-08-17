# Mood API

### Endpoints

#### Team
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

#### User
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

POST/DELETE: /memberships (Create/Delete a team user relationship)
(Return status 200 or error status code + message)
```
{
    team_id: <int>,
    user_id: <int>
}
```

#### Mood
GET: /moods/?{start_date}=<date>&{end_date}=<date>&{team_id}=<int>&{user_id}=<int>
Provide either team_id or user_id.
```
[{
    user: {
        id: <int>,
        name: <string>
    },
    timestamp: <timestamp>,
    label: <string> (emoji),
    value: <int>,    
},{
    user: {
        id: <int>,
        name: <string>,
    },
    timestamp: <timestamp>,
    label: <string> (emoji),
    value: <int>,    
},
...
]
```

GET Average
GET: /average/?{start_date}=<date>&{end_date}=<date>&{team_id}=<int>&{user_id}=<int>
Provide either team_id or user_id.
```
[{
    user: {
        id: <int>,
        name: <string>
    },
    average: <float>
},{
    ...
},
<float> # team / personal average score
]
```

#### Snippet
GET: /snippets/?{start_date}=<date>&{end_date}=<date>&{team_id}=<int>&{user_id}=<int>
Provide either team_id or user_id.
```
[{
    user: {
        id: <int>,
        name: <string>
    },
    timestamp: <timestamp>,
    content: <string> (description of feeling)
},{
    user: {
        id: <int>,
        name: <string>,
    },
    timestamp: <timestamp>,
    content: <string> (description of feeling)
},
...
]
```

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

#### Snippet
```
{
    id: <int>,
    timestamp: <timestamp>,
    content: <string> (description of feeling),
    user_id: <int>,
    created_on: <date time>,
    created_by: <int> (user id),
    modified_on: <date time>,
    modified_by: <int> (user id),
}
```
