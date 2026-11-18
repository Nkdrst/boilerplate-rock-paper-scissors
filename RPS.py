def player(
    prev_play,
    opponent_history=[],
    my_history=[],
    three_gram={},
):
    ideal_response = {"P": "S", "R": "P", "S": "R"}

    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
        three_gram.clear()
        first_move = "R"
        my_history.append(first_move)
        return first_move

    opponent_history.append(prev_play)

    # Оновлюємо статистику трійок наших ходів
    if len(my_history) >= 3:
        seq3 = "".join(my_history[-3:])
        three_gram[seq3] = three_gram.get(seq3, 0) + 1

    # 1. Детектор kris (завжди б'є наш попередній хід)
    if len(my_history) >= 2 and opponent_history[-1] == ideal_response[my_history[-2]]:
        kris_move = ideal_response[my_history[-1]]
        move = ideal_response[kris_move]
        my_history.append(move)
        return move

    # 2. Детектор quincy (фіксований цикл R, P, P, S, R)
    quincy_cycle = ["R", "P", "P", "S", "R"]
    if len(opponent_history) >= 6:
        quincy_matches = sum(
            1 for i in range(len(opponent_history))
            if opponent_history[i] == quincy_cycle[i % 5]
        )
        if quincy_matches / len(opponent_history) > 0.85:
            next_quincy = quincy_cycle[len(opponent_history) % 5]
            move = ideal_response[next_quincy]
            my_history.append(move)
            return move

    # 3. Детектор mrugesh (б'є найчастіший хід із наших останніх 10)
    if len(my_history) >= 11:
        mrugesh_matches = 0
        checked = 0
        for i in range(10, len(opponent_history)):
            window = my_history[i - 10 : i]
            most_freq = max(set(window), key=window.count)
            if opponent_history[i] == ideal_response[most_freq]:
                mrugesh_matches += 1
            checked += 1
        if checked > 0 and mrugesh_matches / checked > 0.8:
            window = my_history[-10:]
            most_freq = max(set(window), key=window.count)
            next_mrugesh = ideal_response[most_freq]
            move = ideal_response[next_mrugesh]
            my_history.append(move)
            return move

    # 4. Стратегія проти abbey (передбачаємо наш наступний хід за 3-грамами)
    if len(my_history) >= 2:
        last_two = "".join(my_history[-2:])
        candidates = [last_two + "R", last_two + "P", last_two + "S"]
        best_seq = max(candidates, key=lambda k: three_gram.get(k, 0))
        predicted_my_next = best_seq[-1]
        abbey_move = ideal_response[predicted_my_next]
        move = ideal_response[abbey_move]
    else:
        move = "P"

    my_history.append(move)
    return move
