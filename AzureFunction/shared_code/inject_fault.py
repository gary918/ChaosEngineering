import argparse
import os
import json
import logging

from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting


# python inject_fault.py --app_config_con_str xxx --is_enabled False --min_latency 120000 --max_latency 180000 --latency_injection_rate 70
def main():
    parser = argparse.ArgumentParser("Update Azure App Configuration settings...")
    parser.add_argument(
        "--app_config_con_str",
        type=str,
        required=True,
        help="Azure App Configuration Connection String")
    parser.add_argument(
        "--is_enabled",
        type=eval,
        required=True,
        choices=[True,False],
        help="Enable Fault Injection or not"
    )
    parser.add_argument(
        "--min_latency",
        type=int,
        default=0,
        help="Min latency in milli-seconds"
    )
    parser.add_argument(
        "--max_latency",
        type=int,
        default=0,
        help="Max latency in milli-seconds"
    )
    parser.add_argument(
        "--latency_injection_rate",
        type=int,
        required=True,
        default=0,
        help="Latency injection rate"
    )
    parser.add_argument(
        "--exception_injection_rate",
        type=int,
        required=True,
        default=0,
        help="Exception injection rate"
    )
    parser.add_argument(
        "--stop_after_attempt",
        type=int,
        default=3,
        help="Retry stop_after_attempt"
    )
    parser.add_argument(
        "--stop_after_delay",
        type=int,
        default=15000,
        help="Retry stop_after_delay"
    )

    args = parser.parse_args()
    connection_string = args.app_config_con_str

    setting = {}
    setting["fault_injection:is_enabled"]=args.is_enabled
    setting["fault_injection:min_latency"]=args.min_latency
    setting["fault_injection:max_latency"]=args.max_latency
    setting["fault_injection:latency_injection_rate"]=args.latency_injection_rate
    setting["fault_injection:exception_injection_rate"]=args.exception_injection_rate
    setting["retry:stop_after_attempt"]=args.stop_after_attempt
    setting["retry:stop_after_delay"]=args.stop_after_delay
    setting = json.dumps(setting, indent=2)

    # {"LatencyInjectionIsEnabled": true, "MinLatency": 120000, "MaxLatency": 180000, "LatencyInjectionRate": 70}
    print("Updating fault injection configuration...")
    # print(setting)

    added_config_setting = ConfigurationSetting(key="fault_injection", value=setting)

    try:
        app_config_client = AzureAppConfigurationClient.from_connection_string(connection_string)
        updated_config_setting = app_config_client.set_configuration_setting(added_config_setting)
        print("Key: " + updated_config_setting.key)
        print("Value: " + updated_config_setting.value)
    except Exception as e:
        print(e)

if __name__=="__main__":
    main()




