#!/usr/bin/env python3
"""
创建示例新闻数据的脚本
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import sessionmaker
from backend.app.database.database import engine
from backend.app.models.user import User
from backend.app.models.news import News
from backend.app.core.security import get_password_hash

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 示例新闻数据
sample_news = [
    {
        "title": "🎵 全新音乐节即将开幕",
        "description": "本月底将在市中心举办为期三天的音乐节，汇聚国内外知名艺术家。从古典音乐到现代流行，从民族音乐到电子音乐，各种风格应有尽有。门票现已开售，早鸟优惠仅限前1000名购买者。",
        "image_url": "https://images.unsplash.com/photo-1459749187778-3663c29ab4b3?w=500",
        "creator": "admin"
    },
    {
        "title": "🎸 摇滚传奇乐队重聚演出",
        "description": "经典摇滚乐队《雷霆之声》时隔十年再次重聚，将在下个月举办全国巡回演唱会。乐队成员表示这次重聚是为了致敬那些陪伴他们成长的歌迷，演出将包含历年来的经典曲目以及全新创作。",
        "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500",
        "creator": "admin"
    },
    {
        "title": "🎹 青年钢琴家获国际大奖",
        "description": "来自本地音乐学院的22岁钢琴家李小华在国际肖邦钢琴比赛中获得金奖，成为该比赛历史上最年轻的获奖者。她的演奏被评委们称赞为《技巧与情感的完美结合》，展现了新一代音乐家的卓越才华。",
        "image_url": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500",
        "creator": "musiclover"
    },
    {
        "title": "🎤 说唱文化节引燃全城",
        "description": "首届城市说唱文化节吸引了超过5万名观众参与，现场气氛火爆。来自全国各地的说唱艺术家齐聚一堂，通过音乐表达青年文化和社会观点。活动不仅有精彩的表演，还设置了说唱工作坊和文化交流环节。",
        "image_url": "https://images.unsplash.com/photo-1483032469466-b937c425697b?w=500",
        "creator": "hiphopfan"
    },
    {
        "title": "🎼 古典音乐进校园活动启动",
        "description": "为了培养青少年对古典音乐的兴趣，市教育局联合交响乐团启动了《古典音乐进校园》活动。专业音乐家将走进中小学校，通过互动演出和音乐课程，让学生们近距离感受古典音乐的魅力。",
        "image_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=500",
        "creator": "musicteacher"
    },
    {
        "title": "🎸 独立音乐人发布新专辑",
        "description": "独立音乐人张小明发布了他的第三张个人专辑《城市夜晚》，专辑融合了民谣、摇滚和电子元素。这张专辑记录了他在大城市生活的感悟，每首歌都诉说着都市青年的心声。专辑一经发布就登上了各大音乐平台的热门榜单。",
        "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500",
        "creator": "indiemusic"
    }
]

def create_sample_users():
    """创建示例用户"""
    users = [
        {"username": "admin", "email": "admin@musicweb.com", "password": "admin123"},
        {"username": "musiclover", "email": "lover@musicweb.com", "password": "music123"},
        {"username": "hiphopfan", "email": "hiphop@musicweb.com", "password": "hiphop123"},
        {"username": "musicteacher", "email": "teacher@musicweb.com", "password": "teach123"},
        {"username": "indiemusic", "email": "indie@musicweb.com", "password": "indie123"}
    ]
    
    for user_data in users:
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing_user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"])
            )
            db.add(user)
            print(f"✅ 创建用户: {user_data['username']}")
        else:
            print(f"⚠️  用户已存在: {user_data['username']}")

def create_sample_news():
    """创建示例新闻"""
    for news_data in sample_news:
        existing_news = db.query(News).filter(News.title == news_data["title"]).first()
        if not existing_news:
            news = News(**news_data)
            db.add(news)
            print(f"✅ 创建新闻: {news_data['title']}")
        else:
            print(f"⚠️  新闻已存在: {news_data['title']}")

def main():
    try:
        print("🎵 开始创建示例数据...")
        
        # 创建用户
        print("\n👥 创建示例用户...")
        create_sample_users()
        
        # 创建新闻
        print("\n📰 创建示例新闻...")
        create_sample_news()
        
        # 提交事务
        db.commit()
        print("\n🎉 示例数据创建完成！")
        
        # 显示统计
        user_count = db.query(User).count()
        news_count = db.query(News).count()
        print(f"\n📊 数据库统计:")
        print(f"   用户总数: {user_count}")
        print(f"   新闻总数: {news_count}")
        
        print(f"\n🔐 测试账号:")
        print(f"   用户名: admin, 密码: admin123")
        print(f"   用户名: musiclover, 密码: music123")
        
    except Exception as e:
        print(f"❌ 创建数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()