from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class DMAnalyse(BaseModel):
    """
    本次实训的最终得分、本次实训的分析list
    基于本次实训和用户画像给与的建议list
    """
    score: float = Field(description="本次实训的最终得分", ge=0, le=100)
    analyses: List[str] = Field(description="本次实训的分析list", min_items=1, max_items=5)
    recommends: List[str] = Field(description="基于本次实训和用户画像给与的建议list", min_items=1, max_items=5)