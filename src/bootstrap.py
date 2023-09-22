# Collect all source files and run the project

import csv
import os


def main():

    # Read SCV file

    csv_file = "misc/dataset/dataset.csv"

    data = []

    with open(csv_file, newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

    # Удалите первую строку, если она содержит заголовки столбцов (u,v,t,h)
    if data and data[0] == ['u', 'v', 't', 'h']:
        data = data[1:]

    # Transfer data to group with unique user

    data_group_per_user = {}

    data_len = len(data)

    i = 0
    for i in range(data_len):

        # Get new user

        user = data[i][0]

        # Write to group_per_user

        if user not in data_group_per_user.keys():

            data_group_per_user[user] = {
                data[i][1]: [data[i][2], data[i][3]],
            }

        else:

            data_group_per_user[user][data[i][1]] = \
                [data[i][2], data[i][3]]

        i += 1

    # Combine friends_prediction_list

    friends_prediction_list = {}

    for user in data_group_per_user:

        # Get user data
        user_data = data_group_per_user[user]
        friends_prediction_list[user] = []

        # Process

        user_friends_list = user_data.keys()

        for friend in user_friends_list:
            if friend in data_group_per_user:
                for step_friend in data_group_per_user[friend]:
                    if len(friends_prediction_list[user]) < 10:
                        friends_prediction_list[user].append(step_friend)

    # print("FFFFFFFFFF")

    # print(friends_prediction_list)

    # for user in friends_prediction_list:
    #    print(len(friends_prediction_list[user]))

    # Format friends_prediction_list to 2D array

    result_data = []

    fpl_keys = friends_prediction_list.keys()

    i = 0
    for user in fpl_keys:

        user_friends_array = friends_prediction_list[user]

        user_friends_array.insert(0, user)

        result_data.append(user_friends_array)

        i += 1

    # Write scv file

    # Ваш двумерный массив данных
    data = result_data

    csv_file = "dist/output_tmp.txt"  # Имя файла, в который вы хотите записать данные

    with open(csv_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)

        # Записываем данные из двумерного массива
        for row in data:
            csv_writer.writerow(row)

    print(f"Данные успешно записаны в файл {csv_file}")

    # Format SCV file from "," to ": " at first row place

    # Имя входного и выходного файлов
    input_file = "dist/output_tmp.txt"
    output_file = "dist/output.txt"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            values = line.strip().split(',')
            if values:
                key = values[0]
                values = values[1:]
                outfile.write(f"{key}: {','.join(values)}\n")

    print(f"Данные успешно преобразованы и записаны в файл {output_file}")

    # Remove tmp file

    file_to_delete = "dist/output_tmp.txt"

    try:
        os.remove(file_to_delete)
        print(f"Файл {file_to_delete} успешно удален.")
    except FileNotFoundError:
        print(f"Файл {file_to_delete} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла: {str(e)}")

    # Exit

    print("FINISHED")
