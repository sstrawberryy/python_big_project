import collections
import pandas as pd
import matplotlib.pyplot as plt


def init_func(df):
    """
    初始化函数 找出所有用户
    """
    user_list = set()
    for i in range(df.shape[0]):
        user_list.add(df['user_id'][i])
    user_list = list(user_list)
    print('用户数量:', len(user_list))
    return user_list


def find_top_shopping(df, user_list, top_num):
    """
    找出购买效率达人
    """
    shop_dict = collections.OrderedDict()
    total_dict = {}
    for i in user_list:
        shop_dict[str(i)] = 0
        total_dict[str(i)] = 0
    for i in range(df.shape[0]):
        str_user_id = str(df['user_id'][i])
        total_dict[str_user_id] += 1
        if (df['behavior_type'][i]) == 4:
            shop_dict[str_user_id] += 1
    for i in user_list:
        shop_dict[str(i)] = shop_dict[str(i)] / total_dict[str(i)] * 100
    shop_dict = sorted(shop_dict.items(), key=lambda x: x[1], reverse=True)
    print('购买效率达人:')
    flag = 0
    for key, val in shop_dict:
        flag += 1
        print('user_id:{}\t购买行为占比:{}%'.format(key, val))
        if flag == top_num:
            break


def find_similar(user_id, user_list, df, top_num):
    """
    找出同道中人
    """
    item_dict = collections.OrderedDict()
    compare_dict = collections.OrderedDict()
    compare_dict[str(user_id)] = 0
    for i in user_list:
        item_dict[str(i)] = set()
    for i in range(df.shape[0]):
        str_user_id = str(df['user_id'][i])
        item_type = df['item_category'][i]
        item_dict[str_user_id].add(str(item_type))
    for i in user_list:
        if str(i) == str(user_id):
            continue
        same_item = len(item_dict[user_id] & item_dict[str(i)])
        compare_dict[str(i)] = same_item
    compare_dict = sorted(compare_dict.items(), key=lambda x: x[1], reverse=True)
    print('用户{}的同道中人:'.format(user_id))
    flag = 0
    for key, val in compare_dict:
        flag += 1
        print('user_id:{},相似种类数:{}'.format(key, val))
        if flag == top_num:
            break


def draw_pie(df):
    """
    用户关注的商品分类饼图(前5)
    """
    type_dict = collections.OrderedDict()
    for i in range(df.shape[0]):
        str_type = str(df['item_category'][i])
        type_dict[str_type] = 0
    for i in range(df.shape[0]):
        str_type = str(df['item_category'][i])
        type_dict[str_type] += 1
    type_dict = sorted(type_dict.items(), key=lambda x: x[1], reverse=True)
    labels = []
    numbers = []
    flag = 0
    for key, val in type_dict:
        flag += 1
        if flag <= 5:
            labels.append('商品分类:' + key)
            numbers.append(val)
        elif flag == 6:
            labels.append('商品分类:其他')
            numbers.append(val)
        else:
            numbers[-1] += val
    plt.rcParams['font.family'] = 'FangSong'
    plt.pie(numbers, labels=labels, autopct='%0.1f%%')
    plt.title('用户关注的商品分类饼图(前5)')
    plt.savefig('用户关注的商品分类前5.svg')
    plt.close()


def draw_plot(df, user_id):
    date_frequency_dict = collections.OrderedDict()
    for i in range(df.shape[0]):
        if str(df['user_id'][i]) == user_id:
            date_info, _ = df['time'][i].split()
            date_frequency_dict[str(date_info)] = 0
    for i in range(df.shape[0]):
        if str(df['user_id'][i]) == user_id:
            date_info, _ = df['time'][i].split()
            date_frequency_dict[str(date_info)] += 1
    date_frequency_dict = sorted(date_frequency_dict.items(), key=lambda item: item[0])
    x = []
    y = []
    for key, val in date_frequency_dict:
        x.append(key)
        y.append(val)
    plt.rcParams['font.family'] = 'FangSong'
    plt.title('用户{}的购物活动时间折线图'.format(user_id))
    plt.tick_params(axis='x', labelsize=4.5)
    plt.xlabel('日期')
    plt.ylabel('4种购物活动次数')
    plt.plot(x, y)
    plt.savefig('用户{}的购物活动时间图.svg'.format(user_id))
    plt.close()


def draw_bar(df, user_list):
    """
    用户活跃度柱状图(前10)
    """
    frequency_dict = collections.OrderedDict()
    for i in user_list:
        frequency_dict[str(i)] = 0
    for i in range(df.shape[0]):
        str_user_id = str(df['user_id'][i])
        frequency_dict[str_user_id] += 1
    frequency_dict = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    flag = 0
    id_list = []
    frequency_list = []
    for key, val in frequency_dict:
        flag += 1
        id_list.append(key)
        frequency_list.append(val)
        if flag == 10:
            break
    x = range(len(id_list))
    plt.rcParams['font.family'] = 'STSong'
    plt.bar(x, height=frequency_list)
    plt.xticks(x, id_list)
    plt.xlabel('user_id')
    plt.ylabel('活跃度')
    plt.title('用户活跃度(前10)')
    plt.tick_params(axis='x', labelsize=6)
    plt.savefig('用户活跃度前10.svg')
    plt.close()


if __name__ == '__main__':
    feature_path = 'small_user.csv'
    df = pd.read_csv(feature_path, header=0)
    user_list = init_func(df)

    # 找出购买效率达人
    find_top_shopping(df, user_list, 10)

    # 找出同道中人
    find_similar('10001082', user_list, df, 10)

    # 给出三种数据画像
    draw_pie(df)
    draw_bar(df, user_list)
    draw_plot(df, '10001082')


