[comment]: # "Auto-generated SOAR connector documentation"
# Google Cloud IAM

Publisher: Splunk Community  
Connector Version: 1\.0\.2  
Product Vendor: Google  
Product Name: Cloud IAM  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.10\.0\.40961  

This app integrates with Google Cloud IAM

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)"
[comment]: # ""
Actions in this app utilize the following API: https://cloud.google.com/iam/docs/reference/rest

## Explanation of Asset Configuration Parameters

The asset configuration parameters affect \[test connectivity\] and all the other actions of the
application. Below are the explanation and usage of all those parameters.

-   **Contents of Service Account JSON file -** After creating a Service Account for authenticating
    with Google Cloud Storage (https://console.cloud.google.com/iam-admin/serviceaccounts/project),
    the file can be downloaded. Paste the contents into the asset configuration input as-is.
-   **Project ID -** The Google Cloud Project ID.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Cloud IAM asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**key\_json** |  required  | password | Contents of Service Account JSON file
**project** |  required  | string | Google Cloud Project ID

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[enable serviceaccount](#action-enable-serviceaccount) - Enables a ServiceAccount that was disabled previously  
[disable serviceaccount](#action-disable-serviceaccount) - Disables a ServiceAccount immediately  
[get serviceaccount](#action-get-serviceaccount) - Gets a ServiceAccount  
[list serviceaccountkey](#action-list-serviceaccountkey) - Lists every ServiceAccountKey for a service account  
[get serviceaccountkey](#action-get-serviceaccountkey) - Gets a ServiceAccountKey  
[delete serviceaccountkey](#action-delete-serviceaccountkey) - Deletes a ServiceAccountKey  
[create serviceaccountkey](#action-create-serviceaccountkey) - Creates a ServiceAccountKey  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'enable serviceaccount'
Enables a ServiceAccount that was disabled previously

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'disable serviceaccount'
Disables a ServiceAccount immediately

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get serviceaccount'
Gets a ServiceAccount

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.data\.\*\.displayName | string | 
action\_result\.data\.\*\.email | string | 
action\_result\.data\.\*\.etag | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.projectId | string | 
action\_result\.data\.\*\.uniqueId | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list serviceaccountkey'
Lists every ServiceAccountKey for a service account

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.data\.0\.keys\.\*\.keyAlgorithm | string | 
action\_result\.data\.0\.keys\.\*\.keyOrigin | string | 
action\_result\.data\.0\.keys\.\*\.keyType | string | 
action\_result\.data\.0\.keys\.\*\.name | string | 
action\_result\.data\.0\.keys\.\*\.validAfterTime | string | 
action\_result\.data\.0\.keys\.\*\.validBeforeTime | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get serviceaccountkey'
Gets a ServiceAccountKey

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 
**key** |  required  | Name of key | string |  `gcloudiam key` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.parameter\.key | string |  `gcloudiam key` 
action\_result\.data\.0\.keyAlgorithm | string | 
action\_result\.data\.0\.keyOrigin | string | 
action\_result\.data\.0\.keyType | string | 
action\_result\.data\.0\.name | string | 
action\_result\.data\.0\.validAfterTime | string | 
action\_result\.data\.0\.validBeforeTime | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete serviceaccountkey'
Deletes a ServiceAccountKey

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 
**key** |  required  | Name of key | string |  `gcloudiam key` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.parameter\.key | string |  `gcloudiam key` 
action\_result\.data | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create serviceaccountkey'
Creates a ServiceAccountKey

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**account** |  required  | Email address or the uniqueId of the service account | string |  `email` 
**save\_key\_to\_vault** |  optional  | Whether or not to save the key to vault | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.account | string |  `email` 
action\_result\.parameter\.save\_key\_to\_vault | boolean | 
action\_result\.data\.0\.filename | string | 
action\_result\.data\.0\.keyAlgorithm | string | 
action\_result\.data\.0\.keyOrigin | string | 
action\_result\.data\.0\.keyType | string | 
action\_result\.data\.0\.name | string | 
action\_result\.data\.0\.privateKeyData | string | 
action\_result\.data\.0\.validAfterTime | string | 
action\_result\.data\.0\.validBeforeTime | string | 
action\_result\.data\.0\.vault\_id | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 