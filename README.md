# hostfact-python-client
This package intended for communication with Hostfact in python applications. All what you need is to create client object and call his methods:

```
from hostfact_client import HostFact

client = HostFact(url="your host fact address", api_key="your_secret")
```

All calls based on the next logic (<b>There are also exceptions that marked with *</b>) and returns a JSON object as result:
```
client.{controller_name}.{action}
```

<b>*controller_name</b> - module that is responsible for a certain functionality, like <b>invoice</b> logic (`client.invoice.{action}`), <b>debtor</b> logic (`client.debtor.{action}`).

<b>**action</b> - method that perform necessary function like add (`client.invoice.add`), edit (`client.invoice.edit`), list (`client.debtor.list`), etc.

<b>All controllers and actions you can find on this page:</b> 
https://www.hostfact.nl/developer/api/


## Make invoices

This is a helper method that create or edit an invoice and allow adding attachments for it.

<b>Parameters list:</b><br>
<b>debtor_code</b> (mandatory) - DebtorCode to whom the invoice is intended.<br>
<b>invoice_lines</b> (mandatory) - InvoiceLines list. <b>Lines always upend to list.</b> If you want to update the existent InvoiceLines' item use `client.invoice.edit()` call.<br>
<b>newInvoice</b> (optional, by default False) - if True, the method will create a new invoice even though customer already has invoice.<br>
<b>attachment</b> (optional, by default None) - dictionary that containe file 'name' and 'content' (base64 string)<br>


```
import base64

from hostfact_client import HostFact

client = HostFact(url="your host fact address", api_key="your_secret")

# Read from file
with open("test.txt", "rb") as my_file:
    filename = my_file.name
    attachment = base64.b64encode(my_file.read()).decode("utf-8")

# Updload string
# filename = "test.txt"
# attachment = base64.b64encode("Hello world".encode()).decode("utf-8")


client.invoice.make_invoice(**{
    "debtor_code": "DB100",
    "invoice_lines": [
        {
            "Description": "some text",
            "PriceExcl": 999
        },
        {
            "ProductCode": "P008",
            "Description": "description"
        }
    ],
    "attachment": {
        "name": filename,
        "content": attachment
    }
})
```


## Create new Invoice

With this function you can create an invoice in HostFact. If you indicate that the invoice should have the status 'Draft' (= 0) then no 'InvoiceCode' should be given.

<b>Mandatory fields</b>: Debtor or DebtorCode and InvoiceLines (minimum 1)

All parameters list you can find on this page: https://www.hostfact.nl/developer/api/facturen/add

```
client.invoice.add(**{
    "DebtorCode": "DB100",
    "InvoiceLines": [
        {
            "Description": "Setupfee",
            "PriceExcl": 150
        },
        {
            "ProductCode": "P003",
            "Description": "Domain example.com"
        }
    ]
})
```

## Edit Invoice

This method allows editing an invoice.
Only entered parameters are changed.

<b>Mandatory fields</b>: `Identifier` or `InvoiceCode`

All parameters list you can find on this page: https://www.hostfact.nl/developer/api/facturen/edit

The next call will update (or create) a line with id 777 and upend lines that don't have Identifier in the body.

```
client.invoice.edit(**{
    "Identifier": 666,
    "InvoiceLines": [
        {
            "Identifier": 777
            "Description": "Test edit",
            "PriceExcl": 999
        },
        {
            "ProductCode": "P007",
            "Description": "Domain edit.example.com"
        }
    ]
})
```

## Show Invoice

This method allows you to retrieve more information about an invoice.

<b>Mandatory fields</b>: `Identifier` or `InvoiceCode`

```
client.invoice.show(Identifier=666)
```

## Delete InvoiceLines items
This method allowed you to remove an invoice line from an existing invoice. This method is available for an invoice in all statuses.

<b>Mandatory fields</b>: `Identifier` or `InvoiceCode`

```
client.invoiceline.delete(Identifier=9999, InvoiceLines=[{"Identifier": 333333}, {"Identifier": 333334}])
```


## List Invoice
This method allows you to retrieve a list of invoices that meet the specified parameters.

You can indicate `sort`, `order`, `offset` and `limit` and parameters for filtering (`status`, `modified`, etc)

All parameters list you can find on this page: https://www.hostfact.nl/developer/api/facturen/list

```
client.invoice.list(DebtorCode=debtor_code, Status=0, sort="Modified")
```

## Add attachment to invoice

This method allows you to add an attachment to an existing invoice. This function is available for an invoice in all statuses.

<b>Mandatory fields</b>: `ReferenceIdentifier` or `InvoiceCode`, `Type`, `Filename` and `Base64`

```
import base64

from hostfact_client import HostFact

client = HostFact(url="your host fact address", api_key="your_secret")

# Read from file
with open("test.txt", "rb") as my_file:
    filename = my_file.name
    attachment = base64.b64encode(my_file.read()).decode("utf-8")

# Updload string
# filename = "test.txt"
# attachment = base64.b64encode("Hello world".encode()).decode("utf-8")


client.attachment.add(**{
    "InvoiceCode": "[concept]0003",
    "Type": "invoice",
    "filename": "test.txt",
    "base64": "SGVsbG8gd29ybGQh"
})
```