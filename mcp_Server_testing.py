from fastmcp import FastMCP
import anyio
from typing import Annotated
from pydantic import Field
from fastmcp.utilities.types import Image, Audio, File
from fastmcp.resources import FileResource, TextResource, DirectoryResource
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent


app = FastMCP(name="testing_mcp",strict_input_validation=True,on_duplicate_prompts="error"  )# Raise an error if a prompt name is duplicated(warn,replace,ignore)

@app.tool(name="greetings",
          description="greets a user when name is provided",
          tags=["hello","greetings","hi"],
          metadata={"version":"1.0"},
          enabled=True)
def greetings(name: str):
    return "hello,{}".format(name)

#Simple Function
def sub_functions(a,b):
    return a - b


@app.tool()
async def sub(a: int, b: int):  # a:Annotated[int,Field(10,description="1st number")]
    return await anyio.to_thread.run_sync(sub_functions, a, b)


@app.resource("resources://text_display")
def text_display():
    return "hello,this is my first mcp program"
    #return {"name":"sneha","age":21}


@app.resource(name="Application Status",
              url="resources://app_status",
              description="used to find status of app",
              mime_type="application/json",
              tags=["status","app"],
              metadata={"version":"1.0"},
              enabled=True)
#@app.resource("resource://{name}/details")
def get_application_status(name):
    """Internal function description ignored if description is provided above."""
    return {"status": "ok", "uptime": 12345}


#resources can be files,images,audio etc.
#for files
readme_resource = FileResource(
        uri=f"file://path",
        path=readme_path, # Path to the actual file
        name="README File",
        description="The project's README.",
        mime_type="text/markdown",
        tags={"documentation"},
        annotations={
        "readOnlyHint": True,
        "idempotentHint": True
        }
    )
app.add_resource(readme_resource)
app.delete_resource(readme_resource)
app.enabled(readme_resource)
app.disables(readme_resource)

#for text
notice_resource = TextResource(
    uri="resource://notice",
    name="Important Notice",
    text="System maintenance scheduled for Sunday.",
    tags={"notification"}
)
app.add_resource(notice_resource)

#directory as resource
data_listing_resource = DirectoryResource(
        uri="resource://data-files",
        path=data_dir_path, # Path to the directory
        name="Data Directory Listing",
        description="Lists files available in the data directory.",
        recursive=False # Set to True to list subdirectories
    )
app.add_resource(data_listing_resource)



@app.prompt(
    name="analyze_data_request",          # Custom prompt name
    description="Creates a request to analyze data with specific parameters",  # Custom description
    tags={"analysis", "data"},            # Optional categorization tags
    meta={"version": "1.1", "author": "data-team"} ,# Custom metadata
    enabled=True
)
def code_in_language(language,task):
    prompt_content=f"write a {language} code for {task}"
    return PromptMessage(content=TextContent(text=prompt_content,type="text"),role="user")
    


if __name__ == "__main__":
    app.run(transport="streamable-http", host="0.0.0.0", port=8000)
