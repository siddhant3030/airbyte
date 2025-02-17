#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from decimal import Decimal
from typing import Any, Dict, Iterable, Type

from pydantic import BaseModel, create_model


class CatalogModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

        @classmethod
        def schema_extra(cls, schema: Dict[str, Any], model: Type["BaseModel"]) -> None:
            # Modify pydantic generated jsonschema.
            # Remove "title" and "description" fields to reduce size.
            schema.pop("title", None)
            schema.pop("description", None)
            # Remove required section so any missing attribute from API wont break object validation.
            schema.pop("required", None)
            # According to https://github.com/airbytehq/airbyte/issues/14196 set additionalProperties to True
            if schema.pop("additionalProperties", None):
                schema["additionalProperties"] = True
            for name, prop in schema.get("properties", {}).items():
                prop.pop("title", None)
                prop.pop("description", None)
                if prop.pop("additionalProperties", None):
                    prop["additionalProperties"] = True
                allow_none = model.__fields__[name].allow_none
                # Pydantic doesnt treat Union[None, Any] type correctly when
                # generation jsonschema so we cant set field as nullable (i.e.
                # field that can have either null and non-null values),
                # generate this jsonschema value manually.
                if "type" in prop:
                    if allow_none:
                        prop["type"] = ["null", prop["type"]]


class MetricsReport(CatalogModel):
    profileId: int
    recordType: str
    reportDate: str
    recordId: str
    # This property will be overwritten with autogenerated model based on metrics list
    metric: None

    @classmethod
    def generate_metric_model(cls, metric_list: Iterable[str]) -> CatalogModel:
        metrics_obj_model = create_model("MetricObjModel", **{f: (str, None) for f in metric_list}, __base__=CatalogModel)
        return create_model("MetricsModel", metric=(metrics_obj_model, None), __base__=cls)


class Targeting(CatalogModel):
    targetId: Decimal
    adGroupId: Decimal
    state: str
    expressionType: str
    bid: Decimal


class KeywordsBase(CatalogModel):
    keywordId: Decimal
    campaignId: Decimal
    adGroupId: Decimal
    state: str
    keywordText: str


class Keywords(KeywordsBase):
    nativeLanguageKeyword: str
    matchType: str
    bid: Decimal


class NegativeKeywords(KeywordsBase):
    matchType: str
