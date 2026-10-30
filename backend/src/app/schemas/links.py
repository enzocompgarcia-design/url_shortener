from pydantic import BaseModel, ConfigDict


class CreatShortLinkRequest(BaseModel):
    long_link: str


class CreatShortLinkResponse(BaseModel):
    short_link: str

    model_config = ConfigDict()
