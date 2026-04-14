from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class TipoMidia(str, Enum):
    FISICA = "💿 Física"
    DIGITAL = "🎮 Digital"
    PS_PLUS = "⭐ PS Plus"

class StatusJogo(str, Enum):
    NAO_INICIADO = "📦 Não iniciado"
    JOGANDO = "🎯 Jogando"
    COMPLETO = "🏆 Completo"
    PLATINADO = "✨ Platinado"
    ABANDONADO = "😴 Abandonado"

class JogoBase(BaseModel):
   
    
    nome: str = Field(..., min_length=2, max_length=100)
    plataforma: str = Field(..., pattern="^(PS4|PS5)$")
    tipo_midia: TipoMidia
    valor_pago: float = Field(..., ge=0)
    
    status: StatusJogo = Field(default=StatusJogo.NAO_INICIADO)
    horas_jogadas: Optional[float] = Field(default=0, ge=0)
    
    @field_validator('plataforma')
    def validar_plataforma(cls, v):
        if v.upper() not in ['PS4', 'PS5']:
            raise ValueError('Plataforma deve ser PS4 ou PS5')
        return v.upper()
    
    @field_validator('valor_pago')
    def validar_valor(cls, v):
        return round(v, 2)

class JogoResponse(JogoBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True