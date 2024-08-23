import re

def intent_encoding(text):
    if re.match(r'query_bidding_information|招投标信息查询', text):
        return 0, 0
    if re.match(r'bidding_project_overview|招投标项目概述', text):
        return 0, 1
    if re.match(r'query_roadshow_events|路演活动查询', text):
        return 1, 0
    if re.match(r'roadshow_event_details|路演活动详情', text):
        return 1, 1
    if re.match(r'query_enterprise_exhibition_information|查询企业参展信息', text):
        return 2, 0
    if re.match(r'enterprise_exhibition_overview|企业参展概述', text):
        return 2, 1
    if re.match(r'view_bidding_announcement|查看招标公告', text):
        return 3, 0
    if re.match(r'query_winning_enterprises|查询中标企业', text):
        return 3, 1
    if re.match(r'roadshow_event_booking|路演活动预约', text):
        return 4, 0
    if re.match(r'bidding_policy_interpretation|招投标政策解读', text):
        return 4, 1
    if re.match(r'query_bidding_records|查询招投标记录', text):
        return 5, 0
    if re.match(r'query_enterprise_legal_person_information|查询企业法人信息', text):
        return 5, 1
    if re.match(r'bidding_information_subscription|招标信息订阅', text):
        return 6, 0
    if re.match(r'roadshow_event_summary|路演活动总结', text):
        return 6, 1
    if re.match(r'others|其他', text):
        return 7, 0
    else:
        return 999, 0

if __name__ == '__main__':
    # 示例使用
    examples = [
        '招投标信息查询',
        '招投标项目概述',
        '路演活动查询',
        '路演活动详情',
        '查询企业参展信息',
        '企业参展概述',
        '查看招标公告',
        '查询中标企业',
        '路演活动预约',
        '招投标政策解读',
        '查询招投标记录',
        '查询企业法人信息',
        '招标信息订阅',
        '路演活动总结',
        '其他',
        'query_bidding_information',
        'bidding_project_overview',
        'query_roadshow_events',
        'roadshow_event_details',
        'query_enterprise_exhibition_information',
        'enterprise_exhibition_overview',
        'view_bidding_announcement',
        'query_winning_enterprises',
        'roadshow_event_booking',
        'bidding_policy_interpretation',
        'query_bidding_records',
        'query_enterprise_legal_person_information',
        'bidding_information_subscription',
        'roadshow_event_summary',
        'others',
    ]

    for example in examples:
        print(f"'{example}' -> {intent_encoding(example)}")
