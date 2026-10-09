"""Validação de entrada com Pydantic."""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class RecordInput(BaseModel):
    record_date: date
    campus: str = Field(min_length=1, max_length=80)
    indicator: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=120)
    series: Optional[str] = Field(default=None, max_length=40)
    status: str = Field(min_length=1, max_length=60)
    value: float = Field(ge=0, le=1_000_000_000)
    unit: str = Field(min_length=1, max_length=40)
    source: str = Field(default="", max_length=200)
    notes: str = Field(default="", max_length=2000)

    @field_validator("campus", "indicator", "category", "status", "unit")
    @classmethod
    def must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("Este campo é obrigatório.")
        return value.strip()

    @field_validator("value")
    @classmethod
    def finite_value(cls, value):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("Informe um número válido.")
        return value
