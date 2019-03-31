import zulip_bots.bots.kenkyu.helper_main as HM
from typing import Any

class KenkyuHandler(object):
    '''
    This chatbot makes a connection between the various APIs that can aid a researcher.
    e.g. Find them the research paper they're looking for, find similar research paper,
    look through confusing terms etc.
    '''

    def usage(self) -> str:
        return '''
                This chatbot makes a connection between the various APIs that can aid a researcher.
                e.g. Find them the research paper they're looking for, find similar research paper,
                look through confusing terms etc.

                Following are some examples of bot triggers

                1. What are some trending research papers?
                2. I want to scrape all the images from this paper.
                3. What does the following word mean? 
                4. I want to search and download this paper.
                5. What is this research paper about?
                6. Make a note! Start! Stop!

                '''

    def handle_message(self, message, bot_handler: Any):
        user_query = message['content']
        query_type = HM.understand(user_query)
        print("Query type is {}".format(query_type))
        if query_type == 'ABSTRACT':
            response_ = HM.findActualContent('test4.pdf')[0]
        if query_type == 'DEFINITION':
            user_query = user_query.replace('Can you tell me the meaning of this? ', '')
            response_ = HM.showMeaning(user_query)
        if query_type == 'TRENDS':
            query_response = HM.trendingPapers()
            titles = [data['title'] for data in query_response]
            abstracts = [data['abstract'] for data in query_response]
            response_ = "This week's top three trending papers are, " \
                        "{}, and the paper is about {}. /n" \
                        "{} and the paper is about {}. /n" \
                        "{} and the paper is about {}.".format(titles[0], abstracts[0],
                                                               titles[1], abstracts[1],
                                                               titles[2], abstracts[2])
        if query_type == 'SCRAPE_IMAGE':
            HM.extractImages('test4.pdf')
            response_ = "Extracted all images :) Check {}".format(os.getcwd())
        if query_type == 'SEARCH_DOWNLOAD':
            user_query = user_query.replace('I want to download this paper', '')
            url = HM.searchDownload(user_query)
            response_ = "Download is available here {}".format(url)
        bot_handler.send_reply(message, response_)




handler_class = KenkyuHandler
