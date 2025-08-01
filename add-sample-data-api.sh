#!/bin/bash

API_URL="http://192.168.5.52:8000/api"

echo "🎵 通过API创建示例数据..."

# 创建示例用户
echo "👥 创建示例用户..."

users=(
    '{"username":"admin","email":"admin@musicweb.com","password":"admin123"}'
    '{"username":"musiclover","email":"lover@musicweb.com","password":"music123"}'
    '{"username":"hiphopfan","email":"hiphop@musicweb.com","password":"hiphop123"}'
    '{"username":"musicteacher","email":"teacher@musicweb.com","password":"teach123"}'
    '{"username":"indiemusic","email":"indie@musicweb.com","password":"indie123"}'
)

for user in "${users[@]}"; do
    echo "注册用户: $(echo $user | grep -o '"username":"[^"]*' | cut -d'"' -f4)"
    curl -s -X POST "$API_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "$user" > /dev/null
done

echo ""
echo "📰 创建示例新闻..."

# 登录admin用户获取token
echo "🔐 登录admin用户..."
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}')

ADMIN_TOKEN=$(echo $ADMIN_LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
    echo "❌ 无法获取admin token"
    exit 1
fi

# 创建新闻数据
news_data=(
    '{"title":"🎵 全新音乐节即将开幕","description":"本月底将在市中心举办为期三天的音乐节，汇聚国内外知名艺术家。从古典音乐到现代流行，从民族音乐到电子音乐，各种风格应有尽有。门票现已开售，早鸟优惠仅限前1000名购买者。","image_url":"https://images.unsplash.com/photo-1459749187778-3663c29ab4b3?w=500"}'
    '{"title":"🎸 摇滚传奇乐队重聚演出","description":"经典摇滚乐队《雷霆之声》时隔十年再次重聚，将在下个月举办全国巡回演唱会。乐队成员表示这次重聚是为了致敬那些陪伴他们成长的歌迷，演出将包含历年来的经典曲目以及全新创作。","image_url":"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500"}'
    '{"title":"🎹 青年钢琴家获国际大奖","description":"来自本地音乐学院的22岁钢琴家李小华在国际肖邦钢琴比赛中获得金奖，成为该比赛历史上最年轻的获奖者。她的演奏被评委们称赞为《技巧与情感的完美结合》，展现了新一代音乐家的卓越才华。","image_url":"https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500"}'
)

for news in "${news_data[@]}"; do
    title=$(echo $news | grep -o '"title":"[^"]*' | cut -d'"' -f4)
    echo "创建新闻: $title"
    curl -s -X POST "$API_URL/news/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d "$news" > /dev/null
done

# 登录其他用户创建更多新闻
echo ""
echo "🎤 创建更多新闻..."

# musiclover用户
LOVER_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"musiclover","password":"music123"}')
LOVER_TOKEN=$(echo $LOVER_LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

curl -s -X POST "$API_URL/news/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $LOVER_TOKEN" \
    -d '{"title":"🎤 说唱文化节引燃全城","description":"首届城市说唱文化节吸引了超过5万名观众参与，现场气氛火爆。来自全国各地的说唱艺术家齐聚一堂，通过音乐表达青年文化和社会观点。活动不仅有精彩的表演，还设置了说唱工作坊和文化交流环节。","image_url":"https://images.unsplash.com/photo-1483032469466-b937c425697b?w=500"}' > /dev/null

# hiphopfan用户
HIPHOP_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"hiphopfan","password":"hiphop123"}')
HIPHOP_TOKEN=$(echo $HIPHOP_LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

curl -s -X POST "$API_URL/news/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $HIPHOP_TOKEN" \
    -d '{"title":"🎼 古典音乐进校园活动启动","description":"为了培养青少年对古典音乐的兴趣，市教育局联合交响乐团启动了《古典音乐进校园》活动。专业音乐家将走进中小学校，通过互动演出和音乐课程，让学生们近距离感受古典音乐的魅力。","image_url":"https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=500"}' > /dev/null

echo ""
echo "🎉 示例数据创建完成！"
echo ""
echo "🔐 测试账号:"
echo "   用户名: admin, 密码: admin123"
echo "   用户名: musiclover, 密码: music123"
echo "   用户名: hiphopfan, 密码: hiphop123"
echo ""
echo "📱 现在可以刷新前端页面查看新闻了！"