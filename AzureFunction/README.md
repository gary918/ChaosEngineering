# Inject Faults to Azure Functions
Inject some latency and/or exceptions to your running Azure Functions.
## Set up the environment
```
pip install -r requirement.txt
```
## Local test configuration
Change the file name local.settings.sample to local.settings.json. Input the correct value for AZURE_APP_CONFIG_CONNECTION_STRING.
## Local run the function
```
func start
```
Open a brower and type: http://localhost:7071/api/HttpTrigger1?name=gary
Check the result and see if the latency/exceptions've been injected.
## Change the latency injection config
Use the following command to inject latency and/or excpetions.
```
python inject_fault.py --app_config_con_str <connection_str> --is_enabled <True or False> --min_latency 120000 --max_latency 180000 --latency_injection_rate 70  --exception_injection_rate 50 --stop_after_attempt 3 --stop_after_delay 1500000
```
You may set exception_injection_rate to 0 if you only want to inject latency.

## References
* [Simmy and Azure App Configuration](http://www.thepollyproject.org/2019/08/13/simmy-and-azure-app-configuration/)
* [Failure injection for Azure Functions - failure-azurefunctions](https://github.com/gunnargrosch/failure-azurefunctions)
* [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
* Azure App Configuration
  - [Azure App Configuration client library for Python - Version 1.1.1](https://docs.microsoft.com/en-us/python/api/overview/azure/appconfiguration-readme?view=azure-python)
  - [Quickstart: Create a Python app with Azure App Configuration](https://docs.microsoft.com/en-us/azure/azure-app-configuration/quickstart-python#code-samples)
  - [Reduce requests made to App Configuration](https://docs.microsoft.com/en-us/azure/azure-app-configuration/howto-best-practices#reduce-requests-made-to-app-configuration)
  - [Tutorial: Use dynamic configuration in an Azure Functions app (C# only)](https://docs.microsoft.com/en-us/azure/azure-app-configuration/enable-dynamic-configuration-azure-functions-csharp)