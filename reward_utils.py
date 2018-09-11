import numpy as np


def points_dict_to_reward_list(points_dict, reward_list):
    list = []
    for key in points_dict:
        list.append(points_dict[key])
    reward_list.append(list)

    return reward_list


def calculate_Gij(i, j, reward_array, gamma=1):
    if i == np.asarray(reward_array).shape[0] - 1:
        return reward_array[i, j]
    else:
        return reward_array[i, j] + gamma * calculate_Gij(i + 1, j, reward_array)


# method for calculating MC target after each game/ episode for all time t

def calculate_G(reward_array, gamma=1):
    reward_array = np.asarray(reward_array)
    G = np.zeros(reward_array.shape)
    for i in range(reward_array.shape[0]):
        for j in range(reward_array.shape[1]):
            G[i, j] = calculate_Gij(i, j, reward_array, gamma)

    return G
