from hostfact_client import HostFact

client = HostFact(url="https://cptest1.nextpertise.nl/Pro/apiv2/api.php", api_key="m3q17L1js3056N8d9Io384h")

# print (client.debtor.list(searchfor='DB100@nextpertise.nl', searchat='EmailAddress'))

# res = client.invoice.add(**{
#     "DebtorCode": "DB100",
#     "InvoiceLines": [
#         {
#             "Description": "Setupfee",
#             "PriceExcl": 150
#         },
#         {
#             "ProductCode": "P003",
#             "Description": "Domain example.com"
#         }
#     ]
# })


res = client.invoice.make_invoice(**{
    "debtor_code": "DB100",
    "invoice_lines": [
        {
            "Description": "Edit test",
            "PriceExcl": 999
        },
        {
            "ProductCode": "P008",
            "Description": "Test edit.example.com"
        }
    ],
    "attachment": {
        "name": "test2.txt",
        "content": "SGVsbG8gd29ybGQh"
    }
})


# client.attachment.add(**{
#     "InvoiceCode": "[concept]0003",
#     "Type": "invoice",
#     "filename": "test.txt",
#     "base64": "SGVsbG8gd29ybGQh"
# })