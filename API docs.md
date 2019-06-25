Final Project for Got It Onboarding Course

# API Docs

## POST /users
This endpoint is used to register a new user.
```
Header:
    Content-Type: application/json
Body:
{
    "username": <string:username>,        #required
    "password": <string:password>,        #required
    "first_name": <string:first_name>,    #optional
    "last_name": <string:last_name>       #optional
}
```
### Successful Request
```
Status code: 201 Created
{
    "description": "User created successfully.",
    "status_code": 201
}
```
### Unsuccessful Request
Username already exists in our database.
```
Status code: 400 Bad Request
{
    "description": "Username already exists.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required username is missing.
```
Status code: 400 Bad Request
{
    "description": "Username is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required password is missing.
```
Status code: 400 Bad Request
{
    "description": "Password is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when creating this user.",
    "error": "Internal Server Error",
    "status_code": 500
}
```
## POST /auth
This endpoint is used to provide access token for registered users.
```
Header:
    Content-Type: application/json

Body:
{
    "username": <string:username>,      #required
    "password": <string:password>       #required
}
```
### Successful request
```
Status code: 200 OK
{
    "access_token": <string:access_token>
}
```
### Unsuccessful request
The required username is missing.
```
Status code: 400 Bad Request
{
    "description": "Username is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required password is missing.
```
Status code: 400 Bad Request
{
    "description": "Password is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The client enters an unregistered user, or an registered user with incorrect password.
```
Status code: 401 Unauthorized
{
    "description": "Invalid credentials",
    "error": "Authorization Required",
    "status_code": 401
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when logging in with this user.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## GET /categories
Retrieve all categories in our current database.
```
No request body needed.
```
### Successful request
```
Status code: 200 OK
[
    {
        "id": <int:id>,
        "name": <string:name>,
        "description": <string:description>,
        "date_created": <DateTime:date_created>,
        "date_modified": <DateTime:date_modified>,
        "items": [
            item1_info,
            item2_info,
            ...
        ]
    },
    {
        category2_info
    }
    ...
]
```
### Unsuccessful request
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when getting all the categories.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## GET /categories/<int:category_id>
Retrieve a specific category in our current database.
```
No request body needed.
```
### Successful request
```
Status code: 200 OK
{
    "id": <int:id>,
    "name": <string:name>,
    "description": <string:description>,
    "date_created": <DateTime:date_created>,
    "date_modified": <DateTime:date_modified>,
    "items": [
        item1_info,
        item2_info,
        ...
    ]
}
```
### Unsuccessful request
This category does not exist in our database.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when getting this category.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## POST /categories/<int:category_id>
Create a new category in our database.
```
Header:
    Content-Type: application/json
    Authorization Required: JWT <string:access_token>

Body:
{
    "name": <string:name>,                  #required
    "description": <string:description>     #optional
}
```
### Successful request
```
Status code: 201 Created
{
    "id": <int:id>,
    "name": <string:name>,
    "description": <string:description>,
    "date_created": <DateTime:date_created>,
    "date_modified": <DateTime:date_modified>,
    "items": []
}
```
### Unsuccessful request
The required category name is missing.
```
Status code: 400 Bad Request
{
    "description": "Category name is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The category name already exists.
```
Status code: 400 Bad Request
{
    "description": "Category name already exists.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required authorization is missing.
```
Status code: 401 Unauthorized
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
The access token is expired.
```
Status code: 401 Unauthorized
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when creating this category.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## GET /categories/<int:category_id>/items
Retrieve all items in a specific category.
```
No request body needed.
```
### Successful request
```
Status code: 200 OK
[
    {
        "id": <int:id>,
        "name": <string:name>,
        "description": <string:description>,
        "date_created": <DateTime:date_created>,
        "date_modified": <DateTime:date_modified>,
    },
    {
        item2_info
    }
    ...
]
```
### Unsuccessful request
The category does not exist.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when getting all the items in this category.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## GET /categories/<int:category_id>/items/<int:item_id>
Retrieve a specific item in our current category.
```
No request body needed.
```
### Successful request
```
Status code: 200 OK
{
    "id": <int:id>,
    "name": <string:name>,
    "description": <string:description>,
    "date_created": <DateTime:date_created>,
    "date_modified": <DateTime:date_modified>,
}
```
### Unsuccessful request
The category does not exist.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
This item does not exist in our current category.
```
Status code: 404 Not Found
{
    "description": "Item not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when getting this item.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## POST /categories/<int:category_id>/items
Create a new item in this category.
```
Header:
    Content-Type: application/json
    Authorization Required: Bearer <string:token>

Body:
{
    "name": <string:name>,                  #required
    "description": <string:description>     #optional
}
```
### Successful request
```
Status code: 201 Created
{
    "id": <int:id>,
    "name": <string:name>,
    "description": <string:description>,
    "date_created": <DateTime:date_created>,
    "date_modified": <DateTime:date_modified>,
}
```
### Unsuccessful request
The required item name is missing.
```
Status code: 400 Bad Request
{
    "description": "Item name is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required authorization is missing.
```
Status code: 401 Unauthorized
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
The access token is expired.
```
Status code: 401 Unauthorized
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
You are not the owner of this item.
```
Status code: 403 Forbidden
{
    "description": "You don't have permission to do this",
    "error": "Forbidden Error",
    "status_code": 403
}
```
The category does not exist.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when creating this item.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## DELETE /categories/<int:category_id>/items/<int:item_id>
Delete an unwanted item in this category.
```
Header:
    Content-Type: application/json
    Authorization Required: Bearer <string:token>
```
### Successful request
```
Status code: 204 No Content
{
    "description": "Item deleted.",
    "status_code": 204
}
```
### Unsuccessful request
The required authorization is missing.
```
Status code: 401 Unauthorized
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
The access token is expired.
```
Status code: 401 Unauthorized
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
You are not the owner of this item.
```
Status code: 403 Forbidden
{
    "description": "You don't have permission to do this",
    "error": "Forbidden Error",
    "status_code": 403
}
```
The category does not exist.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
This item does not exist.
```
Status code: 404 Not Found
{
    "description": "Item not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when deleting this item.",
    "error": "Internal Server Error",
    "status_code": 500
}
```

## PUT /categories/<int:category_id>/items/<int:item_id>
Update an existing item in this category.
```
Header:
    Content-Type: application/json
    Authorization Required: Bearer <string:token>

Body:
{
    "name": <string:name>                   #required
    "description": <string:description>     #optional
}
```
### Successful request
Return an updated item description.
```
Status code: 200 OK
{
    "id": <int:id>,
    "name": <string:name>,
    "description": <string:description>,
    "date_created": <DateTime:date_created>,
    "date_modified": <DateTime:date_modified>,
}
```
### Unsuccessful request
The required item name is missing.
```
Status code: 400 Bad Request
{
    "description": "Item name is required.",
    "error": "Bad Request",
    "status_code": 400
}
```
The required authorization is missing.
```
Status code: 401 Unauthorized
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
The access token is expired.
```
Status code: 401 Unauthorized
{
    "description": "Signature has expired",
    "error": "Authorization Required",
    "status_code": 401
}
```
You are not the owner of this item.
```
Status code: 403 Forbidden
{
    "description": "You don't have permission to do this",
    "error": "Forbidden Error",
    "status_code": 403
}
```
The category does not exist.
```
Status code: 404 Not Found
{
    "description": "Category not found.",
    "error": "Not Found",
    "status_code": 404
}
```
The item does not exist.
```
Status code: 404 Not Found
{
    "description": "Item not found.",
    "error": "Not Found",
    "status_code": 404
}
```
Unexpected Internal Server Error.
```
Status code: 500 Internal Server Error
{
    "description": "An unexpected Internal Server Error occurred when updating this item.",
    "error": "Internal Server Error",
    "status_code": 500
}
```
