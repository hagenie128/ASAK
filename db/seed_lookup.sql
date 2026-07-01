-- Lookup seed data for Salady schema
-- Run after schema.sql

INSERT INTO brands (code, name) VALUES ('salady', '샐러디')
ON CONFLICT (code) DO NOTHING;

INSERT INTO platforms (code, name) VALUES
    ('official', '공식 홈페이지'),
    ('passorder', '패스오더'),
    ('naver_order', '네이버 예약/주문')
ON CONFLICT (code) DO NOTHING;

INSERT INTO menu_category_types (code, name) VALUES
    ('official', '공식 카테고리'),
    ('nav', '네비게이션 카테고리'),
    ('store', '매장 카테고리')
ON CONFLICT (code) DO NOTHING;

INSERT INTO dressing_policies (code, name) VALUES
    ('default', '기본 드레싱'),
    ('recommended', '추천 드레싱'),
    ('included', '포함 드레싱'),
    ('selection', '드레싱 선택 옵션'),
    ('amount', '드레싱 양'),
    ('extra_purchase', '드레싱 추가 구매')
ON CONFLICT (code) DO NOTHING;

INSERT INTO calorie_addon_types (code, name_ko) VALUES
    ('vegetable', '채소 추가'),
    ('grain', '곡물 추가'),
    ('buckwheat', '메밀면 추가'),
    ('noodles', '파스타/누들 추가')
ON CONFLICT (code) DO NOTHING;

INSERT INTO option_group_kinds (code, name_ko) VALUES
    ('base_selection', '베이스 선택'),
    ('base_extra', '베이스 추가'),
    ('dressing_selection', '드레싱 선택'),
    ('dressing_amount', '드레싱 양 선택'),
    ('dressing_extra_purchase', '드레싱 추가 구매'),
    ('topping_extra', '토핑 추가'),
    ('soup_extra', '스프 추가'),
    ('set_side', '세트 사이드/음료')
ON CONFLICT (code) DO NOTHING;

-- 공통 태그
INSERT INTO tags (code, label) VALUES
    ('NEW', '신메뉴'),
    ('BEST', '인기'),
    ('LOW_SUGAR', '저당')
ON CONFLICT (code) DO NOTHING;
