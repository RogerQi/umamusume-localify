import sys
import os
import string
import time
import random
import pytest

import translator

###############################################
# Init
###############################################

test_translator = translator.UmaMusumeStrTrans("test")

def basic_test():
    assert test_translator is not None

###############################################
# Some helper functions
###############################################

def check_appear_in_order(base_str, landmark_str_list):
    my_str = base_str
    for landmark in landmark_str_list:
        landmark_idx = my_str.find(landmark)
        if landmark_idx == -1: return False
        my_str = my_str[landmark_idx + len(landmark):]
    return True

def test_sep_extraction(original_str, gt_seps):
    seps, _ = test_translator.split_raw_str(original_str)
    translated_str = test_translator.trans_one(original_str)

    assert len(seps) == len(gt_seps)
    assert check_appear_in_order(translated_str, gt_seps)

###############################################
# Cases grabbed from race_message.json
# Note: race_comment.json is pretty similar
###############################################

def test_vanilla_str():
    original_str = "ここは第3コーナー、桶狭間ポイント！"
    gt_seps = []

    test_sep_extraction(original_str, gt_seps)

def test_start_formater():
    original_str = "%horse1いいスタートだ"
    gt_seps = ["%horse1"]

    test_sep_extraction(original_str, gt_seps)

def test_formater_end():
    original_str = "いいスタートを切っ%horse_ta1"
    gt_seps = ["%horse_ta1"]

    test_sep_extraction(original_str, gt_seps)

def test_formater_eol():
    original_str = "美しい青空が広がる、%course\nターフも絶好の良バ場になりました！"
    gt_seps = ["%course\n"]

    test_sep_extraction(original_str, gt_seps)

def test_double_backslash_eol():
    original_str = "前年の覇者\\n%h_pop3\\n現在、3番人気\\n下剋上は起りうるのか！？"
    gt_seps = ["\\n%h_pop3\\n", "\\n"]

    test_sep_extraction(original_str, gt_seps)

def test_eol_formater_end():
    original_str = "さあ、1番人気の紹介です\n%h_pop1"
    gt_seps = ["\n%h_pop1"]

    test_sep_extraction(original_str, gt_seps)

def test_formater_ja_char():
    original_str = "さあ、今日の主役はこのウマ娘を置いて他にいない\n1番人気%h_pop1！"
    gt_seps = ["\n", "%h_pop1"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_eol():
    original_str = "さあ、今日の主役は\nこのウマ娘を置いて他にいない\n1番人気%h_pop1！"
    gt_seps = ["\n", "\n", "%h_pop1"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_formater():
    original_str = "%h_rank1、%h_rank2\nふたりの競り合いは続いている"
    gt_seps = ["%h_rank1", "%h_rank2\n"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_formater_case_2():
    original_str = "2着には%h_rank_l2\n3着に入っ%h_rank_ta3"
    gt_seps = ["%h_rank_l2\n", "%h_rank_ta3"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_formater_hard():
    original_str = "%h_rank10、%h_rank_l10\\n%h_rank_no10、%h_rank_to10\\n%h_rank_ta10、%h_rank_a10"
    gt_seps = ["%h_rank10", "%h_rank_l10\\n%h_rank_no10", "%h_rank_to10\\n%h_rank_ta10", "%h_rank_a10"]

    test_sep_extraction(original_str, gt_seps)

def test_all_formatter():
    # I don't think this case exist in the original_data.
    # I'm just including this case here to make sure the parser is consistently working
    original_str = "%h_rank10%h_rank_l10\\n%h_rank_no10%h_rank_to10\\n%h_rank_ta10%h_rank_a10"
    gt_seps = ["%h_rank10%h_rank_l10\\n%h_rank_no10%h_rank_to10\\n%h_rank_ta10%h_rank_a10"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_contiguous_special_char():
    original_str = "長丁場のこのレースですが\n%h_rank1\n早くも先頭に躍り出た"
    gt_seps = ["\n%h_rank1\n"]

    test_sep_extraction(original_str, gt_seps)

def test_multiple_contiguous_special_char_hard():
    original_str = "夜空を覆う雨雲が緊張感を演出します\n%course%ground%distance\n%race\n%h_num_noウマ娘たちが挑みます"
    gt_seps = ["\n%course%ground%distance\n%race\n%h_num_no"]

    test_sep_extraction(original_str, gt_seps)

###############################################
# Cases grabbed from chara.json
###############################################

def test_double_eol_r_n():
    original_str = "うーん、絶不調。\r\n踏ん張り時かなー…。"
    gt_seps = ["\r\n"]

    test_sep_extraction(original_str, gt_seps)

###############################################
# Cases grabbed from common.json
###############################################

def test_tab_char():
    original_str = "君臨する“皇帝”\\nその権威に揺らぎなし！\t"
    gt_seps = ["\\n", "\t"]

    test_sep_extraction(original_str, gt_seps)

def test_double_backslash_n_eol():
    original_str = "無敵でキュート！\\n天真爛漫ホッピン少女 "
    gt_seps = ["\\n"]

    test_sep_extraction(original_str, gt_seps)

def test_color_tag():
    original_str = "いい仕上がりです。\\n<color=#FF6D26>【有力なウマ娘の1人】</color>になるでしょう。"
    gt_seps = ["\\n<color=#FF6D26>", "</color>"]

    test_sep_extraction(original_str, gt_seps)

###############################################
# Cases grabbed from static.json
###############################################

def test_static_color_tag():
    original_str = "Facebookアカウントでは<color=#ff911c>他プラットフォーム</color>のデータと\nアカウント連携させる事ができません\nゲームデータの復旧のみ行う事ができます"
    gt_seps = ["<color=#ff911c>", "</color>", "\n", "\n"]

    test_sep_extraction(original_str, gt_seps)

def test_static_bracket_formmater():
    original_str = "{0}勝で{2}{1}グループ{3}"
    gt_seps = ["{0}", "{2}", "{1}", "{3}"]

    test_sep_extraction(original_str, gt_seps)

def test_stacked_color_tag_bracket():
    original_str = "エントリー回数は <color=#ff9900>{0}</color>時にリセットされます"
    gt_seps = ["<color=#ff9900>{0}</color>"]

    test_sep_extraction(original_str, gt_seps)

def test_special_qualifier():
    # I don't think / is a special char!
    original_str = "/{0:#,0}位"
    gt_seps = ["{0:#,0}"]

    test_sep_extraction(original_str, gt_seps)

def test_qualifier_hard():
    original_str = "（{0:0.00}{1}）"
    gt_seps = ["{0:0.00}{1}"]

    test_sep_extraction(original_str, gt_seps)
