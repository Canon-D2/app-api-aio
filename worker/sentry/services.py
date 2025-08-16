import sentry_sdk

class SentryServices:
    def __init__(self) -> None:
        # self.base_url = 'https://a6542d71b1e25396948622b0154a34a8@o4509821824139264.ingest.us.sentry.io/4509821828399104'
        pass
    
    async def parse_query_url(self, data: dict):
        if not data.get('event'):
            return None
        if not data['event'].get('request'):
            return None
        url = data['event']['request']['url']
        query_list = data['event']['request'].get('query_string', [])
        result = url + '?'
        for query in query_list:
            result += query[0] + '=' + query[1] + '&'
        return result[:-1]
    
    async def parse_line_and_lineno(self, data: dict, filename: str):
        event = data['event']
        if not event.get('exception'):
            return None, None
        exception = event['exception']
        if not exception.get('values'):
            return None, None
        values = exception['values']
        for value in values:
            frames = value['stacktrace']['frames']
            for frame in frames:
                if filename == frame['filename']:
                    return frame['context_line'], frame['lineno']
        return None, None
            
    async def parse(self, data: dict):
        result = {}
        result['issues_link'] = data['url']
        result['url'] = await self.parse_query_url(data)
        if not data.get('event'):
            result['method'] = result['title'] = result['function'] = result['filename'] = result['context_line'] = result['lineno'] = None
            return result
        result['method'] = data['event']['request']['method']
        result['title'] = data['event']['title']
        result['function'] = data['event']['metadata'].get('function')
        result['filename'] = data['event']['metadata'].get('filename')
        result['context_line'], result['lineno'] = await self.parse_line_and_lineno(data, result['filename'])
        return result

    async def capture_exception(self, err, request_id):
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("request_id", request_id)
            issue_id = sentry_sdk.capture_exception(err)
        # issue_link = self.base_url + f'?query={issue_id}'
        return issue_id
    

# sentry_services = SentryServices()