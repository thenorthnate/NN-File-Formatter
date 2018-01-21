# NN File Formatter

This is the Database Engine for NN type files. It runs a small server which
can be connected to through a TCP socket. It currently will only handle one
connection at a time, but it could easily be expanded to handle many.

### Request Codes:
0: Create new user; Should include path to private key, username, password
1: Get Token
2: Make Entry; Sent with token
3: Get Data; Sent with token 



https://www.htmlgoodies.com/beyond/reference/article.php/3472941/Server-Response-Codes.htm
### Response Codes:
200: All is good
400: Syntax error
401: Header did not include correct auth codes
403: Forbidden (access not allowed)
404: File not found
410: Content used to be present, but it's gone now
413: Too big - can't be processed
