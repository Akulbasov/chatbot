import json
from google.cloud import dialogflow
from google.protobuf.json_format import MessageToJson, MessageToDict


class DialogFlowProccess:
    def __init__(self, project_id="chatbotforut", language_code="eng"):
        self.DIALOGFLOW_PROJECT_ID = project_id
        self.DIALOGFLOW_LANGUAGE_CODE = language_code


    def recognize_text(self, text=None, session_id=None):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.DIALOGFLOW_PROJECT_ID, "2")
        text_input = dialogflow.TextInput(text=text, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        print(response.query_result)
        return {
            "intent": {
                "display_name":  response.query_result.intent.display_name,
                "detection_confidence": response.query_result.intent_detection_confidence,
                "query_text": response.query_result.query_text
            },
            "parameters": response.query_result
        }
