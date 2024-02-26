import uuid
import asyncio
import httpx
import json

from client import config


def get_client():
    return httpx.AsyncClient(
                timeout=config.CLIENT_TIMEOUT_SEC,
                limits=httpx.Limits(
                    max_connections=config.CLIENT_MAX_CONNECTIONS,
                    max_keepalive_connections=config.CLIENT_KEEPALIVE_CONNECTIONS
                )
        )


async def perform_rollback(response_list, request_type):
    print("Rolling back changes.")

    for success in response_list:
        print(f"Rolling back server: {success['url']}")
        if request_type == "create":
            await send_delete_request(success['url'], success['group_id'])
        elif request_type == "delete":
            await send_create_request(success['url'], success['group_id'])

    print("Rollback completed.")


async def send_create_request(url, group_id):
    async with get_client() as client:
        return await client.post(url, content=json.dumps({"groupId":group_id}))


async def send_delete_request(url, group_id):
    async with get_client() as client:
        return await client.request("DELETE", url, content=json.dumps({"groupId":group_id}))


async def create_or_delete_group_on_cluster(cluster_urls, group_id, type):
    print(f"{type.capitalize()} the group on the cluster.")

    success_responses = []
    to_rollback = False
    for index, url in enumerate(cluster_urls):
        try:
            print(f"Sending {type} request to: {url}")
            if type == "create":
                result = await send_create_request(url, group_id)
                if result.status_code == 201:
                    print("Successfully sent a create request")
                    success_responses.append({"url": url, "group_id": group_id})
                else:
                    to_rollback = True
            else:
                result = await send_delete_request(url, group_id)
                if result.status_code == 200:
                    print("Successfully sent a delete request")
                    success_responses.append({"url": url, "group_id": group_id})
                else:
                    to_rollback = True
            if to_rollback:
                print(f"Server responded with {result.status_code}, performing a rollback")
                await perform_rollback(success_responses, type)
                return False
        except Exception as e:
            print("Error: ", e)
            print(f"There was an error on the server: {url}. Performing a rollback")
            await perform_rollback(success_responses, type)

    return True


if __name__ == "__main__":
    action = input("Delete or create a group? Please enter d or c: ")
    group_id = input("Group ID: ")

    if action == "d":
        asyncio.run(create_or_delete_group_on_cluster(config.CLUSTER_URLS, group_id, "delete"))
    elif action == "c":
        asyncio.run(create_or_delete_group_on_cluster(config.CLUSTER_URLS, group_id, "create"))
    else:
        print("Bad input. Execution stopped.")
