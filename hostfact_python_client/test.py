from hostfact_client import HostFact

client = HostFact(url="https://cptest1.nextpertise.nl/Pro/apiv2/api.php", api_key="m3q17L1js3056N8d9Io384h")


print ("#################### ACTION/CONTROLLER #################")
print (client.call(action='list', controller='debtor', searchfor='DB100@nextpertise.nl', searchat='EmailAddress'))



print ("#################### CLASS LOGIC #################")
print (client.debtor.debtors_list(searchfor='DB100@nextpertise.nl', searchat='EmailAddress'))
