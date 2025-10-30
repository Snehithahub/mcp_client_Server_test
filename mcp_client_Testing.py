from fastmcp import Client
import asyncio

# async def dev():
#     async with Client("http://localhost:8000/mcp", "client1") as client:
#         response = await client.call_tool("greetings", {"name": "sony"})
#         try:
#             print(response.content[0].text)
#         except Exception:
#             print(response)


async def dev_tool_resource_prompt():
    async with Client("http://localhost:8000/mcp", "client1") as client:
        print("\n🧰 TOOLS TEST:")
        # --- Tool 1: greetings
        resp1 = await client.call_tool("greetings", {"name": "sony"})
        print("greetings →", resp1.content[0].text)

        # --- Tool 2: sub
        resp2 = await client.call_tool("sub", {"a": 10, "b": 4})
        print("sub →", resp2.content[0].text)

        print("\n📚 RESOURCES TEST:")
        # --- Resource 1: text_display
        text_res = await client.get_resource("resources://text_display")
        print("text_display →", text_res)

        # --- Resource 2: Application Status
        status_res = await client.get_resource("resources://app_status")
        print("app_status →", status_res)

        print("\n💬 PROMPTS TEST:")
        # --- Prompt: analyze_data_request
        prompt_res = await client.call_prompt(
            "analyze_data_request",
            {"language": "python", "task": "find factorial"}
        )
        for msg in prompt_res.messages:
            print(f"{msg.role} → {msg.content[0].text}")



asyncio.run(dev_tool_resource_prompt())
