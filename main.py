import os
import asyncio
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator

from llm_service import llm_service

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="小六壬占卜 API",
    description="基于 Gemini API 的小六壬占卜服务",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DivinationRequest(BaseModel):
    """占卜请求模型"""
    wish: str
    numbers: List[int]
    language: Optional[str] = None
    
    @validator('wish')
    def validate_wish(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('愿望内容不能为空且至少包含2个字符')
        if len(v) > 200:
            raise ValueError('愿望内容不能超过200个字符')
        return v.strip()
    
    @validator('numbers')
    def validate_numbers(cls, v):
        if len(v) != 3:
            raise ValueError('必须提供恰好3个数字')
        for num in v:
            if not isinstance(num, int) or num < 1 or num > 99:
                raise ValueError('数字必须是1-99之间的整数')
        return v


class DivinationResponse(BaseModel):
    """占卜响应模型"""
    success: bool
    divination: Optional[str] = None
    prediction: Optional[str] = None
    advice: Optional[str] = None
    luck: Optional[int] = None
    # 新增：大吉/中吉... 文本
    luck_text: Optional[str] = None
    # 新增：三宫（人/事/应）六神结构化信息
    # name: 中文六神名；pinyin: 英文拼音（小写空格分隔）；element: 五行；position: ren/shi/ying
    palaces: Optional[list] = None
    full_text: Optional[str] = None
    error: Optional[str] = None


class DailyFortuneResponse(BaseModel):
    """每日运势响应模型"""
    success: bool
    fortune: Optional[str] = None
    date: Optional[str] = None
    lunar_date: Optional[str] = None
    error: Optional[str] = None


class IncenseRequest(BaseModel):
    """上香请求模型"""
    wish: str
    incense_type: str  # 香的类型：basic, premium, luxury
    
    @validator('wish')
    def validate_wish(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('愿望内容不能为空且至少包含2个字符')
        if len(v) > 200:
            raise ValueError('愿望内容不能超过200个字符')
        return v.strip()
    
    @validator('incense_type')
    def validate_incense_type(cls, v):
        if v not in ['basic', 'premium', 'luxury']:
            raise ValueError('香的类型必须是 basic, premium, luxury 之一')
        return v


class IncenseResponse(BaseModel):
    """上香响应模型"""
    success: bool
    blessing: Optional[str] = None
    merit_points: Optional[int] = None
    incense_count: Optional[int] = None
    error: Optional[str] = None


class ShopItem(BaseModel):
    """商品模型"""
    id: int
    name: str
    description: str
    price: int  # 使用积分作为价格单位
    category: str
    in_stock: bool
    image_url: Optional[str] = None


class ShopResponse(BaseModel):
    """商城响应模型"""
    success: bool
    items: Optional[List[ShopItem]] = None
    error: Optional[str] = None


class PurchaseRequest(BaseModel):
    """购买请求模型"""
    item_id: int
    quantity: int = 1
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v < 1 or v > 10:
            raise ValueError('购买数量必须在1-10之间')
        return v


class PurchaseResponse(BaseModel):
    """购买响应模型"""
    success: bool
    message: Optional[str] = None
    remaining_points: Optional[int] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "小六壬占卜 API 服务",
        "version": "1.0.0",
        "endpoints": {
            "占卜": "/api/divination",
            "每日运势": "/api/daily-fortune",
            "上香": "/api/incense",
            "商城": "/api/shop",
            "购买": "/api/purchase",
            "API文档": "/docs"
        }
    }


@app.post("/api/divination", response_model=DivinationResponse)
async def perform_divination(request: DivinationRequest, http_request: Request):
    """
    执行小六壬占卜
    
    - **wish**: 您的愿望或要占卜的事情
    - **numbers**: 三个1-99之间的数字
    """
    try:
        # 语言优先级：body.language > Accept-Language header > zh
        lang = (request.language or 
                http_request.headers.get('Accept-Language', '') or 
                'zh').lower()
        lang = 'en' if lang.startswith('en') else 'zh'
        result = await llm_service.perform_divination(request.wish, request.numbers, language=lang)
        return DivinationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"占卜服务异常: {str(e)}")


@app.get("/api/daily-fortune", response_model=DailyFortuneResponse)
async def get_daily_fortune(date: Optional[str] = None):
    """
    获取每日运势
    
    - **date**: 可选，指定日期（格式：YYYY-MM-DD），不提供则使用当前日期
    """
    try:
        target_date = None
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD 格式")
        
        result = await llm_service.get_daily_fortune(target_date)
        return DailyFortuneResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取运势服务异常: {str(e)}")


# 模拟用户数据存储（在实际应用中应使用数据库）
user_data = {
    "incense_count": 0,
    "merit_points": 100,  # 初始功德值
}

# 商品数据
shop_items = [
    ShopItem(id=1, name="平安符", description="保佑平安健康", price=50, category="护身符", in_stock=True),
    ShopItem(id=2, name="招财符", description="招财进宝", price=80, category="护身符", in_stock=True),
    ShopItem(id=3, name="学业符", description="学业进步", price=60, category="护身符", in_stock=True),
    ShopItem(id=4, name="姻缘符", description="促进姻缘", price=70, category="护身符", in_stock=True),
    ShopItem(id=5, name="檀香", description="高品质檀香", price=30, category="香品", in_stock=True),
    ShopItem(id=6, name="沉香", description="珍贵沉香", price=100, category="香品", in_stock=True),
]


@app.post("/api/incense", response_model=IncenseResponse)
async def offer_incense(request: IncenseRequest):
    """
    上香祈福
    
    - **wish**: 祈愿内容
    - **incense_type**: 香的类型 (basic/premium/luxury)
    """
    try:
        # 根据香的类型获得不同的功德值
        merit_rewards = {"basic": 10, "premium": 20, "luxury": 30}
        merit_points = merit_rewards[request.incense_type]
        
        # 更新用户数据
        user_data["incense_count"] += 1
        user_data["merit_points"] += merit_points
        
        # 生成祝福语
        blessings = [
            f"愿您的心愿「{request.wish}」早日实现，诸事顺遂！",
            f"香火缭绕，诚心祈愿「{request.wish}」，愿得佛祖庇佑！",
            f"虔诚上香，祈求「{request.wish}」心想事成，福慧双增！",
            f"香烟袅袅，愿「{request.wish}」如愿以偿，功德无量！"
        ]
        
        blessing = blessings[user_data["incense_count"] % len(blessings)]
        
        return IncenseResponse(
            success=True,
            blessing=blessing,
            merit_points=merit_points,
            incense_count=user_data["incense_count"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上香服务异常: {str(e)}")


@app.get("/api/shop", response_model=ShopResponse)
async def get_shop_items(category: Optional[str] = None):
    """
    获取商城商品列表
    
    - **category**: 可选，商品分类筛选
    """
    try:
        items = shop_items
        if category:
            items = [item for item in shop_items if item.category == category]
        
        return ShopResponse(success=True, items=items)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"商城服务异常: {str(e)}")


@app.post("/api/purchase", response_model=PurchaseResponse)
async def purchase_item(request: PurchaseRequest):
    """
    购买商品
    
    - **item_id**: 商品ID
    - **quantity**: 购买数量
    """
    try:
        # 查找商品
        item = next((item for item in shop_items if item.id == request.item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="商品不存在")
        
        if not item.in_stock:
            raise HTTPException(status_code=400, detail="商品已售罄")
        
        total_price = item.price * request.quantity
        
        if user_data["merit_points"] < total_price:
            raise HTTPException(status_code=400, detail="功德值不足")
        
        # 扣除功德值
        user_data["merit_points"] -= total_price
        
        return PurchaseResponse(
            success=True,
            message=f"成功购买 {request.quantity} 个 {item.name}",
            remaining_points=user_data["merit_points"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"购买服务异常: {str(e)}")


@app.get("/api/user/status")
async def get_user_status():
    """获取用户状态"""
    return {
        "success": True,
        "incense_count": user_data["incense_count"],
        "merit_points": user_data["merit_points"]
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": bool(os.getenv('GEMINI_API_KEY'))
    }

@app.get("/api/debug/env")
async def debug_env():
    """调试环境变量（仅用于排查问题）"""
    api_key = os.getenv('GEMINI_API_KEY', '')
    all_env_keys = list(os.environ.keys())
    gemini_keys = [k for k in all_env_keys if 'GEMINI' in k.upper()]
    
    return {
        "env_vars_count": len(all_env_keys),
        "gemini_related_keys": gemini_keys,
        "api_key_exists": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "api_key_prefix": api_key[:10] + "..." if len(api_key) > 10 else api_key,
        "is_render": os.getenv('RENDER') == 'true',
        "render_url": os.getenv('RENDER_EXTERNAL_URL', 'not_set')
    }


if __name__ == "__main__":
    import uvicorn
    host = os.getenv('SERVER_HOST', '127.0.0.1')
    port = int(os.getenv('SERVER_PORT', 8000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🔮 小六壬占卜服务启动中...")
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"📚 API 文档: http://{host}:{port}/docs")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
