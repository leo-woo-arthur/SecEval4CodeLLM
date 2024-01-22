import json
import aiohttp
import asyncio
from retry import retry
from utils.logger_factory import logger


@retry(tries=3, delay=1, backoff=2)
async def call_neb_api_with_retries(p_url, p_headers, p_json):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(p_url, headers=p_headers, json=p_json) as response:
                return await response.json()
    except Exception as e:
        logger.error(f"Func[call_neb_api_with_retries]: Error in session\n    except: {e}")
        # reponse like {'bo': {'chatUuid': '...', 'docId': '...', 'finishReason': 'stop', 'result': '["1+20=21"]'}, 'code': {'code': '0000', 'msg': 'Success', 'msgId': ''}}
        return json.loads('''{'bo': {'result': ['']}, 'code': { 'code': '0001000', 'msg': 'Fail', 'msgId': 'RetCode.Fail' } }''')


async def call_neb_api(p_num, p_question):
    url = "https://.../.../openapi/v1/chat"
    neb_app_id = "...."
    neb_app_key = "...."
    neb_x_auth = "..."
    neb_emp_no = "..."
    headers = { "Content-Type": "application/json", "Authorization": f"Bearer {neb_app_id}-{neb_app_key}", "X-Auth-Value": f"{neb_x_auth}", "X-Emp-No": f"{neb_emp_no}" }
    
    neb_model = "nebulacoder"
    data = { "chatUuid": "", "chatName": "", "stream": False, "keep": True, "text": f"{p_question}", "model": f"{neb_model}" }
        
    response = await call_neb_api_with_retries(url, headers, data)
    
    ret_answer = "Fail or Error"
    if response["code"]["msg"] == "Success":
        try:
            ret_answer = json.loads(response["bo"]["result"])[0]
        except Exception as e:
            logger.error(f"Func[call_neb_api]: Error in json.loads: {response}\n    except: {e}")
    else:
        logger.error(f"Func[call_neb_api]: return fail msg: {response}")
    
    logger.debug(f"Func[call_neb_api]: response: {ret_answer}")
    
    return [p_num, ret_answer]


async def call_neb_apis(p_analyzers, p_func_gen_prompt):
    tasks = []
    for cur_analyzer in p_analyzers:
        prompt = p_func_gen_prompt(cur_analyzer.case_code)
        tasks.append(call_neb_api(cur_analyzer.case_num, prompt))
    results = await asyncio.gather(*tasks)
    return results



