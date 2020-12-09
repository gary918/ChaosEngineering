import argparse
import os
import json
import logging

from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting


# python inject_fault.py --app_config_con_str xxx --enable_latency_injection False --min_latency 120000 --max_latency 180000 --latency_injection_rate 70
def main():
    parser = argparse.ArgumentParser("Update Azure App Configuration settings...")
    parser.add_argument(
        "--app_config_con_str",
        type=str,
        required=True,
        help="Azure App Configuration Connection String")
    parser.add_argument(
        "--enable_latency_injection",
        type=eval,
        required=True,
        choices=[True,False],
        help="Enable Latency Injection or not"
    )
    parser.add_argument(
        "--min_latency",
        type=int,
        help="Min latency in milli-seconds"
    )
    parser.add_argument(
        "--max_latency",
        type=int,
        help="Max latency in milli-seconds"
    )
    parser.add_argument(
        "--latency_injection_rate",
        type=int,
        help="Latency injection rate"
    )

    args = parser.parse_args()
    connection_string = args.app_config_con_str

    setting = {}
    setting["LatencyInjectionIsEnabled"]=args.enable_latency_injection
    setting["MinLatency"]=args.min_latency
    setting["MaxLatency"]=args.max_latency
    setting["LatencyInjectionRate"]=args.latency_injection_rate
    setting = json.dumps(setting, indent=2)

    # {"LatencyInjectionIsEnabled": true, "MinLatency": 120000, "MaxLatency": 180000, "LatencyInjectionRate": 70}
    print("Updating latency injection configuration for 'LatencyInjection'")
    print(setting)

    added_config_setting = ConfigurationSetting(key="LatencyInjection", value=setting)

    try:
        app_config_client = AzureAppConfigurationClient.from_connection_string(connection_string)
        updated_config_setting = app_config_client.set_configuration_setting(added_config_setting)
        print("Updated Key: " + updated_config_setting.key)
        print("with Value: " + updated_config_setting.value)
    except Exception as e:
        print(e)

if __name__=="__main__":
    main()




