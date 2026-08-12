-- ASAK seed-v3 menu dedupe
-- removed: 34, kept: 58
SET FOREIGN_KEY_CHECKS = 0;

-- 스파이시 쉬림프 샌드위치: 364 (cat 231) -> 8196 (cat 236)
UPDATE order_item SET menu_id = 8196 WHERE menu_id = 364;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 364;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 364;
DELETE FROM `menu_ing` WHERE `menu_id` = 364;
DELETE FROM `menu_nutr` WHERE `menu_id` = 364;
DELETE FROM `menu_tag` WHERE `menu_id` = 364;
DELETE FROM menu WHERE id = 364;

-- 불고기 반미 샌드위치: 501 (cat 231) -> 6918 (cat 236)
UPDATE order_item SET menu_id = 6918 WHERE menu_id = 501;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 501;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 501;
DELETE FROM `menu_ing` WHERE `menu_id` = 501;
DELETE FROM `menu_nutr` WHERE `menu_id` = 501;
DELETE FROM `menu_tag` WHERE `menu_id` = 501;
DELETE FROM menu WHERE id = 501;

-- 클래식 치킨 샌드위치: 638 (cat 232) -> 7264 (cat 236)
UPDATE order_item SET menu_id = 7264 WHERE menu_id = 638;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 638;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 638;
DELETE FROM `menu_ing` WHERE `menu_id` = 638;
DELETE FROM `menu_nutr` WHERE `menu_id` = 638;
DELETE FROM `menu_tag` WHERE `menu_id` = 638;
DELETE FROM menu WHERE id = 638;

-- 칠리베이컨 곡물랩: 908 (cat 232) -> 6683 (cat 235)
UPDATE order_item SET menu_id = 6683 WHERE menu_id = 908;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 908;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 908;
DELETE FROM `menu_ing` WHERE `menu_id` = 908;
DELETE FROM `menu_nutr` WHERE `menu_id` = 908;
DELETE FROM `menu_tag` WHERE `menu_id` = 908;
DELETE FROM menu WHERE id = 908;

-- 멕시칸 랩: 1036 (cat 232) -> 6422 (cat 235)
UPDATE order_item SET menu_id = 6422 WHERE menu_id = 1036;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 1036;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 1036;
DELETE FROM `menu_ing` WHERE `menu_id` = 1036;
DELETE FROM `menu_nutr` WHERE `menu_id` = 1036;
DELETE FROM `menu_tag` WHERE `menu_id` = 1036;
DELETE FROM menu WHERE id = 1036;

-- 로스트닭다리살 샐러디: 1301 (cat 232) -> 5855 (cat 233)
UPDATE order_item SET menu_id = 5855 WHERE menu_id = 1301;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 1301;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 1301;
DELETE FROM `menu_ing` WHERE `menu_id` = 1301;
DELETE FROM `menu_nutr` WHERE `menu_id` = 1301;
DELETE FROM `menu_tag` WHERE `menu_id` = 1301;
DELETE FROM menu WHERE id = 1301;

-- 그라브락스 연어 샐러디: 1437 (cat 232) -> 8601 (cat 233)
UPDATE order_item SET menu_id = 8601 WHERE menu_id = 1437;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 1437;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 1437;
DELETE FROM `menu_ing` WHERE `menu_id` = 1437;
DELETE FROM `menu_nutr` WHERE `menu_id` = 1437;
DELETE FROM `menu_tag` WHERE `menu_id` = 1437;
DELETE FROM menu WHERE id = 1437;

-- 타코 쉬림프 랩: 1700 (cat 232) -> 6550 (cat 235)
UPDATE order_item SET menu_id = 6550 WHERE menu_id = 1700;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 1700;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 1700;
DELETE FROM `menu_ing` WHERE `menu_id` = 1700;
DELETE FROM `menu_nutr` WHERE `menu_id` = 1700;
DELETE FROM `menu_tag` WHERE `menu_id` = 1700;
DELETE FROM menu WHERE id = 1700;

-- 로스트닭다리살마요 덮밥: 1833 (cat 232) -> 6275 (cat 232)
UPDATE order_item SET menu_id = 6275 WHERE menu_id = 1833;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 1833;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 1833;
DELETE FROM `menu_ing` WHERE `menu_id` = 1833;
DELETE FROM `menu_nutr` WHERE `menu_id` = 1833;
DELETE FROM `menu_tag` WHERE `menu_id` = 1833;
DELETE FROM menu WHERE id = 1833;

-- BELT 시저 샌드위치: 4056 (cat 232) -> 8065 (cat 236)
UPDATE order_item SET menu_id = 8065 WHERE menu_id = 4056;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 4056;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 4056;
DELETE FROM `menu_ing` WHERE `menu_id` = 4056;
DELETE FROM `menu_nutr` WHERE `menu_id` = 4056;
DELETE FROM `menu_tag` WHERE `menu_id` = 4056;
DELETE FROM menu WHERE id = 4056;

-- 비프에그마요 샌드위치: 4317 (cat 232) -> 7504 (cat 236)
UPDATE order_item SET menu_id = 7504 WHERE menu_id = 4317;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 4317;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 4317;
DELETE FROM `menu_ing` WHERE `menu_id` = 4317;
DELETE FROM `menu_nutr` WHERE `menu_id` = 4317;
DELETE FROM `menu_tag` WHERE `menu_id` = 4317;
DELETE FROM menu WHERE id = 4317;

-- 고소우삼겹 곡물랩: 4581 (cat 232) -> 10451 (cat 235)
UPDATE order_item SET menu_id = 10451 WHERE menu_id = 4581;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 4581;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 4581;
DELETE FROM `menu_ing` WHERE `menu_id` = 4581;
DELETE FROM `menu_nutr` WHERE `menu_id` = 4581;
DELETE FROM `menu_tag` WHERE `menu_id` = 4581;
DELETE FROM menu WHERE id = 4581;

-- 그라브락스 연어 랩: 4842 (cat 232) -> 10324 (cat 235)
UPDATE order_item SET menu_id = 10324 WHERE menu_id = 4842;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 4842;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 4842;
DELETE FROM `menu_ing` WHERE `menu_id` = 4842;
DELETE FROM `menu_nutr` WHERE `menu_id` = 4842;
DELETE FROM `menu_tag` WHERE `menu_id` = 4842;
DELETE FROM menu WHERE id = 4842;

-- 시저치킨 랩: 4969 (cat 232) -> 10069 (cat 235)
UPDATE order_item SET menu_id = 10069 WHERE menu_id = 4969;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 4969;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 4969;
DELETE FROM `menu_ing` WHERE `menu_id` = 4969;
DELETE FROM `menu_nutr` WHERE `menu_id` = 4969;
DELETE FROM `menu_tag` WHERE `menu_id` = 4969;
DELETE FROM menu WHERE id = 4969;

-- 로스트닭다리살 랩: 5093 (cat 232) -> 10193 (cat 235)
UPDATE order_item SET menu_id = 10193 WHERE menu_id = 5093;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 5093;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 5093;
DELETE FROM `menu_ing` WHERE `menu_id` = 5093;
DELETE FROM `menu_nutr` WHERE `menu_id` = 5093;
DELETE FROM `menu_tag` WHERE `menu_id` = 5093;
DELETE FROM menu WHERE id = 5093;

-- 에그마요 랩: 5224 (cat 232) -> 9941 (cat 235)
UPDATE order_item SET menu_id = 9941 WHERE menu_id = 5224;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 5224;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 5224;
DELETE FROM `menu_ing` WHERE `menu_id` = 5224;
DELETE FROM `menu_nutr` WHERE `menu_id` = 5224;
DELETE FROM `menu_tag` WHERE `menu_id` = 5224;
DELETE FROM menu WHERE id = 5224;

-- 우삼겹메밀면 누들볼: 5725 (cat 232) -> 1568 (cat 232)
UPDATE order_item SET menu_id = 1568 WHERE menu_id = 5725;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 5725;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 5725;
DELETE FROM `menu_ing` WHERE `menu_id` = 5725;
DELETE FROM `menu_nutr` WHERE `menu_id` = 5725;
DELETE FROM `menu_tag` WHERE `menu_id` = 5725;
DELETE FROM menu WHERE id = 5725;

-- 그라브락스 연어 포케볼: 5998 (cat 232) -> 768 (cat 232)
UPDATE order_item SET menu_id = 768 WHERE menu_id = 5998;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 5998;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 5998;
DELETE FROM `menu_ing` WHERE `menu_id` = 5998;
DELETE FROM `menu_nutr` WHERE `menu_id` = 5998;
DELETE FROM `menu_tag` WHERE `menu_id` = 5998;
DELETE FROM menu WHERE id = 5998;

-- 타코 쉬림프 샐러디: 6133 (cat 233) -> 2393 (cat 233)
UPDATE order_item SET menu_id = 2393 WHERE menu_id = 6133;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 6133;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 6133;
DELETE FROM `menu_ing` WHERE `menu_id` = 6133;
DELETE FROM `menu_nutr` WHERE `menu_id` = 6133;
DELETE FROM `menu_tag` WHERE `menu_id` = 6133;
DELETE FROM menu WHERE id = 6133;

-- 탄단지 샐러디: 8328 (cat 233) -> 1978 (cat 233)
UPDATE order_item SET menu_id = 1978 WHERE menu_id = 8328;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 8328;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 8328;
DELETE FROM `menu_ing` WHERE `menu_id` = 8328;
DELETE FROM `menu_nutr` WHERE `menu_id` = 8328;
DELETE FROM `menu_tag` WHERE `menu_id` = 8328;
DELETE FROM menu WHERE id = 8328;

-- 랜치 콥 샐러디: 8463 (cat 233) -> 2114 (cat 233)
UPDATE order_item SET menu_id = 2114 WHERE menu_id = 8463;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 8463;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 8463;
DELETE FROM `menu_ing` WHERE `menu_id` = 8463;
DELETE FROM `menu_nutr` WHERE `menu_id` = 8463;
DELETE FROM `menu_tag` WHERE `menu_id` = 8463;
DELETE FROM menu WHERE id = 8463;

-- 고소삼겹 들기름파스타 누들볼: 8737 (cat 232) -> 3523 (cat 233)
UPDATE order_item SET menu_id = 3523 WHERE menu_id = 8737;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 8737;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 8737;
DELETE FROM `menu_ing` WHERE `menu_id` = 8737;
DELETE FROM `menu_nutr` WHERE `menu_id` = 8737;
DELETE FROM `menu_tag` WHERE `menu_id` = 8737;
DELETE FROM menu WHERE id = 8737;

-- 칠리베이컨 포케볼: 8870 (cat 232) -> 1167 (cat 232)
UPDATE order_item SET menu_id = 1167 WHERE menu_id = 8870;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 8870;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 8870;
DELETE FROM `menu_ing` WHERE `menu_id` = 8870;
DELETE FROM `menu_nutr` WHERE `menu_id` = 8870;
DELETE FROM `menu_tag` WHERE `menu_id` = 8870;
DELETE FROM menu WHERE id = 8870;

-- 바베큐닭다리살 포케볼: 9003 (cat 232) -> 2962 (cat 233)
UPDATE order_item SET menu_id = 2962 WHERE menu_id = 9003;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9003;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9003;
DELETE FROM `menu_ing` WHERE `menu_id` = 9003;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9003;
DELETE FROM `menu_tag` WHERE `menu_id` = 9003;
DELETE FROM menu WHERE id = 9003;

-- 우삼겹 포케볼: 9138 (cat 232) -> 2678 (cat 233)
UPDATE order_item SET menu_id = 2678 WHERE menu_id = 9138;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9138;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9138;
DELETE FROM `menu_ing` WHERE `menu_id` = 9138;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9138;
DELETE FROM `menu_tag` WHERE `menu_id` = 9138;
DELETE FROM menu WHERE id = 9138;

-- 노릇노릇두부 포케볼: 9273 (cat 232) -> 2820 (cat 233)
UPDATE order_item SET menu_id = 2820 WHERE menu_id = 9273;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9273;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9273;
DELETE FROM `menu_ing` WHERE `menu_id` = 9273;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9273;
DELETE FROM `menu_tag` WHERE `menu_id` = 9273;
DELETE FROM menu WHERE id = 9273;

-- 바베큐삼겹 덮밥: 9408 (cat 232) -> 3105 (cat 233)
UPDATE order_item SET menu_id = 3105 WHERE menu_id = 9408;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9408;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9408;
DELETE FROM `menu_ing` WHERE `menu_id` = 9408;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9408;
DELETE FROM `menu_tag` WHERE `menu_id` = 9408;
DELETE FROM menu WHERE id = 9408;

-- 닭다리살 MAX 프로틴 박스: 9549 (cat 232) -> 3664 (cat 234)
UPDATE order_item SET menu_id = 3664 WHERE menu_id = 9549;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9549;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9549;
DELETE FROM `menu_ing` WHERE `menu_id` = 9549;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9549;
DELETE FROM `menu_tag` WHERE `menu_id` = 9549;
DELETE FROM menu WHERE id = 9549;

-- 치킨 MAX 프로틴 파스타: 9677 (cat 232) -> 3794 (cat 234)
UPDATE order_item SET menu_id = 3794 WHERE menu_id = 9677;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9677;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9677;
DELETE FROM `menu_ing` WHERE `menu_id` = 9677;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9677;
DELETE FROM `menu_tag` WHERE `menu_id` = 9677;
DELETE FROM menu WHERE id = 9677;

-- 우삼겹 MAX 프로틴 박스: 9806 (cat 232) -> 3925 (cat 234)
UPDATE order_item SET menu_id = 3925 WHERE menu_id = 9806;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 9806;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 9806;
DELETE FROM `menu_ing` WHERE `menu_id` = 9806;
DELETE FROM `menu_nutr` WHERE `menu_id` = 9806;
DELETE FROM `menu_tag` WHERE `menu_id` = 9806;
DELETE FROM menu WHERE id = 9806;

-- 채소볼: 10581 (cat 232) -> 5478 (cat 232)
UPDATE order_item SET menu_id = 5478 WHERE menu_id = 10581;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 10581;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 10581;
DELETE FROM `menu_ing` WHERE `menu_id` = 10581;
DELETE FROM `menu_nutr` WHERE `menu_id` = 10581;
DELETE FROM `menu_tag` WHERE `menu_id` = 10581;
DELETE FROM menu WHERE id = 10581;

-- 포케볼: 10642 (cat 232) -> 5539 (cat 232)
UPDATE order_item SET menu_id = 5539 WHERE menu_id = 10642;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 10642;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 10642;
DELETE FROM `menu_ing` WHERE `menu_id` = 10642;
DELETE FROM `menu_nutr` WHERE `menu_id` = 10642;
DELETE FROM `menu_tag` WHERE `menu_id` = 10642;
DELETE FROM menu WHERE id = 10642;

-- 메밀면볼: 10706 (cat 232) -> 5603 (cat 232)
UPDATE order_item SET menu_id = 5603 WHERE menu_id = 10706;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 10706;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 10706;
DELETE FROM `menu_ing` WHERE `menu_id` = 10706;
DELETE FROM `menu_nutr` WHERE `menu_id` = 10706;
DELETE FROM `menu_tag` WHERE `menu_id` = 10706;
DELETE FROM menu WHERE id = 10706;

-- 파스타볼: 10767 (cat 232) -> 5664 (cat 232)
UPDATE order_item SET menu_id = 5664 WHERE menu_id = 10767;
DELETE FROM `menu_opt_override` WHERE `menu_id` = 10767;
DELETE FROM `menu_opt_policy` WHERE `menu_id` = 10767;
DELETE FROM `menu_ing` WHERE `menu_id` = 10767;
DELETE FROM `menu_nutr` WHERE `menu_id` = 10767;
DELETE FROM `menu_tag` WHERE `menu_id` = 10767;
DELETE FROM menu WHERE id = 10767;

SET FOREIGN_KEY_CHECKS = 1;