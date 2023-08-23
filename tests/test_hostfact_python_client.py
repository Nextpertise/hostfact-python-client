import vcr
import base64
import pytest
import httpx
import respx
from hostfact_python_client.utilities import http_build_query
from hostfact_python_client.hostfact_client import HostFact


class HTTPXTransport:
    @staticmethod
    def request(url: str, data: str, headers: dict = None, timeout: int = 30):
        # Use httpx.request to send the request
        response = httpx.request("POST", url, data=data, headers=headers, timeout=timeout)

        # Return the response
        return response


# Set up the mocked transport
transport = HTTPXTransport()

# Clients
transport_client = HostFact(url="https://your-hostfact-server.com/Pro/apiv2/api.php",
                            api_key="secret", transport=transport)
transport_client_invalid_api_key = HostFact(url="https://your-hostfact-server.com/Pro/apiv2/api.php",
                                            api_key="wrong_secret", transport=transport)
native_client = HostFact(url="https://your-hostfact-server.com/Pro/apiv2/api.php", api_key="secret")
native_client_invalid_api_key = HostFact(url="https://your-hostfact-server.com/Pro/apiv2/api.php",
                                         api_key="wrong_secret")


def test_invoice_list_http_build_query():
    result = http_build_query({
        "action": "list",
        "controller": "invoice",
        "sort": "Modified"
    })

    assert (result == "action=list&controller=invoice&sort=Modified")


@pytest.mark.parametrize("client", [native_client, transport_client])
@vcr.use_cassette('tests/vcr_cassettes/invoice.list.yaml')
def test_invoice_list_http_request(client):
    result = client.invoice.list()

    assert (result == {
        "controller": "invoice",
        "action": "list",
        "status": "success",
        "date": "2021-06-18T14:23:45+02:00",
        "totalresults": 3,
        "currentresults": 3,
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


@pytest.mark.parametrize("client", [native_client, transport_client])
@vcr.use_cassette('tests/vcr_cassettes/invoice.make_invoice.yaml')
def test_make_invoice_http_request(client):

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


@pytest.mark.parametrize("client", [native_client_invalid_api_key, transport_client_invalid_api_key])
@vcr.use_cassette('tests/vcr_cassettes/failed_invoice.list.yaml')
def test_with_incorrect_api_key_http_request(client):
    with pytest.raises(Exception) as exc_info:
        client.invoice.list()
    assert str(exc_info.value) == "HostFact error: ['API key is invalid']"


@pytest.mark.parametrize("client", [native_client_invalid_api_key, transport_client_invalid_api_key])
def test_timeout_in_http_request(client):
    # Mock the request to timeout
    respx.get("https://your-hostfact-server.com/").mock(side_effect=httpx.TimeoutException("Mocked timeout"))

    with pytest.raises(Exception) as exc_info:
        client.invoice.list()
    assert str(exc_info.value) == "HostFact error: [Errno 8] nodename nor servname provided, or not known"
