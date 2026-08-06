-- ASAK menu dedupe (real DB schema)
SET FOREIGN_KEY_CHECKS=0;

-- 스파이시 쉬림프 샌드위치: 364 -> 8196
UPDATE order_item SET menu_id=8196 WHERE menu_id=364;
DELETE FROM menu_opt_override WHERE menu_id=364;
DELETE FROM menu_opt_policy WHERE menu_id=364;
DELETE FROM menu_ing WHERE menu_id=364;
DELETE FROM menu_nutr WHERE menu_id=364;
DELETE FROM menu_tag WHERE menu_id=364;
DELETE FROM menu WHERE id=364;

-- 불고기 반미 샌드위치: 501 -> 6918
UPDATE order_item SET menu_id=6918 WHERE menu_id=501;
DELETE FROM menu_opt_override WHERE menu_id=501;
DELETE FROM menu_opt_policy WHERE menu_id=501;
DELETE FROM menu_ing WHERE menu_id=501;
DELETE FROM menu_nutr WHERE menu_id=501;
DELETE FROM menu_tag WHERE menu_id=501;
DELETE FROM menu WHERE id=501;

-- 클래식 치킨 샌드위치: 638 -> 7264
UPDATE order_item SET menu_id=7264 WHERE menu_id=638;
DELETE FROM menu_opt_override WHERE menu_id=638;
DELETE FROM menu_opt_policy WHERE menu_id=638;
DELETE FROM menu_ing WHERE menu_id=638;
DELETE FROM menu_nutr WHERE menu_id=638;
DELETE FROM menu_tag WHERE menu_id=638;
DELETE FROM menu WHERE id=638;

-- 칠리베이컨 곡물랩: 908 -> 6683
UPDATE order_item SET menu_id=6683 WHERE menu_id=908;
DELETE FROM menu_opt_override WHERE menu_id=908;
DELETE FROM menu_opt_policy WHERE menu_id=908;
DELETE FROM menu_ing WHERE menu_id=908;
DELETE FROM menu_nutr WHERE menu_id=908;
DELETE FROM menu_tag WHERE menu_id=908;
DELETE FROM menu WHERE id=908;

-- 멕시칸 랩: 1036 -> 6422
UPDATE order_item SET menu_id=6422 WHERE menu_id=1036;
DELETE FROM menu_opt_override WHERE menu_id=1036;
DELETE FROM menu_opt_policy WHERE menu_id=1036;
DELETE FROM menu_ing WHERE menu_id=1036;
DELETE FROM menu_nutr WHERE menu_id=1036;
DELETE FROM menu_tag WHERE menu_id=1036;
DELETE FROM menu WHERE id=1036;

-- 로스트닭다리살 샐러디: 1301 -> 5855
UPDATE order_item SET menu_id=5855 WHERE menu_id=1301;
DELETE FROM menu_opt_override WHERE menu_id=1301;
DELETE FROM menu_opt_policy WHERE menu_id=1301;
DELETE FROM menu_ing WHERE menu_id=1301;
DELETE FROM menu_nutr WHERE menu_id=1301;
DELETE FROM menu_tag WHERE menu_id=1301;
DELETE FROM menu WHERE id=1301;

-- 그라브락스 연어 샐러디: 1437 -> 8601
UPDATE order_item SET menu_id=8601 WHERE menu_id=1437;
DELETE FROM menu_opt_override WHERE menu_id=1437;
DELETE FROM menu_opt_policy WHERE menu_id=1437;
DELETE FROM menu_ing WHERE menu_id=1437;
DELETE FROM menu_nutr WHERE menu_id=1437;
DELETE FROM menu_tag WHERE menu_id=1437;
DELETE FROM menu WHERE id=1437;

-- 타코 쉬림프 랩: 1700 -> 6550
UPDATE order_item SET menu_id=6550 WHERE menu_id=1700;
DELETE FROM menu_opt_override WHERE menu_id=1700;
DELETE FROM menu_opt_policy WHERE menu_id=1700;
DELETE FROM menu_ing WHERE menu_id=1700;
DELETE FROM menu_nutr WHERE menu_id=1700;
DELETE FROM menu_tag WHERE menu_id=1700;
DELETE FROM menu WHERE id=1700;

-- BELT 시저 샌드위치: 4056 -> 8065
UPDATE order_item SET menu_id=8065 WHERE menu_id=4056;
DELETE FROM menu_opt_override WHERE menu_id=4056;
DELETE FROM menu_opt_policy WHERE menu_id=4056;
DELETE FROM menu_ing WHERE menu_id=4056;
DELETE FROM menu_nutr WHERE menu_id=4056;
DELETE FROM menu_tag WHERE menu_id=4056;
DELETE FROM menu WHERE id=4056;

-- 비프에그마요 샌드위치: 4317 -> 7504
UPDATE order_item SET menu_id=7504 WHERE menu_id=4317;
DELETE FROM menu_opt_override WHERE menu_id=4317;
DELETE FROM menu_opt_policy WHERE menu_id=4317;
DELETE FROM menu_ing WHERE menu_id=4317;
DELETE FROM menu_nutr WHERE menu_id=4317;
DELETE FROM menu_tag WHERE menu_id=4317;
DELETE FROM menu WHERE id=4317;

-- 고소우삼겹 곡물랩: 4581 -> 10451
UPDATE order_item SET menu_id=10451 WHERE menu_id=4581;
DELETE FROM menu_opt_override WHERE menu_id=4581;
DELETE FROM menu_opt_policy WHERE menu_id=4581;
DELETE FROM menu_ing WHERE menu_id=4581;
DELETE FROM menu_nutr WHERE menu_id=4581;
DELETE FROM menu_tag WHERE menu_id=4581;
DELETE FROM menu WHERE id=4581;

-- 그라브락스 연어 랩: 4842 -> 10324
UPDATE order_item SET menu_id=10324 WHERE menu_id=4842;
DELETE FROM menu_opt_override WHERE menu_id=4842;
DELETE FROM menu_opt_policy WHERE menu_id=4842;
DELETE FROM menu_ing WHERE menu_id=4842;
DELETE FROM menu_nutr WHERE menu_id=4842;
DELETE FROM menu_tag WHERE menu_id=4842;
DELETE FROM menu WHERE id=4842;

-- 시저치킨 랩: 4969 -> 10069
UPDATE order_item SET menu_id=10069 WHERE menu_id=4969;
DELETE FROM menu_opt_override WHERE menu_id=4969;
DELETE FROM menu_opt_policy WHERE menu_id=4969;
DELETE FROM menu_ing WHERE menu_id=4969;
DELETE FROM menu_nutr WHERE menu_id=4969;
DELETE FROM menu_tag WHERE menu_id=4969;
DELETE FROM menu WHERE id=4969;

-- 로스트닭다리살 랩: 5093 -> 10193
UPDATE order_item SET menu_id=10193 WHERE menu_id=5093;
DELETE FROM menu_opt_override WHERE menu_id=5093;
DELETE FROM menu_opt_policy WHERE menu_id=5093;
DELETE FROM menu_ing WHERE menu_id=5093;
DELETE FROM menu_nutr WHERE menu_id=5093;
DELETE FROM menu_tag WHERE menu_id=5093;
DELETE FROM menu WHERE id=5093;

-- 에그마요 랩: 5224 -> 9941
UPDATE order_item SET menu_id=9941 WHERE menu_id=5224;
DELETE FROM menu_opt_override WHERE menu_id=5224;
DELETE FROM menu_opt_policy WHERE menu_id=5224;
DELETE FROM menu_ing WHERE menu_id=5224;
DELETE FROM menu_nutr WHERE menu_id=5224;
DELETE FROM menu_tag WHERE menu_id=5224;
DELETE FROM menu WHERE id=5224;

-- 우삼겹메밀면 누들볼: 5725 -> 1568
UPDATE order_item SET menu_id=1568 WHERE menu_id=5725;
DELETE FROM menu_opt_override WHERE menu_id=5725;
DELETE FROM menu_opt_policy WHERE menu_id=5725;
DELETE FROM menu_ing WHERE menu_id=5725;
DELETE FROM menu_nutr WHERE menu_id=5725;
DELETE FROM menu_tag WHERE menu_id=5725;
DELETE FROM menu WHERE id=5725;

-- 그라브락스 연어 포케볼: 5998 -> 768
UPDATE order_item SET menu_id=768 WHERE menu_id=5998;
DELETE FROM menu_opt_override WHERE menu_id=5998;
DELETE FROM menu_opt_policy WHERE menu_id=5998;
DELETE FROM menu_ing WHERE menu_id=5998;
DELETE FROM menu_nutr WHERE menu_id=5998;
DELETE FROM menu_tag WHERE menu_id=5998;
DELETE FROM menu WHERE id=5998;

-- 타코 쉬림프 샐러디: 6133 -> 2393
UPDATE order_item SET menu_id=2393 WHERE menu_id=6133;
DELETE FROM menu_opt_override WHERE menu_id=6133;
DELETE FROM menu_opt_policy WHERE menu_id=6133;
DELETE FROM menu_ing WHERE menu_id=6133;
DELETE FROM menu_nutr WHERE menu_id=6133;
DELETE FROM menu_tag WHERE menu_id=6133;
DELETE FROM menu WHERE id=6133;

-- 로스트닭다리살마요 덮밥: 6275 -> 1833
UPDATE order_item SET menu_id=1833 WHERE menu_id=6275;
DELETE FROM menu_opt_override WHERE menu_id=6275;
DELETE FROM menu_opt_policy WHERE menu_id=6275;
DELETE FROM menu_ing WHERE menu_id=6275;
DELETE FROM menu_nutr WHERE menu_id=6275;
DELETE FROM menu_tag WHERE menu_id=6275;
DELETE FROM menu WHERE id=6275;

-- 탄단지 샐러디: 8328 -> 1978
UPDATE order_item SET menu_id=1978 WHERE menu_id=8328;
DELETE FROM menu_opt_override WHERE menu_id=8328;
DELETE FROM menu_opt_policy WHERE menu_id=8328;
DELETE FROM menu_ing WHERE menu_id=8328;
DELETE FROM menu_nutr WHERE menu_id=8328;
DELETE FROM menu_tag WHERE menu_id=8328;
DELETE FROM menu WHERE id=8328;

-- 랜치 콥 샐러디: 8463 -> 2114
UPDATE order_item SET menu_id=2114 WHERE menu_id=8463;
DELETE FROM menu_opt_override WHERE menu_id=8463;
DELETE FROM menu_opt_policy WHERE menu_id=8463;
DELETE FROM menu_ing WHERE menu_id=8463;
DELETE FROM menu_nutr WHERE menu_id=8463;
DELETE FROM menu_tag WHERE menu_id=8463;
DELETE FROM menu WHERE id=8463;

-- 고소삼겹 들기름파스타 누들볼: 8737 -> 3523
UPDATE order_item SET menu_id=3523 WHERE menu_id=8737;
DELETE FROM menu_opt_override WHERE menu_id=8737;
DELETE FROM menu_opt_policy WHERE menu_id=8737;
DELETE FROM menu_ing WHERE menu_id=8737;
DELETE FROM menu_nutr WHERE menu_id=8737;
DELETE FROM menu_tag WHERE menu_id=8737;
DELETE FROM menu WHERE id=8737;

-- 칠리베이컨 포케볼: 8870 -> 1167
UPDATE order_item SET menu_id=1167 WHERE menu_id=8870;
DELETE FROM menu_opt_override WHERE menu_id=8870;
DELETE FROM menu_opt_policy WHERE menu_id=8870;
DELETE FROM menu_ing WHERE menu_id=8870;
DELETE FROM menu_nutr WHERE menu_id=8870;
DELETE FROM menu_tag WHERE menu_id=8870;
DELETE FROM menu WHERE id=8870;

-- 바베큐닭다리살 포케볼: 9003 -> 2962
UPDATE order_item SET menu_id=2962 WHERE menu_id=9003;
DELETE FROM menu_opt_override WHERE menu_id=9003;
DELETE FROM menu_opt_policy WHERE menu_id=9003;
DELETE FROM menu_ing WHERE menu_id=9003;
DELETE FROM menu_nutr WHERE menu_id=9003;
DELETE FROM menu_tag WHERE menu_id=9003;
DELETE FROM menu WHERE id=9003;

-- 우삼겹 포케볼: 9138 -> 2678
UPDATE order_item SET menu_id=2678 WHERE menu_id=9138;
DELETE FROM menu_opt_override WHERE menu_id=9138;
DELETE FROM menu_opt_policy WHERE menu_id=9138;
DELETE FROM menu_ing WHERE menu_id=9138;
DELETE FROM menu_nutr WHERE menu_id=9138;
DELETE FROM menu_tag WHERE menu_id=9138;
DELETE FROM menu WHERE id=9138;

-- 노릇노릇두부 포케볼: 9273 -> 2820
UPDATE order_item SET menu_id=2820 WHERE menu_id=9273;
DELETE FROM menu_opt_override WHERE menu_id=9273;
DELETE FROM menu_opt_policy WHERE menu_id=9273;
DELETE FROM menu_ing WHERE menu_id=9273;
DELETE FROM menu_nutr WHERE menu_id=9273;
DELETE FROM menu_tag WHERE menu_id=9273;
DELETE FROM menu WHERE id=9273;

-- 바베큐삼겹 덮밥: 9408 -> 3105
UPDATE order_item SET menu_id=3105 WHERE menu_id=9408;
DELETE FROM menu_opt_override WHERE menu_id=9408;
DELETE FROM menu_opt_policy WHERE menu_id=9408;
DELETE FROM menu_ing WHERE menu_id=9408;
DELETE FROM menu_nutr WHERE menu_id=9408;
DELETE FROM menu_tag WHERE menu_id=9408;
DELETE FROM menu WHERE id=9408;

-- 닭다리살 MAX 프로틴 박스: 9549 -> 3664
UPDATE order_item SET menu_id=3664 WHERE menu_id=9549;
DELETE FROM menu_opt_override WHERE menu_id=9549;
DELETE FROM menu_opt_policy WHERE menu_id=9549;
DELETE FROM menu_ing WHERE menu_id=9549;
DELETE FROM menu_nutr WHERE menu_id=9549;
DELETE FROM menu_tag WHERE menu_id=9549;
DELETE FROM menu WHERE id=9549;

-- 치킨 MAX 프로틴 파스타: 9677 -> 3794
UPDATE order_item SET menu_id=3794 WHERE menu_id=9677;
DELETE FROM menu_opt_override WHERE menu_id=9677;
DELETE FROM menu_opt_policy WHERE menu_id=9677;
DELETE FROM menu_ing WHERE menu_id=9677;
DELETE FROM menu_nutr WHERE menu_id=9677;
DELETE FROM menu_tag WHERE menu_id=9677;
DELETE FROM menu WHERE id=9677;

-- 우삼겹 MAX 프로틴 박스: 9806 -> 3925
UPDATE order_item SET menu_id=3925 WHERE menu_id=9806;
DELETE FROM menu_opt_override WHERE menu_id=9806;
DELETE FROM menu_opt_policy WHERE menu_id=9806;
DELETE FROM menu_ing WHERE menu_id=9806;
DELETE FROM menu_nutr WHERE menu_id=9806;
DELETE FROM menu_tag WHERE menu_id=9806;
DELETE FROM menu WHERE id=9806;

-- 채소볼: 10581 -> 5478
UPDATE order_item SET menu_id=5478 WHERE menu_id=10581;
DELETE FROM menu_opt_override WHERE menu_id=10581;
DELETE FROM menu_opt_policy WHERE menu_id=10581;
DELETE FROM menu_ing WHERE menu_id=10581;
DELETE FROM menu_nutr WHERE menu_id=10581;
DELETE FROM menu_tag WHERE menu_id=10581;
DELETE FROM menu WHERE id=10581;

-- 포케볼: 10642 -> 5539
UPDATE order_item SET menu_id=5539 WHERE menu_id=10642;
DELETE FROM menu_opt_override WHERE menu_id=10642;
DELETE FROM menu_opt_policy WHERE menu_id=10642;
DELETE FROM menu_ing WHERE menu_id=10642;
DELETE FROM menu_nutr WHERE menu_id=10642;
DELETE FROM menu_tag WHERE menu_id=10642;
DELETE FROM menu WHERE id=10642;

-- 메밀면볼: 10706 -> 5603
UPDATE order_item SET menu_id=5603 WHERE menu_id=10706;
DELETE FROM menu_opt_override WHERE menu_id=10706;
DELETE FROM menu_opt_policy WHERE menu_id=10706;
DELETE FROM menu_ing WHERE menu_id=10706;
DELETE FROM menu_nutr WHERE menu_id=10706;
DELETE FROM menu_tag WHERE menu_id=10706;
DELETE FROM menu WHERE id=10706;

-- 파스타볼: 10767 -> 5664
UPDATE order_item SET menu_id=5664 WHERE menu_id=10767;
DELETE FROM menu_opt_override WHERE menu_id=10767;
DELETE FROM menu_opt_policy WHERE menu_id=10767;
DELETE FROM menu_ing WHERE menu_id=10767;
DELETE FROM menu_nutr WHERE menu_id=10767;
DELETE FROM menu_tag WHERE menu_id=10767;
DELETE FROM menu WHERE id=10767;

SET FOREIGN_KEY_CHECKS=1;