import os
import json
import logging

import azure.functions as func
from shared_code.FaultInjection import *
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_incrementing,
    before_sleep_log,
    Retrying,
    wait_random,
    before_log,
    after_log
)


# Function needs to be retried
# @retry(reraise=True, stop=stop_after_attempt(3),wait=wait_random(0, 3))
def process_data(data):
    # print(process_data.retry.statistics)
    print(f"....processing data:{data}")
    if random.randint(0, 10) > 1:
        print(".....Need retry")
        raise Exception("......Failed process the data!")
    else:
        print(".....Don't need retry")
        return f"Awesome {data}!"


def str_to_bool(str):
    return True if str.lower() == 'true' else False


# Get the configruation from Azure App Configuration
# AZURE_APP_CONFIG_CONNECTION_STRING should be stored in local.settings.json for local test
# or in appsettings.json for function deployment
def get_fault_injection_config():
    injection_config = None
    
    try:
        connection_string = os.getenv('AZURE_APP_CONFIG_CONNECTION_STRING')
        app_config_client = AzureAppConfigurationClient.from_connection_string(connection_string)
        latency_injection = app_config_client.get_configuration_setting(key="fault_injection").value
        injection_config = json.loads(latency_injection)
    except Exception as e:
        print(e)
    print(injection_config)
    return injection_config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logger = logging.getLogger(__name__)
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    injection_config = get_fault_injection_config()

    faultInjector=None
    retryer=None
    try:
        # No @retry
        """ faultInjector = FaultInjector (is_enabled=is_enabled, min_latency=1000, max_latency=3000, latency_injection_rate=70)
        name = faultInjector (process_data, [name])
        last_status = faultInjector.get_last_status()
        print (f"STATUS:{last_status}") """
        # Use Retrying without @retry
        retryer = Retrying(
            reraise=True, 
            stop=(stop_after_attempt(injection_config["retry:stop_after_attempt"])|stop_after_delay(injection_config["retry:stop_after_delay"]/1000)),
            wait=wait_random(0, 3) + wait_incrementing(start=1, \
            increment=1, \
            max=2),
            before=before_log(logger, logging.INFO),
            after=after_log(logger, logging.INFO))
        faultInjector = FaultInjector (
            is_enabled=injection_config["fault_injection:is_enabled"], 
            min_latency=injection_config["fault_injection:min_latency"], 
            max_latency=injection_config["fault_injection:max_latency"], 
            latency_injection_rate=injection_config["fault_injection:latency_injection_rate"],
            exception_injection_rate=injection_config["fault_injection:exception_injection_rate"])
        name = retryer(faultInjector, process_data, [name])
        print(faultInjector.get_last_status())
    except Exception as e:
        print(faultInjector.get_last_status())
        print(f"EXCEPTION:{e}")

    stat = retryer.statistics
    if stat is not None:
        stat["file_url"]="file_url"
        stat=json.dumps(stat)
        print(stat)


    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
