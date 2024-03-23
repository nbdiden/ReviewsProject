def calculate_rating_distribution(average_rating, rating_count, bounds):
    distribution = [0] * 5
    remaining_count = rating_count
    remaining_sum = average_rating * rating_count

    # Assign minimum proportion of each rating
    for i in range(5):
        min_count = int(bounds[i][0] * rating_count)
        distribution[i] = min_count
        remaining_count -= min_count
        remaining_sum -= min_count * (i + 1)

    # Distribute remaining ratings
    while remaining_count > 0:
        average_remaining = remaining_sum / remaining_count
        closest_rating = min(range(1, 6), key=lambda x: abs(x - average_remaining))
        if remaining_sum - closest_rating >= 0:
            distribution[closest_rating - 1] += 1
            remaining_sum -= closest_rating
            remaining_count -= 1
        else:
            break

    return distribution

# Example usage
average_rating = 4.6
rating_count = 670
bounds = [
    (0.012, 0.024),  # Bounds for 1-star ratings
    (0.012, 0.024),   # Bounds for 2-star ratings
    (0.048, 0.108),   # Bounds for 3-star ratings
    (0.12, 0.18),    # Bounds for 4-star ratings
    (0.78, 0.96)     # Bounds for 5-star ratings
]

distribution = calculate_rating_distribution(average_rating, rating_count, bounds)
print("Rating Distribution:")
for i in range(5):
    print(f"{i+1} star: {distribution[i]}")