# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
import logging
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from datetime import *
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_intros = ["Welcome to the official FIFA skill. What would you like to know about the current matches?", "Hi, this is FIFA. What would you like to know?", "Hello, welcome to FIFA. Ask me anything."]
        speech_text = random.choice(speech_intros)
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class MatchesIntentHandler(AbstractRequestHandler):
    """Handler for Matches Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Matches")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        #logger.info("In Matches now.")
        #logger.info(handler_input.request_envelope)
        
        timeframe_value = get_slot_value(handler_input=handler_input, slot_name="timeframe")
        
        delta = datetime.strptime(timeframe_value, "%Y-%m-%d").day - datetime.now().day
    
        if delta == 0:  
            speech_text = "Today we have Germany playing against Switzerland and Ukraine against England"
        elif delta == 1:
            speech_text = "Tomorrow Serbia is playing against Russia and South Africa against Australia"
        elif delta == 2:
            speech_text = "On " + timeframe_value + " Marokko plays against Saudi Arabia"
        else:
            speech_text = "I have no record of games on " + timeframe_value      
        
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        
        return handler_input.response_builder.response


class MatchSearchIntentHandler(AbstractRequestHandler):
    """Handler for MatchSearch Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Matchsearch")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
 
        country_value = get_slot_value(
            handler_input=handler_input, slot_name="country")
            
        event_value = get_slot_value(
            handler_input=handler_input, slot_name="event")
            
        session_attr["selectedCountry"] = country_value
        
        if country_value == 'Germany': 
            speech_text = "Germany is playing today against Switzerland. <break strength='strong'/> Do you want to know when this game is on?"
        elif country_value == 'Australia': 
            speech_text = "Australia is playing tomorrow against South Africa. <break strength='strong'/> Do you want to know when this game is on?"
        else:
            speech_text = "I have no record of games for " + country_value      
        
            
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response
        

class ResultsIntentHandler(AbstractRequestHandler):
    """Handler for Results Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Results")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        timeframe_value = get_slot_value(handler_input=handler_input, slot_name="timeframe")
 
        delta = datetime.now().day - datetime.strptime(timeframe_value, "%Y-%m-%d").day
    
        if delta == 0:  
            speech_text = "Today Brazil won 3 to 0 against Argentina and Portugal played draw 0 0 with Spain"
        elif delta == 1:
            speech_text = "Yesterday Egypt played 1 to 0 against South Korea and United States played 3 to 2 with Canada"
        elif delta == 2:
            speech_text = "On " + timeframe_value + " Bosnia lost 2:3 to Croatia"
        else:
            speech_text = "I have no record of games on " + timeframe_value      
        
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class StatsIntentHandler(AbstractRequestHandler):
    """Handler for Stats Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Stats")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        country_value = get_slot_value(
            handler_input=handler_input, slot_name="country")
            
        stat_value = get_slot_value(
            handler_input=handler_input, slot_name="stat")
            
        if not country_value:
            speech_text = "The top scorers of the FIFA Women World Cup so far are Marco Cronin with 6 goals for Ireland, Iunia Borza with 4 goals for Romania and Tasiana Guevarana with 3 goals for Spain"
        elif country_value == 'Switzerland':
            speech_text = "The best scorer of the FIFA Women World Cup for Switzerland is Janna Wilderama with 2 goals"
        else:
            speech_text = "I don't have that statistics"
            
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        country_value = session_attr["selectedCountry"]
        
        if not country_value:
            speech_text = ""
        elif country_value == 'Germany':
            speech_text = "Germany against Switzerland is today at 18:00"
        elif country_value == 'Australia':
            speech_text = "Australia against South Africa is tomorrow at 13:30"
        else:
            speech_text = "I don't have information for " + country_value
            
        session_attr["selectedCountry"] = ""
        
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speech_text = "Ok, anything else?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
        
        
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me! How can I help?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.
class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = ("You just triggered {}").format(intent_name)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class ErrorHandler(AbstractExceptionHandler):
    """Catch-all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


# This handler acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(MatchesIntentHandler())
sb.add_request_handler(MatchSearchIntentHandler())
sb.add_request_handler(ResultsIntentHandler())
sb.add_request_handler(StatsIntentHandler())

sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(ErrorHandler())

handler = sb.lambda_handler()