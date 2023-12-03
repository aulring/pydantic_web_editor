from enum import Enum
from typing import List, Optional, Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, PositiveInt, TypeAdapter

from pydantic_web_editor import WebEditorConfig2, copy_static_folder, WebEditorConfig

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
copy_static_folder(copy_path="static")


class ResourceModel(BaseModel):
    pass


from typing import Union, List, Dict, Literal
from pydantic import BaseModel



class DefaultString(BaseModel):
    set_default_string: str = Field(
        None, description="Default variable if setting as a string"
    )


class DefaultInteger(BaseModel):
    set_default_integer: int = Field(
        None, description="Default variable if setting as an integer"
    )


class DefaultNumber(BaseModel):
    set_default_number: float = Field(
        None, description="Default variable if setting as a float/number"
    )


class AllowedString(BaseModel):
    set_allowed_strings: str = Field(
        None, description="Default variable if setting as a string"
    )


class AllowedInteger(BaseModel):
    set_allowed_integers: int = Field(
        None, description="Default variable if setting as an integer"
    )


class AllowedNumber(BaseModel):
    set_allowed_numbers: float = Field(
        None, description="Default variable if setting as a float/number"
    )


class KeyValuePair(BaseModel):
    key: str
    value: str

class Parameter(BaseModel):
    Type: Literal[
        "String",
        "Number",
        "List<Number>",
        "CommaDelimitedList",
        "AWS Specific Type",
        "SSM Parameter Types",
    ] = Field("String", description="Cloudformation Parameter Type")
    Default: Union[DefaultString, DefaultInteger, DefaultNumber] = Field(
        ..., description="Default Value for the parameter if not set.", 
    )
    Description: str = Field(None, description="Description to describe the parameter.")
    AllowedValues: Union[
        List[AllowedString], List[AllowedInteger], List[AllowedNumber]
    ] = Field(None, description="Values allowed to be passed as the paramter")
    ConstraintDescription: str = Field(
        None, description="Constraint to apply to the parameter."
    )
    MinLength: PositiveInt = Field(
        None, description="Constraint to apply to the parameter."
    )
    MaxLength: PositiveInt = Field(
        None, description="Constraint to apply to the parameter."
    )
    MinValue: int = Field(None, description="Constraint to apply to the parameter.")
    MaxValue: int = Field(None, description="Constraint to apply to the parameter.")
    NoEcho: bool = Field(None, description="Constraint to apply to the parameter.")
    AllowedPattern: str = Field(
        None, description="Constraint to apply to the parameter."
    )


class Base64InternalType(BaseModel):
    value_to_encode: str = Field(..., description="String to encode in base64")

    def to_dict(self) -> dict:
        return {"Fn::Base64": self.value_to_encode}

class CidrInternalType(BaseModel):
    ip_block: str = Field(..., description="The IP block to be split, e.g., '192.168.0.0/24'")
    count: int = Field(..., description="The number of CIDRs to generate")
    cidr_bits: Optional[int] = Field(None, description="The number of bits in the resulting CIDR mask")

    def to_dict(self) -> dict:
        cidr_values = [self.ip_block, self.count]
        if self.cidr_bits is not None:
            cidr_values.append(self.cidr_bits)
        return {"Fn::Cidr": cidr_values}

class FindInMapInternalType(BaseModel):
    map_name: Any
    top_level_key: Any
    second_level_key: Any
    default_value: Optional[Any] = None

    def to_dict(self) -> dict:
        find_in_map_details = [self.map_name, self.top_level_key, self.second_level_key]
        if self.default_value is not None:
            find_in_map_details.append({"DefaultValue": self.default_value})
        return {"Fn::FindInMap": find_in_map_details}

class GetAttInternalType(BaseModel):
    logical_name: str  # Resource name, usually a string
    attribute_name: str  # Attribute name of the resource, also a string

class GetAZsInternalType(BaseModel):
    region: str = Field(default="", description="The name of the region for which to get the Availability Zones")

    def to_dict(self) -> dict:
        return {"Fn::GetAZs": self.region}
    
class ImportValueInternalType(BaseModel):
    exported_name: str = Field(..., description="The name of the exported output from another stack")

    def to_dict(self) -> dict:
        return {"Fn::ImportValue": self.exported_name}
    
class JoinInternalType(BaseModel):
    delimeter: str = Field(
        "-", description="delimeter to join items by"
    )
    items: List[str]


class SelectInternalType(BaseModel):
    index: int = Field(..., description="The index of the item to retrieve")
    objects: List[Union[str, int, float]] = Field(..., description="The list of objects to select from")

    def to_dict(self) -> dict:
        return {"Fn::Select": [self.index, self.objects]}

class SplitInternalType(BaseModel):
    delimiter: str = Field(..., description="The delimiter to split the string by")
    source_string: str = Field(..., description="The string to be split")

    def to_dict(self) -> dict:
        return {"Fn::Split": [self.delimiter, self.source_string]}
    
class SubInternalType(BaseModel):
    input_str: str = Field(..., description="The string with variables to substitute")
    variables: Dict[str, Union[str, int, float]] = Field(default={}, description="Mapping of variables to their substitution values")

    def to_dict(self) -> dict:
        return {"Fn::Sub": [self.input_str, self.variables] if self.variables else self.input_str}

class TransformInternalType(BaseModel):
    name: str = Field(..., description="The name of the macro to use for transformation")
    parameters: Dict[str, str] = Field(default_factory=dict, description="Parameters to pass to the macro")

    def to_dict(self) -> dict:
        return {"Fn::Transform": {"Name": self.name, "Parameters": self.parameters}}

class RefInternalType(BaseModel):
    resource_or_parameter_name: str = Field(..., description="The name of the resource or parameter to reference.")

    def to_dict(self) -> dict:
        return {"Ref": self.resource_or_parameter_name}


##################################################################################################

class Base64(BaseModel):
    value_to_encode: str = Field(..., description="String to encode in base64")

    def to_dict(self) -> dict:
        return {"Fn::Base64": self.value_to_encode}

class Cidr(BaseModel):
    ip_block: str = Field(..., description="The IP block to be split, e.g., '192.168.0.0/24'")
    count: int = Field(..., description="The number of CIDRs to generate")
    cidr_bits: Optional[int] = Field(None, description="The number of bits in the resulting CIDR mask")

    def to_dict(self) -> dict:
        cidr_values = [self.ip_block, self.count]
        if self.cidr_bits is not None:
            cidr_values.append(self.cidr_bits)
        return {"Fn::Cidr": cidr_values}

class FindInMap(BaseModel):
    map_name: Any
    top_level_key: Any
    second_level_key: Any
    default_value: Optional[Any] = None

    def to_dict(self) -> dict:
        find_in_map_details = [self.map_name, self.top_level_key, self.second_level_key]
        if self.default_value is not None:
            find_in_map_details.append({"DefaultValue": self.default_value})
        return {"Fn::FindInMap": find_in_map_details}

class GetAtt(BaseModel):
    logical_name: str  # Resource name, usually a string
    attribute_name: str  # Attribute name of the resource, also a string

class GetAZs(BaseModel):
    region: str = Field(default="", description="The name of the region for which to get the Availability Zones")

    def to_dict(self) -> dict:
        return {"Fn::GetAZs": self.region}
    
class ImportValue(BaseModel):
    exported_name: str = Field(..., description="The name of the exported output from another stack")

    def to_dict(self) -> dict:
        return {"Fn::ImportValue": self.exported_name}
    
class Join(BaseModel):
    delimeter: str = Field(
        "-", description="delimeter to join items by"
    )
    items: List[str]


class Select(BaseModel):
    index: int = Field(..., description="The index of the item to retrieve")
    objects: List[Union[str, int, float]] = Field(..., description="The list of objects to select from")

    def to_dict(self) -> dict:
        return {"Fn::Select": [self.index, self.objects]}

class Split(BaseModel):
    delimiter: str = Field(..., description="The delimiter to split the string by")
    source_string: str = Field(..., description="The string to be split")

    def to_dict(self) -> dict:
        return {"Fn::Split": [self.delimiter, self.source_string]}
    
class Sub(BaseModel):
    input_str: str = Field(..., description="The string with variables to substitute")
    variables: Dict[str, Union[str, int, float]] = Field(default={}, description="Mapping of variables to their substitution values")

    def to_dict(self) -> dict:
        return {"Fn::Sub": [self.input_str, self.variables] if self.variables else self.input_str}

class Transform(BaseModel):
    name: str = Field(..., description="The name of the macro to use for transformation")
    parameters: Dict[str, str] = Field(default_factory=dict, description="Parameters to pass to the macro")

    def to_dict(self) -> dict:
        return {"Fn::Transform": {"Name": self.name, "Parameters": self.parameters}}

class Ref(BaseModel):
    resource_or_parameter_name: str = Field(..., description="The name of the resource or parameter to reference.")

    def to_dict(self) -> dict:
        return {"Ref": self.resource_or_parameter_name}


# Define the base classes for the conditional functions
class Equals(BaseModel):
    value_one: Any = Field(..., description="The first value for comparison.")
    value_two: Any = Field(..., description="The second value for comparison.")

    def to_dict(self) -> dict:
        return {"Fn::Equals": [self.value_one, self.value_two]}

class If(BaseModel):
    condition: str = Field(..., description="A reference to a condition in the Conditions section.")
    true_value: Union[str, Ref] = Field(..., description="Value to return if the condition is true.")
    false_value: Union[str, Ref] = Field(..., description="Value to return if the condition is false.")

    def to_dict(self) -> dict:
        return {"Fn::If": [self.condition, self.true_value, self.false_value]}

class Not(BaseModel):
    condition: Any = Field(..., description="A condition that evaluates to true or false.")

    def to_dict(self) -> dict:
        return {"Fn::Not": [self.condition]}

class Or(BaseModel):
    conditions: List[Any] = Field(..., description="A list of conditions that evaluate to true or false.")

    def to_dict(self) -> dict:
        return {"Fn::Or": self.conditions}

# Define a union of condition types for the And class
ConditionType = Union[Equals, If, Not, Or]

class And(BaseModel):
    conditions: List[ConditionType] = Field(..., description="A list of condition objects.")

    def to_dict(self) -> dict:
        return {"Fn::And": [condition.model_dump() for condition in self.conditions]}



class MappingKey(BaseModel):
    """YEYE"""

    key: Union[str, Join, Transform]
    mapping: List[KeyValuePair]


class Mappings(BaseModel):
    mappings: List[MappingKey]


# class Mapping(BaseModel):
#     # Example: {"RegionMap": {"us-east-1": {"HVM64": "ami-0ff8a91507f77f867"}}}
#     Mapping: Dict[str, Dict[str, Union[str, int]]] = None

# class Output(BaseModel):
#     Description: str = None
#     Value: Union[str, Dict[str, Union[str, int, List[Union[str, int]]]]]
#     Export: Dict[str, str] = None

# class CloudFormationTemplate(BaseModel):
#     AWSTemplateFormatVersion: Literal['2010-09-09'] = '2010-09-09'
#     Description: str = None
#     Resources: Dict[str, ResourceModel]  # Resources will be defined in detail elsewhere
#     Parameters: Dict[str, Parameter] = None
#     Mappings: Dict[str, Mapping] = None
#     Outputs: Dict[str, Output] = None

#     class Config:
#         extra = 'allow'  # Allows for additional fields not defined in the model


class ParameterKey(BaseModel):
    key: str = Field(..., description="Template key for the parameter")
    parameter: Parameter = Field(None, description="Parameter to be defined")


class Parameters(BaseModel):
    parameters: List[ParameterKey] = Field(
        ...,
        description="List of Cloudformation Parameters template will use",
    )


class TestEnum(Enum):
    test = "HI"
    there = "THERE"

class Template(BaseModel):
    parameters: Parameters
    mappings: Mappings
    test: Dict[TestEnum, MappingKey]

@app.get("/")
def hello():
    web_editor_config = WebEditorConfig(
        title="Example Pydantic Editor demoing Schema Org's About Page",
        model=Template,
        #gen_ui_schema=True
    )
    return HTMLResponse(web_editor_config.html)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
