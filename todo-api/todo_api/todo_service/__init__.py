import json

from todo_service import todo_create, todo_update, todo_delete, todo_list, todo_detail
from todo_service.repository import MemTodoRepository
from todo_service.todos import TODO_DATA

routes = {
    ('GET', '/todos'): todo_list.lambda_handler,
    ('GET', '/todos/{id}'): todo_detail.lambda_handler,
    ('POST', '/todos'): todo_create.lambda_handler,
    ('PUT', '/todos/{id}'): todo_update.lambda_handler,
    ('DELETE', '/todos/{id}'): todo_delete.lambda_handler,
}


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    request_context = event['requestContext']
    path = request_context['resourcePath']
    http_method = request_context['httpMethod']
    todo_repository = MemTodoRepository(TODO_DATA)
    try:
        return routes[(http_method, path)](event, context, todo_repository=todo_repository)
    except:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "not found",
                'path': path,
                'httpMethod': http_method,
                'requestContext': request_context,
            })
        }
