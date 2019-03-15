import csv

games = {}
with open("data-mini/transactions.csv") as f:
    file = csv.reader(f)
    next(f)
    for row in file:
        if row[1] not in games:
            games[row[1]] = 0
        games[row[1]] += 1

sorted_by_value = sorted(games.items(), key=lambda kv: kv[1])
actual_games = []
for i in sorted_by_value:
    if i[1] >= 900:
        actual_games.append(i[0])

to_be_written = {}
with open("data/games.csv") as f:
    file = csv.reader(f)
    next(f)
    for row in file:
        if row[0] in actual_games:
            to_be_written[row[0]] = row[1]

print(to_be_written)
print(len(to_be_written))

with open("data-mini/games.csv", "w+", newline='') as f:
    file = csv.writer(f)
    file.writerow(["game-id", "game-title"])
    for k in to_be_written:
        file.writerow([k, to_be_written[k]])

wanted_transactions = []
with open('data/transactions.csv') as f:
    csv_f = csv.reader(f)
    next(csv_f)
    for row in csv_f:
        if row[1] in to_be_written:
            wanted_transactions.append(row)

print(wanted_transactions)
print(len(wanted_transactions))

with open("data-mini/transactions.csv", "w+", newline='') as f:
    file = csv.writer(f)
    file.writerow(["user-id", "game-title", "behaviour-name", "values"])
    for k in wanted_transactions:
        file.writerow(k)

wanted_users = {}
with open('data-mini/transactions.csv') as f:
    csv_f = csv.reader(f)
    next(csv_f)
    for row in csv_f:
        if row[0] not in wanted_users:
            wanted_users[row[0]] = 0

print(wanted_users)
print(len(wanted_users))

with open("data-mini/users.csv", "w+", newline='') as f:
    file = csv.writer(f)
    file.writerow(["user-id"])
    for k in wanted_users:
        file.writerow([k])


# games = {}
# with open("data/games.csv") as f:
#     file = csv.reader(f)
#     next(file)
#     for row in file:
#         games[row[1]] = row[0]
#
# rows = []
# with open("../steam-video-games/steam-200k.csv") as f:
#     file = csv.reader(f)
#     next(file)
#     for row in file:
#         row[1] = games[row[1]]
#         rows.append(row[:-1])
#
# with open("data/transactions.csv", "w+", newline='') as f:
#     file = csv.writer(f)
#     file.writerow(["user-id", "game-title", "behaviour-name", "values"])
#     for row in rows:
#         file.writerow(row)

# print(len(users))
# user_set = list(set(users))
# print(len(user_set))
#
# with open("users.csv", "w+", newline='') as f:
#     file = csv.writer(f)
#     file.writerow(["user-id"])
#     for user in user_set:
#         file.writerow([user])

# users = []
# with open("../steam-video-games/steam-200k.csv") as f:
#     file = csv.reader(f)
#     next(file)
#     for row in file:
#         users.append(row[0])
#
# print(len(users))
# user_set = list(set(users))
# print(len(user_set))
#
# with open("users.csv", "w+", newline='') as f:
#     file = csv.writer(f)
#     file.writerow(["user-id"])
#     for user in user_set:
#         file.writerow([user])


# games = []
# with open("games.txt") as f:
#     for row in f:
#         games.append(row[:-1])
#
# print(games)
#
# with open("games.csv", "w+", newline='') as f:
#     file = csv.writer(f)
#     file.writerow(["game-id", "game-title"])
#     for i, game in enumerate(games):
#         file.writerow([i+1, game])
