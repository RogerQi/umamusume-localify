import os
import string
import time
import random
import pytest

###############################################
# Cases grabbed from race_message.json
# Note: race_comment.json is pretty similar
###############################################

def test_vanilla_str():
    original_str = "ここは第3コーナー、桶狭間ポイント！"

def test_start_formater():
    original_str = "%horse1いいスタートだ"

def test_formater_end():
    original_str = "いいスタートを切っ%horse_ta1"

def test_formater_eol():
    original_str = "美しい青空が広がる、%course\nターフも絶好の良バ場になりました！"

def test_double_backslash_eol():
    original_str = "前年の覇者\\n%h_pop3\\n現在、3番人気\\n下剋上は起りうるのか！？"

def test_eol_formater_end():
    original_str = "さあ、1番人気の紹介です\n%h_pop1"

def test_formater_ja_char():
    original_str = "さあ、今日の主役はこのウマ娘を置いて他にいない\n1番人気%h_pop1！"

def test_multiple_eol():
    original_str = "さあ、今日の主役は\nこのウマ娘を置いて他にいない\n1番人気%h_pop1！"

def test_multiple_formater():
    original_str = "%h_rank1、%h_rank2\nふたりの競り合いは続いている"

def test_multiple_formater_case_2():
    original_str = "2着には%h_rank_l2\n3着に入っ%h_rank_ta3"

def test_multiple_formater_hard():
    original_str = "%h_rank10、%h_rank_l10\\n%h_rank_no10、%h_rank_to10\\n%h_rank_ta10、%h_rank_a10"

def test_all_formatter():
    # I don't think this case exist in the original_data.
    # I'm just including this case here to make sure the parser is consistently working
    original_str = "%h_rank10、%h_rank_l10\\n%h_rank_no10、%h_rank_to10\\n%h_rank_ta10、%h_rank_a10"

def test_multiple_contiguous_special_char():
    original_str = "長丁場のこのレースですが\n%h_rank1\n早くも先頭に躍り出た"

def test_multiple_contiguous_special_char_hard():
    original_str = "夜空を覆う雨雲が緊張感を演出します\n%course%ground%distance\n%race\n%h_num_noウマ娘たちが挑みます"

###############################################
# Cases grabbed from chara.json
###############################################

def test_double_eol_r_n():
    original_str = "うーん、絶不調。\r\n踏ん張り時かなー…。"

###############################################
# Cases grabbed from common.json
###############################################

def test_tab_char():
    original_str = "君臨する“皇帝”\\nその権威に揺らぎなし！\t"

def test_double_backslash_n_eol():
    original_str = "無敵でキュート！\\n天真爛漫ホッピン少女 "

def test_color_tag():
    original_str = "いい仕上がりです。\\n<color=#FF6D26>【有力なウマ娘の1人】</color>になるでしょう。"

###############################################
# Cases grabbed from static.json
###############################################

def test_static_color_tag():
    original_str = "Facebookアカウントでは<color=#ff911c>他プラットフォーム</color>のデータと\nアカウント連携させる事ができません\nゲームデータの復旧のみ行う事ができます"

def test_static_bracket_formmater():
    original_str = "{0}勝で{2}{1}グループ{3}"

def test_stacked_color_tag_bracket():
    original_str = "エントリー回数は <color=#ff9900>{0}</color>時にリセットされます"

def test_special_char():
    # I don't think / is a special char!
    original_str = "/{0:#,0}位"