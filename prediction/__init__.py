import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('userId')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('userId')

    if user_id:
        response = json.dumps([user_id]*3)
        logging.info(response)
        return func.HttpResponse(response)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user ID in the query string or in the request body to get predictions.",
             status_code=200
        )
