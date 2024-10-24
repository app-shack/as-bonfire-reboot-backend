from dataclasses import dataclass, fields
from typing import Optional


class BaseResponse:
    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)


@dataclass
class EmailSearchUserProfile(BaseResponse):
    email: str
    first_name: str
    last_name: str
    phone: str

    image_original: Optional[str] = None
    is_custom_image: Optional[bool] = None


@dataclass
class EmailSearchUser(BaseResponse):
    id: str
    profile: EmailSearchUserProfile

    def __post_init__(self):
        self.profile = EmailSearchUserProfile.from_kwargs(**self.profile)


@dataclass
class SearchEmailResponse(BaseResponse):
    ok: str
    user: EmailSearchUser

    def __post_init__(self):
        self.user = EmailSearchUser.from_kwargs(**self.user)
