import vobiz

client = vobiz.RestClient()

resp = client.calls.create(
    from_="911171366943",
    to_="917348860185",
    answer_url="https://example.com/answer.xml",
)
print(resp)

live = client.calls.list_live()
print(live.__dict__)

queued = client.calls.list_queued()
print(queued.__dict__)

# If the API returns a 'calls' list, you can do:
# for call in live.calls:
#     print(call)


# client.calls.transfer(
#     call_uuid="CALL_UUID",
#     legs="both",
#     aleg_url="https://example.com/aleg.xml",
#     aleg_method="POST",
#     bleg_url="https://example.com/bleg.xml",
#     bleg_method="POST",
# )