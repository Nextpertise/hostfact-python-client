import vcr
import base64

from hostfact_python_client.utilities import http_build_query

from hostfact_python_client.hostfact_client import HostFact


client = HostFact(url="https://localhost/api.php", api_key="secret")


def test_invoice_list_http_build_query():
    result = http_build_query({
        "action": "list",
        "controller": "invoice",
        "sort": "Modified"
    })

    assert (result == "action=list&controller=invoice&sort=Modified")

@vcr.use_cassette('vcr_cassettes/invoice.list.yaml')
def test_invoice_list_http_request():
    
    result = client.invoice.list()

    assert (result == {
        "controller": "invoice",
        "action": "list",
        "status": "success",
        "date": "2021-06-18T14:23:45+02:00",
        "totalresults": 9,
        "currentresults": 9,
        "offset": 0,
        "invoices": [
            {
                "Identifier": "9297",
                "InvoiceCode": "[concept]0009",
                "Debtor": "1",
                "DebtorCode": "DB100",
                "CompanyName": "DB100",
                "Initials": "D.",
                "SurName": "Code",
                "AmountExcl": "4444.00",
                "AmountIncl": "5377.24",
                "AmountOpen": 0,
                "Date": "2021-06-18",
                "Status": "0",
                "SubStatus": "",
                "Authorisation": "no",
                "Modified": "2021-06-18 13:13:19"
            },
            {
                "Identifier": "9296",
                "InvoiceCode": "[concept]0008",
                "Debtor": "1",
                "DebtorCode": "DB100",
                "CompanyName": "DB100",
                "Initials": "D.",
                "SurName": "Code",
                "AmountExcl": "1111.00",
                "AmountIncl": "1344.31",
                "AmountOpen": 0,
                "Date": "2021-06-18",
                "Status": "0",
                "SubStatus": "",
                "Authorisation": "no",
                "Modified": "2021-06-18 12:53:40"
            },
            {
                "Identifier": "9295",
                "InvoiceCode": "[concept]0007",
                "Debtor": "1",
                "DebtorCode": "DB100",
                "CompanyName": "DB100",
                "Initials": "D.",
                "SurName": "Code",
                "AmountExcl": "16433.00",
                "AmountIncl": "19883.93",
                "AmountOpen": 0,
                "Date": "2021-06-17",
                "Status": "0",
                "SubStatus": "",
                "Authorisation": "no",
                "Modified": "2021-06-18 12:39:03"
            }
        ]
    })


@vcr.use_cassette('vcr_cassettes/invoice.make_invoice.yaml')
def test_make_invoice_http_request():

    filename = "test.txt"
    attachment = base64.b64encode("Hello world".encode())
    
    result = client.invoice.make_invoice(**{
        "debtor_code": "DB100",
        "invoice_lines": [
            {
                "Description": "test@test.nl",
                "PriceExcl": 2222
            }
        ],
        "newInvoice": True,
        "attachment": {
            "name": filename,
            "content": attachment
        }
    })

    assert (result == {'Identifier': '9300'})

    invoice = client.invoice.show(Identifier=result['Identifier'])['invoice']

    assert (invoice["Attachments"] == [
        {
        "Identifier": "49",
        "Filename": "test.txt"
        }
    ])
    assert (invoice["InvoiceLines"] == [
        {
        "Identifier": 318661,
        "Date": "2021-06-18",
        "Number": "1",
        "NumberSuffix": "",
        "ProductCode": "",
        "Description": "test@test.nl",
        "PriceExcl": "2222",
        "DiscountPercentage": 0,
        "DiscountPercentageType": "line",
        "TaxPercentage": 21,
        "PeriodicID": "0",
        "Periods": "1",
        "Periodic": "",
        "StartPeriod": "",
        "EndPeriod": "",
        "ProductType": "",
        "Reference": "0",
        "NoDiscountAmountIncl": 2688.62,
        "NoDiscountAmountExcl": 2222,
        "DiscountAmountIncl": 0,
        "DiscountAmountExcl": 0
        }
    ])


    result = client.invoice.make_invoice(**{
        "debtor_code": "DB100",
        "invoice_lines": [
            {
                "Description": "Big money",
                "PriceExcl": 5000
            }
        ]
    })

    invoice = client.invoice.show(Identifier=result['Identifier'])['invoice']

    assert (invoice["Attachments"] == [
        {
        "Identifier": "49",
        "Filename": "test.txt"
        }
    ])
    assert (invoice["InvoiceLines"] == [
        {
            "Identifier": 318661,
            "Date": "2021-06-18",
            "Number": "1",
            "NumberSuffix": "",
            "ProductCode": "",
            "Description": "test@test.nl",
            "PriceExcl": "2222",
            "DiscountPercentage": 0,
            "DiscountPercentageType": "line",
            "TaxPercentage": 21,
            "PeriodicID": "0",
            "Periods": "1",
            "Periodic": "",
            "StartPeriod": "",
            "EndPeriod": "",
            "ProductType": "",
            "Reference": "0",
            "NoDiscountAmountIncl": 2688.62,
            "NoDiscountAmountExcl": 2222,
            "DiscountAmountIncl": 0,
            "DiscountAmountExcl": 0
        },
        {
            "Identifier": 318662,
            "Date": "2021-06-18",
            "Number": "1",
            "NumberSuffix": "",
            "ProductCode": "",
            "Description": "Big money",
            "PriceExcl": "5000",
            "DiscountPercentage": 0,
            "DiscountPercentageType": "line",
            "TaxPercentage": 21,
            "PeriodicID": "0",
            "Periods": "1",
            "Periodic": "",
            "StartPeriod": "",
            "EndPeriod": "",
            "ProductType": "",
            "Reference": "0",
            "NoDiscountAmountIncl": 6050,
            "NoDiscountAmountExcl": 5000,
            "DiscountAmountIncl": 0,
            "DiscountAmountExcl": 0
        }
    ])
    