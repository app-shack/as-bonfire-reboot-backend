from dataclasses import dataclass, fields


@dataclass
class EmailSearchUserProfile:
    email: str
    image_original: str
    is_custom_image: bool
    first_name: str
    last_name: str
    phone: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)


@dataclass
class EmailSearchUser:
    profile: EmailSearchUserProfile

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.profile = EmailSearchUserProfile.from_kwargs(**self.profile)


@dataclass
class SearchEmailResponse:
    ok: str
    user: EmailSearchUser

    @classmethod
    def from_kwargs(cls, **kwargs):
        names = set([f.name for f in fields(cls)])
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
        return cls(**filtered_kwargs)

    def __post_init__(self):
        self.user = EmailSearchUser.from_kwargs(**self.user)
